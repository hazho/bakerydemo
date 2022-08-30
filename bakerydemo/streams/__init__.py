import wagtail.core.fields


################################################################################################################
# Remove the database field definition override that Wagtail adds to StreamFields. It creates unnecessary churn
# in our migration files that ends up being really annoying.
################################################################################################################
def deconstruct_without_block_definition(self):
    name, path, _, kwargs = super(wagtail.core.fields.StreamField, self).deconstruct()
    block_types = list()
    args = [block_types]
    return name, path, args, kwargs
wagtail.core.fields.StreamField.deconstruct = deconstruct_without_block_definition

