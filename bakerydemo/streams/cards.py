from wagtail.blocks import BooleanBlock, CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock, RawHTMLBlock, ListBlock, PageChooserBlock, IntegerBlock, DateTimeBlock

from wagtail.images.blocks import ImageChooserBlock
from .style_blocks import ElementStyleBlock, ElementStyleNoHoverBlock, MarqueeSettings
from .texts import SingleLineTextElement, MultiLineTextElement


class ImageBlock(StructBlock):
    el_style =ElementStyleBlock(blank=True, null=True, required=False,label="Image Styles 🎨")
    image = ImageChooserBlock(blank=True, null=True, required=False,label="Image")

    class Meta:
        template = "blocks/image_element.html"
        label = "Image Element📷"
        form_classname = 'image_block struct_block'
        icon="📷"
        group="Image & Card Blocks"
    

class FixedImageCard(StructBlock):
    el_style=ElementStyleBlock(blank=True, null=True, required=False,label="Figure Card Styles 🎨")
    caption=CharBlock(blank=True, null=True, required=False, max_length=50)

    class Meta:
        template = "blocks/cards/fixed_image_card.html"
        label = "Image Card📷"
        form_classname = 'fixed_image_card struct_block'
        icon="📷"
        group="Image & Card Blocks"


class CircleImageCardBlock(StructBlock):
    content_height = CharBlock(blank=True, null=True, required=False, default="12rem", max_length=8)
    cards = ListBlock( StructBlock( [
        ("img", ImageChooserBlock(blank=True, null=True, required=False,)),
        ("title", SingleLineTextElement(blank=True, null=True, required=False, max_length=100)),
        ("description", MultiLineTextElement(blank=True, null=True, required=False, max_length=4000)),
        ("el_pg_link", PageChooserBlock(blank=True, null=True, required=False,)),
        ("link_url", CharBlock(blank=True, null=True, required=False, max_length=200, )),
    ] ) )
    
    class Meta:  #noqa
        form_classname = "circle_img_cards struct_block"
        template = "blocks/circle_card_block"
        label = "Card Block with Circle Image  "
        icon=""
        group="Image & Card Blocks"


class HoverCTACard(StructBlock):
    el_style=ElementStyleBlock(blank=True, null=True, required=False,label="Styles of CTA-Card Block 🎨")
    image=ImageBlock(blank=True, null=True, required=False, label="CTA Image")
    title=SingleLineTextElement(blank=True, null=True, required=False, label="CTA Heading/Title")
    description=MultiLineTextElement(blank=True, null=True, required=False, max_length=4000, label="About CTA")

    class Meta:  #noqa
        template = "blocks/cards/hover_c_t_a_card.html"
        form_classname = 'hoverable_cta_card struct_block'
        label = "Hoverable CTA Card Block"
        icon=""
        group="Image & Card Blocks"
    

class IconTitleDesc(StructBlock):
    el_style=ElementStyleBlock(blank=True, null=True, required=False,label="Styles of This-Card Block 🎨")
    icon=CharBlock(blank=True, null=True, required=False, label="Icon")
    title=CharBlock(blank=True, null=True, required=False, max_length=100, label="Under-Icon Title")
    desc=TextBlock(blank=True, null=True, required=False, max_length=4000, label="Description(back-side)")

    class Meta:  #noqa
        template = "blocks/cards/icon_title_desc_card.html"
        form_classname = 'itd struct_block'
        label = "Icon Title Desciption Card Block 🔣"
        icon=""
        group="Image & Card Blocks"
