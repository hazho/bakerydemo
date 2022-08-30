
from wagtail.contrib.table_block.blocks import TableBlock
# from wagtail.contrib.typed_table_block.blocks import TypedTableBlock as EnhancedTableBlock
from wagtail.blocks import BooleanBlock, CharBlock, RichTextBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock
from .style_blocks import ElementStyleNoHoverBlock
# from .enhanced_table import EnhancedTableBlock
from .en_tables import TypedTableBlock as EnhancedTableBlock


class HHTableBlock(StructBlock):
    el_style =ElementStyleNoHoverBlock(blank=True, null=True, required=False,label="Styles of Table Block 🎨") 
    table = EnhancedTableBlock([
        # ('text', CharBlock(blank=True, null=True, required=False,template="blocks/hh_table_block_text.html")),
        ('rich_text', RichTextBlock(blank=True, null=True, required=False,template="blocks/hh_table_block_paragraph.html")),
        # ('image', ImageChooserBlock(blank=True, null=True, required=False,))
    ])
    class Meta:  #   noqa
        form_classname = "hh_table struct_block"
        template = "blocks/hh_table_block.html"
        label = "Enhanced Table Block "
        icon=""
        group="Table Blocks"

 
class HTableBlock(StructBlock):
    el_style =ElementStyleNoHoverBlock(blank=True, null=True, required=False,label="Styles of Table Block 🎨") 
    table=TableBlock(table_options={'stretchH': 'all','manualColumnResize': True, 'manualRowResize': True, 'minSpareRows': 0,'startRows': 3,'startCols': 4, 'autoColumnSize': True,'height': 100,
        'contextMenu': ['row_above','row_below','---------','col_left','col_right','---------','remove_row','remove_col','---------','undo','redo','---------','alignment'],},)

    class Meta:  #   noqa
        template = "blocks/table_block.html"
        form_classname = 'table_block struct_block'
        label = "Simple Table Block "
        icon=""
        group="Table Blocks"
