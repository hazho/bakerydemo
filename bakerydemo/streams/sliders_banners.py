from wagtail.blocks import CharBlock, StreamBlock, StructBlock, ListBlock

from .texts import SingleLineTextElement, MultiLineTextElement, HHCharBlock
from .style_blocks import ElementStyleBlock


class BannerBlock(StructBlock):
    banner = StructBlock([
        ("el_style", ElementStyleBlock(blank=True, null=True, required=False,label="Styles of Banner Block 🎨")),
        ("title", SingleLineTextElement(blank=True, null=True, required=False,label="Banner's Heading/Title")),
        ("description", MultiLineTextElement(blank=True, null=True, required=False,label="Banner's Description")),
    ], form_classname="banner_block")

    class Meta:  #noqa
        template = "blocks/banner_block.html"
        form_classname="banner_block struct_block"
        icon=""
        label="Banner 💬"
        group="Slider & Banner Blocks"

