import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler
from wagtail import hooks


def _insert_feature_before(features, insert_feature, anchor_feature):
    try:
        index = features.default_features.index(anchor_feature)
    except ValueError:
        index = None
    if index is not None:
        features.default_features.insert(index, insert_feature)
    else:
        features.default_features.append(insert_feature)

def _insert_feature_after(features, insert_feature, anchor_feature):
    try:
        index = features.default_features.index(anchor_feature)
    except ValueError:
        index = None
    if index is not None:
        features.default_features.insert(index + 1, insert_feature)
    else:
        features.default_features.append(insert_feature)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Creates centered text in our richtext editor."""
    feature_name = "centero"
    type_ = "CENTERTHETEXT"
    tag = "div"
    control = {"element":tag,"type": type_,"label": "Center","description": "Center the selected line","style": {"margin": "0 auto","text-align": "center"}}
    features.register_editor_plugin("draftail", feature_name, draftail_features.BlockFeature(control))
    db_conversion = {
        "from_database_format": {tag: BlockElementHandler(type_)},
        "to_database_format": {"block_map": {type_: {"element": tag,"props": {"class": "center","style": {"margin": "0 auto","text-align": "center"}}}}}
    }
    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_tab_space_feature(features):
    """Creates indentation for the selected text in our richtext editor."""
    feature_name = "tab"
    type_ = "TABSPACE"
    tag = "span"
    control = {"element":tag,"type": type_,"label": "Tab Space","description": "Add a Tab Space before the selected word","style": {"margin": "0 0 0 1.5rem","text-indent": "2rem"}}
    features.register_editor_plugin("draftail", feature_name, draftail_features.InlineStyleFeature(control))
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_:  {"element": tag,"props": {"class": "indent","style": {"margin": "0 0 0 1.5rem","text-indent": "2rem"}}}}}
    }
    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


# @hooks.register("register_rich_text_features")
def register_id_feature(features):
    """adds the ID attribute to the selected text in our richtext editor."""
    feature_name = "id"
    type_ = "ADD_ID"
    tag = "span"
    control = {"element":tag,"type": type_,"label": "ID","description": "Add an ID to the selected string","class": "ided"}
    features.register_editor_plugin("draftail", feature_name, draftail_features.InlineStyleFeature(control))
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_:  {"element": tag,"props": {"class": "ided", "id":""}}}}
    }
    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    feature_name = 'mark'
    tag = 'mark'
    # Configure how Draftail handles the feature in its toolbar.
    control = {'type': feature_name.upper(),'label': '☆','description': 'Mark/Highlight',}
    features.register_editor_plugin('draftail', feature_name, draftail_features.InlineStyleFeature(control))
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(feature_name.upper())},
        'to_database_format': {'style_map': {feature_name.upper(): tag}},
    }
    features.register_converter_rule('contentstate', feature_name, db_conversion)
    features.default_features.append('mark')


@hooks.register('register_rich_text_features')
def register_br_feature(features):
    feature_name = 'br'
    tag = 'br'
    control = {'type': feature_name.upper(),'label': '','description': 'BR',}
    features.register_editor_plugin('draftail',feature_name,draftail_features.InlineStyleFeature(control,))
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(feature_name.upper())},
        'to_database_format': {'style_map': {feature_name.upper(): tag}},
    }
    features.register_converter_rule('contentstate', feature_name, db_conversion)
    # features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_defaults(features):
    features.default_features.append('subscript')
    features.default_features.append('superscript')
    features.default_features.append('INSERT')
    # features.default_features.append('h1')
    _insert_feature_before(features, 'h1', 'h2')
    # _insert_feature_after(features, 'h5', 'h4')
    # _insert_feature_after(features, 'h6', 'h5')
    features.default_features.insert(2000, 'h5')
    features.default_features.append('h6')
    
    return features.default_features


from .views import SlideChooserViewSet


@hooks.register('register_admin_viewset')
def register_slide_chooser_viewset():
    return SlideChooserViewSet('slide_chooser', url_prefix='slide-chooser')
