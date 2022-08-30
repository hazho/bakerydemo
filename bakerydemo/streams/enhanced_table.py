from django import forms
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.templatetags.static import static

from wagtail.admin.staticfiles import versioned_static
from wagtail.blocks.base import Block, DeclarativeSubBlocksMetaclass, get_help_icon
from wagtail.telepath import Adapter, register


class EnhancedTableBlockValidationError(ValidationError):
    def __init__(self, cell_errors=None):
        self.cell_errors = cell_errors
        super().__init__('Validation error in EnhancedTableBlock', params=cell_errors)


class EnhancedTableBlockValidationErrorAdapter(Adapter):
    js_constructor = 'enhanced_table.EnhancedTableBlockValidationError'

    def js_args(self, error):
        if error.cell_errors is None:
            return [None]
        else:
            return [
                {
                    row_index: {
                        col_index: cell_error
                        for col_index, cell_error in row_errors.items()
                    }
                    for row_index, row_errors in error.cell_errors.items()
                }
            ]

    @cached_property
    def media(self):
        return forms.Media(js=[
            static('enhanced_table/js/enhanced_table.js'),
        ])


register(EnhancedTableBlockValidationErrorAdapter(), EnhancedTableBlockValidationError)


class TypedTable:
    template = 'enhanced_table/enhanced_table.html'

    def __init__(self, columns, row_data):
        # a list of dicts, each with items 'block' (the block instance) 
        self.columns = columns

        # a list of dicts, each with an item 'values' (the list of block values)
        self.row_data = row_data

    @property
    def rows(self):
        """
        Iterate over the rows of the table, with each row returned as a list of BoundBlocks
        """
        for row in self.row_data:
            yield [
                column['block'].bind(value)
                for column, value in zip(self.columns, row['values'])
            ]

    def get_context(self, parent_context=None):
        context = parent_context or {}
        context.update({
            'self': self,
            'value': self,
        })
        return context

    def render_as_block(self, context=None):
        return render_to_string(self.template, self.get_context(context))


class BaseEnhancedTableBlock(Block):
    def __init__(self, local_blocks=None, **kwargs):
        self._constructor_kwargs = kwargs

        super().__init__(**kwargs)

        # create a local (shallow) copy of base_blocks so that it can be supplemented by local_blocks
        self.child_blocks = self.base_blocks.copy()
        if local_blocks:
            for name, block in local_blocks:
                block.set_name(name)
                self.child_blocks[name] = block

    def value_from_datadict(self, data, files, prefix):
        column_count = int(data['%s-column-count' % prefix])
        columns = [
            {
                'id': i,
                'type': data['%s-column-%d-type' % (prefix, i)],
                'order': int(data['%s-column-%d-order' % (prefix, i)]),
            }
            for i in range(0, column_count)
            if not data['%s-column-%d-deleted' % (prefix, i)]
        ]
        columns.sort(key=lambda col: col['order'])
        for col in columns:
            col['block'] = self.child_blocks[col['type']]

        row_count = int(data['%s-row-count' % prefix])
        rows = [
            {
                'id': row_index,
                'order': int(data['%s-row-%d-order' % (prefix, row_index)]),
                'values': [
                    col['block'].value_from_datadict(
                        data, files, '%s-cell-%d-%d' % (prefix, row_index, col['id'])
                    )
                    for col in columns
                ],
            }
            for row_index in range(0, row_count)
            if not data['%s-row-%d-deleted' % (prefix, row_index)]
        ]
        rows.sort(key=lambda row: row['order'])

        return TypedTable(
            columns=[
                {'block': col['block']}
                for col in columns
            ],
            row_data=[
                {'values': row['values']}
                for row in rows
            ],
        )

    def get_prep_value(self, table):
        if table:
            return {
                'columns': [
                    {'type': col['block'].name}
                    for col in table.columns
                ],
                'rows': [
                    {
                        'values': [
                            column['block'].get_prep_value(val)
                            for column, val in zip(table.columns, row['values'])
                        ]
                    }
                    for row in table.row_data
                ]
            }
        else:
            return {
                'columns': [],
                'rows': [],
            }

    def to_python(self, value):
        if value:
            columns = [
                {
                    'block': self.child_blocks[col['type']],
                }
                for col in value['columns']
            ]
            # restore data column-by-column to take advantage of bulk_to_python
            columns_data = [
                col['block'].bulk_to_python([
                    row['values'][column_index] for row in value['rows']
                ])
                for column_index, col in enumerate(columns)
            ]
            return TypedTable(
                columns=columns,
                row_data=[
                    {
                        'values': [
                            column_data[row_index]
                            for column_data in columns_data
                        ]
                    }
                    for row_index in range(0, len(value['rows']))
                ]
            )
        else:
            return TypedTable(
                columns=[],
                row_data=[],
            )

    def get_form_state(self, table):
        if table:
            return {
                'columns': [
                    {'type': col['block'].name}
                    for col in table.columns
                ],
                'rows': [
                    {
                        'values': [
                            column['block'].get_form_state(val)
                            for column, val in zip(table.columns, row['values'])
                        ]
                    }
                    for row in table.row_data
                ]
            }
        else:
            return {
                'columns': [],
                'rows': [],
            }

    def clean(self, table):
        if table:
            # a dict where each key is a row index, and the value is a dict of errors on that row keyed by column index
            cell_errors = {}
            cleaned_rows = []
            for row_index, row in enumerate(table.row_data):
                row_errors = {}
                row_data = []
                for col_index, column in enumerate(table.columns):
                    val = row['values'][col_index]
                    try:
                        row_data.append(column['block'].clean(val))
                    except ValidationError as e:
                        row_errors[col_index] = e

                if row_errors:
                    cell_errors[row_index] = row_errors
                else:
                    cleaned_rows.append({'values': row_data})

            if cell_errors:
                raise EnhancedTableBlockValidationError(cell_errors=cell_errors)
            else:
                return TypedTable(columns=table.columns, row_data=cleaned_rows)

        else:
            return TypedTable(columns=[], row_data=[])

    def deconstruct(self):
        """
        Always deconstruct EnhancedTableBlock instances as if they were plain EnhancedTableBlock with all
        of the field definitions passed to the constructor - even if in reality this is a subclass
        with the fields defined declaratively, or some combination of the two.

        This ensures that the field definitions get frozen into migrations, rather than leaving a
        reference to a custom subclass in the user's models.py that may or may not stick around.
        """
        path = 'enhanced_table.blocks.EnhancedTableBlock'
        args = [list(self.child_blocks.items())]
        kwargs = self._constructor_kwargs
        return (path, args, kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        for name, child_block in self.child_blocks.items():
            errors.extend(child_block.check(**kwargs))
            errors.extend(child_block._check_name(**kwargs))

        return errors

    def render_basic(self, value, context=None):
        if value:
            return value.render_as_block(context)
        else:
            return ''

    class Meta:
        default = None
        icon = "table"


class EnhancedTableBlock(BaseEnhancedTableBlock, metaclass=DeclarativeSubBlocksMetaclass):
    pass


class EnhancedTableBlockAdapter(Adapter):
    js_constructor = 'enhanced_table.blocks.EnhancedTableBlock'

    def js_args(self, block):
        meta = {
            'label': block.label, 'required': block.required, 'icon': block.meta.icon,
            'strings': {
                'ADD_COLUMN': "Add column",
                'ADD_ROW': "Add row",
                'INSERT_COLUMN': "Insert column",
                'DELETE_COLUMN': "Delete column",
                'INSERT_ROW': "Insert row",
                'DELETE_ROW': "Delete row",
            },
        }

        help_text = getattr(block.meta, 'help_text', None)
        if help_text:
            meta['helpText'] = help_text
            meta['helpIcon'] = get_help_icon()

        return [
            block.name,
            block.child_blocks.values(),
            {
                name: child_block.get_form_state(child_block.get_default())
                for name, child_block in block.child_blocks.items()
            },
            meta,
        ]

    @cached_property
    def media(self):
        return forms.Media(js=[
            static('enhanced_table/js/enhanced_table.js'),
        ], css={
            'all': [
                static('enhanced_table/css/enhanced_table.css'),
            ]
        })


register(EnhancedTableBlockAdapter(), EnhancedTableBlock)
