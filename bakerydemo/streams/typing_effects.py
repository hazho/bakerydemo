from wagtail.blocks import BooleanBlock, CharBlock, RichTextBlock, StructBlock, ListBlock
from .style_blocks import ElementStyleBlock


class SwapWordTypeWriting(StructBlock):
    el_style=ElementStyleBlock(blank=True, null=True, required=False,label="STW Styles 🎨")
    delay=CharBlock(blank=True, null=True, required=False, max_length=6, default="500", label="when to start?", help = "after page loaded, when do you want to start the type writing")
    l_ch_s=CharBlock(blank=True, null=True, required=False, max_length=6, default="500", label="letter-changing speed")
    k_t=CharBlock(blank=True, null=True, required=False, max_length=6, default="1000", label="word keeping time")
    words = ListBlock( StructBlock( [("w", CharBlock(blank=True, null=True, required=False, max_length=600, label = "Word", help = "Word you want to be effected by this block and swapped by some other words like this"))] ) )

    class Meta:  #   noqa
        form_classname = "swap_tw struct_block"
        template = "blocks/swapping_words_type_writing.html"
        label = "Swapping Words TypeWritter ⌨️"
        icon=""
        group="Typing Effects Blocks"


class TypeWriterText(StructBlock):
    el_style = ElementStyleBlock(blank=True, null=True, required=False,label="Styles of Type writter block 🎨")
    text = CharBlock(blank=True, null=True, required=False, form_classname="typewriter_text")
    speed = CharBlock(blank=True, null=True, required=False, label="Speed (by milliseconds)", form_classname="typewriter_speed")
    interval = CharBlock(blank=True, null=True, required=False, label="Delay (by seconds)", form_classname="typewriter_interval", default="0.5")
    repeat = CharBlock(blank=True, null=True, required=False, form_classname="typewriter_repeat")
    # privacy = PrivacyBlock(blank=True, null=True, required=False,label="this block private to")    #  TODO 
    
    class Meta:  #   noqa
        template = "blocks/typewriter_block.html"
        form_classname = 'typewriter struct_block'
        label = "TypeWriter ⌨️"
        icon=""
        group="Typing Effects Blocks"
