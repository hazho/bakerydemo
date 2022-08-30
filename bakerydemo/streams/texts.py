from wagtail.blocks import CharBlock, RichTextBlock, StructBlock, TextBlock, RichTextBlock, StructBlock
from .style_blocks import ElementStyleBlock, MarqueeSettings


class SingleLineTextElement(StructBlock):
    el_style=ElementStyleBlock(blank=True, null=True, required=False,label="SLT Styles 🎨")
    heading_text = CharBlock(blank=True, null=True, required=False,max_length=500, form_classname="title", label="SLT")

    class Meta:
        form_classname = "struct_block slt heading_block_config"
        template = "blocks/singl_line_text_element.html"
        label = "SingleLine Text"
        icon=""
        


class MultiLineTextElement(StructBlock):
    el_style=ElementStyleBlock(blank=True, null=True, required=False,label="MLT Styles 🎨")
    text=TextBlock(blank=True, null=True, required=False, max_length=1000, label="MLT", rows=5, cols=90)

    class Meta:  #noqa
        form_classname = "multi_lines_text struct_block"
        template = "blocks/multi_line_text_block.html"
        label = "Multi-Line Text Element"
        icon=""
        


class HHCharBlock(StructBlock):
    text=CharBlock(blank=True, null=True, required=False, max_length=1000,)

    class Meta:  #noqa
        form_classname = "hh_char struct_block"
        template = "blocks/hh_char_block.html"
        label = "Char Element"
        icon=""
        


class HHRichTextBlock(StructBlock):
    el_style=ElementStyleBlock(blank=True, null=True, required=False, label="Paragraph Block Styles 🎨")
    # read: https://docs.wagtail.org/en/stable/advanced_topics/customisation/page_editing_interface.html#rich-text-features
    paragraph = RichTextBlock( blank=True, null=True, required=False, label=' Rich-text Paragraph ')
    class Meta:
        form_classname = "styled_rich_text struct_block"
        db_table = ''
        managed = True
        label = 'Paragraph 📜'
        verbose_name_plural = ' Styled rich_texts'
        template="blocks/paragraph_block_styled.html"
        icon=""
        


class MarqueeRichTextBlock(StructBlock):
    ms=MarqueeSettings(blank=True, null=True, required=False,label="Settings and Styles 🎨")
    paragraph = RichTextBlock(blank=True, null=True, required=False, label=' Rich-text Paragraph ')
    
    class Meta:
        form_classname = "styled_rich_text struct_block"
        db_table = ''
        managed = True
        label = 'Moving Paragraph 📜'
        verbose_name_plural = 'Scrolling RichText'
        template="blocks/paragraph_scrolling_marquee.html"
        icon=""
        
