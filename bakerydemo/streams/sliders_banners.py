from wagtail.blocks import CharBlock, StreamBlock, StructBlock, ListBlock
from wmodelchooser.blocks import ModelChooserBlock

from .texts import SingleLineTextElement, MultiLineTextElement, HHCharBlock
from .style_blocks import ElementStyleBlock
from .g_choosers import SlideChooserBlock


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


# class sliderBlock(StructBlock):
#     overall_title = CharBlock(blank=True, null=True, required=False, form_classname="hhhhhhhh")
#     min_height = CharBlock(blank=True, null=True, required=False, verbose_name="slider height",default="500px")
#     sliding_speed = CharBlock(blank=True, null=True, required=False,default=2000)
#     slide = ListBlock(StructBlock([('caroslide',ModelChooserBlock('streams.CarouselItems',blank=True, null=True, required=False, label='Slide'))]))
    
#     class Meta:  #   noqa 
#         template = "blocks/slides_block.html"
#         form_classname = 'slides_block struct_block'
#         label = "Shared Slider ◀ 📷 ▶"
#         icon=""
#         group="Slider & Banner Blocks"


class sliderBlock(StructBlock):
    overall_title = CharBlock(blank=True, null=True, required=False, form_classname="hhhhhhhh")
    min_height = CharBlock(blank=True, null=True, required=False, verbose_name="slider height",default="500px")
    sliding_speed = CharBlock(blank=True, null=True, required=False,default=2000)
    slide = ListBlock(StructBlock([('caroslide',SlideChooserBlock('streams.CarouselItems',blank=True, null=True,  label='Slide'))]))
    
    class Meta:  #   noqa 
        template = "blocks/slides_block.html"
        form_classname = 'slides_block struct_block'
        label = "Shared Slider ◀ 📷 ▶"
        icon=""
        group="Slider & Banner Blocks"
