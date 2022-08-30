from wagtail.blocks import CharBlock, StructBlock, PageChooserBlock


class EmbedFormPage(StructBlock):
    height=CharBlock(blank=True, null=True, required=False, max_length=6, default="100%", label="Form Height")
    width=CharBlock(blank=True, null=True, required=False, max_length=6, default="100%", label="Form Width")
    pg_link=PageChooserBlock(blank=True, null=True, required=False, label="Page", target_model="base.FormPage") #

    class Meta:  #   noqa
        template = "blocks/embed_form_page_block.html"
        label = "Embed Form 📄"
        icon = ""
        form_classname="form_embed_element"
        
 

class EmbedFormPageModal(StructBlock):
    height=CharBlock(blank=True, null=True, required=False, max_length=6, default="100%", label="modal Height")
    width=CharBlock(blank=True, null=True, required=False, max_length=6, default="100%", label="modal Width")
    b_text=CharBlock(blank=True, null=True, required=False, max_length=60, default="Open Form", label="Button Text")
    m_title=CharBlock(blank=True, null=True, required=False, max_length=60, default="Form For ?????? ", label="Modal Window Title")
    pg_link=PageChooserBlock(blank=True, null=True, required=False, label="Page", target_model="base.FormPage")

    class Meta:  #   noqa
        template = "blocks/embed_form_modal_block.html"
        label = "Embed Form (as Modal) 📄💬"
        icon = ""
        form_classname="form_embed_modal"
        
 