import datetime
from django.utils.translation import gettext_lazy as _
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.blocks import BooleanBlock, CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock, RawHTMLBlock, ListBlock, PageChooserBlock, IntegerBlock, DateTimeBlock
from wmodelchooser.blocks import ModelChooserBlock
from .style_blocks import ElementStyleBlock, ElementStyleNoHoverBlock, MarqueeSettings
# from .privacy import PrivacyBlock
from .charts import ChartsStructBlock 
from .cards import ImageBlock, FixedImageCard, CircleImageCardBlock, HoverCTACard, IconTitleDesc
from .texts import SingleLineTextElement, MultiLineTextElement, HHCharBlock, HHRichTextBlock, MarqueeRichTextBlock
from .svg import MapBlock  
from .tables import HHTableBlock, HTableBlock
from .typing_effects import TypeWriterText, SwapWordTypeWriting
from .forms import EmbedFormPage, EmbedFormPageModal
from .sliders_banners import BannerBlock, sliderBlock


class HHEmbedBlock(StructBlock):
    embeds = ListBlock( StructBlock( [("height", CharBlock(blank=True, null=True, required=False, label = "object height", help = "height for this video embed object")),
                                      ("id", CharBlock(blank=True, null=True, required=False, label = "a uniqu ID", help = "a uniqu ID for this video embed object")),
                                      ("embed_link_url", EmbedBlock(blank=True, null=True, required=False)),] ) )

    class Meta:  #   noqa
        form_classname = "hh_embed struct_block"
        template = "blocks/hh_embed_block"
        label = "Embed Videos 🎬 📺"
        icon=""


class CountDownBlock(StructBlock):
    el_style =ElementStyleBlock(blank=True, null=True, required=False,label="CountDown Block Styles 🎨")
    date_time = DateTimeBlock(blank=True, null=True, required=False, default='2022, 1, 8, 15, 9, 17, 610972',form_classname="date_time",label="CountDown to", help_text = " targeted date & time")

    class Meta:  #   noqa
        template = "blocks/countdown_block.html"
        form_classname = 'count_down date_time_in_meta struct_block'
        label = "CountDown ⏲"
        icon=""


class SpaceLine(StructBlock):
    el_style =ElementStyleBlock(blank=True, null=True, required=False,label="Styles of EmptyLine Block 🎨")
    height=CharBlock(blank=True, null=True, required=False, max_length=20)
    class Meta: #noqa
        form_classname = "space_line struct_block"
        template="blocks/empty_line_block.html"
        label = "Empty Line ↕"
        icon=""


class HrElement(StructBlock):
    class Meta: #noqa
        form_classname = "hr struct_block"
        template="blocks/hr_element.html"
        label = "ــــــــــ Breaking Line ــــــــــ"
        icon=""


class RowStyleBlock(ElementStyleBlock):
    class Meta:
        form_classname = "styling_config tab_row_style row_style"
        icon=""


class ColStyleBlock(ElementStyleBlock):
    class Meta:
        form_classname = "styling_config tab_col_style col_style"
        icon=""


class TabBodyStreamBlock(StreamBlock):
    empty_line = SpaceLine(blank=True, null=True, required=False,)
    cd = CountDownBlock(blank=True, null=True, required=False,)
    type_writer = TypeWriterText(blank=True, null=True, required=False,)
    heading = SingleLineTextElement(blank=True, null=True, required=False,)
    paragraph = HHRichTextBlock(blank=True, null=True, required=False,help_text="you can use the mark-down code for font sizes, ex: [s1]=1rem [s2]=1.5rem [nl]=new_empty_line ")
    hr = HrElement(blank=True, null=True, required=False)
    marquee = MarqueeRichTextBlock(blank=True, null=True, required=False,icon="",help_text="same as RichText Paragraph but with moving behaviours")
    carousel = sliderBlock(blank=True, null=True, required=False,)
    image = ImageBlock(blank=True, null=True, required=False,)
    embed = HHEmbedBlock(blank=True, null=True, required=False, help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',template="blocks/hh_embed_block")
    embed_form = EmbedFormPage(blank=True, null=True, required=False,)
    custom_css = RawHTMLBlock(blank=True, null=True, required=False, icon="",template="blocks/custom_css_block.html",help_text="for this page only", label="custom Style ")
    custom_js = RawHTMLBlock(blank=True, null=True, required=False, icon="",template="blocks/custom_js_block.html",help_text="for this page only", label="custom JavaScript ")
    raw_code = RawHTMLBlock(blank=True, null=True, required=False, icon="",template="blocks/html_raw_block.html",help_text="for this page only", label="Custom HTML Code ")


class TabBodyColsBlock(StructBlock):
    cols=ListBlock(StructBlock( [
            ("col_style", ColStyleBlock(blank=True, null=True, required=False, label="This Tab's Column Styles 🎨")),
            ("col_items", TabBodyStreamBlock(blank=True, null=True, required=False, label='blocks/contents of this Column of this tab',help_text="choose any block/content type") ),
            ]), label="Tab's Body Column")
    class Meta:  #noqa
        form_classname = "struct_block tabs_cols_block"
        template = "blocks/tabs_cols_block.html"
        label = "Sections of (Rows and Columns)"
        icon=""


class TabBodyGridBlock(StructBlock):
    row_id = IntegerBlock(blank=True, null=True, required=False, autoincrease=True, help_text="Row ID")
    row_style = RowStyleBlock(blank=True, null=True, required=False, label="Tab's Body Styles 🎨")
    row = TabBodyColsBlock( blank=True, null=True, required=False,label=". . . .")

    class Meta:  #noqa
        form_classname = "struct_block tabs_grid_block"
        template = "blocks/tabs_grid_block.html"
        label = "Sections of (Rows and Columns)"
        icon=""


class TabsBlock(StructBlock):
    overall_title = CharBlock(blank=True, null=True, required=False,)
    template = ChoiceBlock(blank=True, null=True, required=False, choices=[('vert_a', _('Masonry')),('vert_b', _('Collapsible')),('vert_c', _('Vertical A')),('hor_a', _('Horizontal A'))], default='vert_a', label="Choose a template")
    title_width = CharBlock(blank=True, null=True, required=False, default="20%",max_length=5,help_text='Applicatble to some templates, width for titles column (default = 20%)', label='Titles Wrapper width')
    tabs = StructBlock( [
        ("tab",ListBlock(StructBlock( [
            ("title", SingleLineTextElement(blank=True, null=True, required=False, label="Tab Title/Heading")),
            ("body", TabBodyGridBlock(blank=True, null=True, required=False, label="Tab's body contents") ),
            ], label="")
        , label=" "))
    ], label="Tabs ")
            

    class Meta:  #noqa
        form_classname = "tabs struct_block"
        template = "blocks/accordion_tabs_block.html" # TODO only vertical c is correct 
        label = "Accordion Tabs 📰"
        icon=""


class InnerStreamBlock(StreamBlock):
    empty_line = SpaceLine(blank=True, null=True, required=False)
    heading = SingleLineTextElement(blank=True, null=True, required=False)
    paragraph = HHRichTextBlock(blank=True, null=True, required=False, help_text="you can use the mark-down code for font sizes, ex: [s1]=1rem [s2]=1.5rem [nl]=new_empty_line ")
    # rtl_paragraph = HHRichTextBlock(icon="",template="blocks/paragraph_bidi_block_styled.html",blank=True, null=True, required=False, label=' Paragraph for bidi languages ',help_text="you can use the mark-down code for font sizes, ex: [s1]=1rem [s2]=1.5rem [nl]=new_empty_line ")
    hr = HrElement(blank=True, null=True, required=False)
    marquee = MarqueeRichTextBlock(icon="",blank=True, null=True, required=False,help_text="same as RichText Paragraph but with moving behaviours")
    carousel = sliderBlock(blank=True, null=True, required=False)
    image = ImageBlock(blank=True, null=True, required=False)
    banner = BannerBlock(blank=True, null=True, required=False, help_text="Only Saved inside this Page (can't be accessed or reused in other pages)..! ")
    local_tabs = TabsBlock(blank=True, null=True, required=False)
    embed = HHEmbedBlock(blank=True, null=True, required=False, help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',template="blocks/hh_embed_block",)
    embed_form = EmbedFormPage(blank=True, null=True, required=False)
    custom_css = RawHTMLBlock(icon="",template="blocks/custom_css_block.html",blank=True, null=True, required=False, help_text="for this page only", label="custom Style ")
    custom_js = RawHTMLBlock(icon="",template="blocks/custom_js_block.html",blank=True, null=True, required=False, help_text="for this page only", label="custom JavaScript ")
    raw_code = RawHTMLBlock(icon="",template="blocks/html_raw_block.html",blank=True, null=True, required=False, help_text="for this page only", label="Custom HTML Code ")

    class Meta:
        form_classname = 'gallery_stream_section'
        icon=""


class InnerColumnsBlock(StructBlock):
    is_active=BooleanBlock(blank=True, null=True, required=False, default=False, label="Active Modal?", help_text = "if unchecked, this modal will not be shown")
    row_id = IntegerBlock(blank=True, autoincrease=True, null=True, help_text="Row ID")
    row_style = RowStyleBlock(blank=True, null=True, required=False, label="Modal Row Styles 🎨")
    row = StructBlock( [
        ("col",ListBlock(StructBlock( [
            ("col_style", ColStyleBlock(blank=True, null=True, required=False, label="Modal Column Styles 🎨")),
            ("col_row", InnerStreamBlock(blank=True, null=True, required=False, label='blocks/contents of this Column',help_text="choose any block/content type") ),
            ], label="🔳")
        , label="Columns"))
    ], label=" ")

    class Meta:  #noqa
        form_classname = "inner_columns struct_block"
        template = "blocks/in_page_modal_block.html"
        icon=""
        label="Modal/popup window 💬"


class ModalColumnsBlock(StructBlock):
    col_style=ColStyleBlock(blank=True, null=True, required=False, label="Modal Column Styles 🎨")
    col_row=InnerStreamBlock(blank=True, null=True, required=False, label='blocks/contents of this Column',help_text="choose any block/content type")
    
    class Meta:  #noqa
        form_classname = "inner_columns struct_block"
        template = "blocks/public_modal_columns.html"
        icon=""


class SectionsStructBlock(StructBlock):
    section_style = ElementStyleBlock(blank=True, null=True, required=False, label="Sections Block Styles 🎨")
    section_title = CharBlock(blank=True, null=True, required=False, label = "Section Title")
    sections =  StructBlock( [
        ("section",ListBlock(StructBlock( [
            ("summary", CharBlock(blank=True, null=True, required=False, label = "Summary")),
            ("details", TextBlock(blank=True, null=True, required=False, label="Details", rows=3, cols=90) ),
            ], label="Summary-Details Block", icon=" ")
        , label=" "))
    ], label="Sections")

    class Meta:
        template = "blocks/section.html"
        form_classname="section_block struct_block"
        icon=""
        label="Sections with Summary-Details Blocks "


class GalleryStreamBlock(StreamBlock):
    cd = CountDownBlock(group="Whatever Else",blank=True, null=True, required=False)
    empty_line = SpaceLine(group="Whatever Else",blank=True, null=True, required=False)
    hr = HrElement(group="Whatever Else",blank=True, null=True, required=False)
    map = MapBlock(group="Whatever Else",blank=True, null=True, required=False)
    embed = HHEmbedBlock(group="Whatever Else",blank=True, help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',null=True)
    type_writer = TypeWriterText(blank=True, null=True, required=False)
    swapping_type_writer = SwapWordTypeWriting(blank=True, null=True, required=False)
    heading = SingleLineTextElement(group="      SimpleText & RichText Blocks",blank=True, null=True, required=False)
    paragraph = HHRichTextBlock(group="      SimpleText & RichText Blocks",blank=True, null=True, required=False,help_text="you can use the mark-down code for font sizes, ex: [s1]=1rem [s2]=1.5rem..etc")
    marquee = MarqueeRichTextBlock(group="      SimpleText & RichText Blocks",icon="",blank=True, null=True, required=False,help_text="same as RichText Paragraph but with moving behaviours")
    carousel = sliderBlock(group="     Banner & Slider Blocks",blank=True, null=True, required=False)
    banner = BannerBlock(group="     Banner & Slider Blocks",blank=True, null=True, required=False, help_text="Only Saved inside this Page (can't be accessed or reused in other pages)..! ")
    image = ImageBlock(group="    Image & Card Blocks",blank=True, null=True, required=False)
    figure_image = FixedImageCard(group="    Image & Card Blocks",blank=True, null=True, required=False)
    itd = IconTitleDesc(group="    Image & Card Blocks",blank=True, null=True, required=False)
    local_tabs = TabsBlock(group="Complicated Blocks",blank=True, null=True, required=False)
    modal = InnerColumnsBlock(group="Complicated Blocks",blank=True, null=True, required=False, help_text="Only One modal block is applicable per page..! ")
    embed_form = EmbedFormPage(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False)
    embed_form_modal = EmbedFormPageModal(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False)
    charts = ChartsStructBlock(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False, help_text="Some Chart and Plot Blocks", label="Charts/Plots Blocks 📊📈")
    sections = SectionsStructBlock(group="Complicated Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False, help_text="Some Chart and Plot Blocks", label="Sections of Summary-Details Blocks ")
    table = HTableBlock(group="  Data Tables blocks",blank=True, null=True, required=False, help_text="Table Block", label="Table Block ")
    tablea = HHTableBlock(group="  Data Tables blocks",blank=True, null=True, required=False, help_text="Enhanced Table Block", label="Enhanced Table Block ")
    custom_css = RawHTMLBlock(group="Custom Local Code-Blocks", icon="",template="blocks/custom_css_block.html",blank=True, null=True, required=False, help_text="for this page only", label="custom (local) CSS 🎨")
    custom_js = RawHTMLBlock(group="Custom Local Code-Blocks", icon="",template="blocks/custom_js_block.html",blank=True, null=True, required=False, help_text="for this page only ", label="custom (local) JavaScript 📜")
    raw_code = RawHTMLBlock(group="Custom Local Code-Blocks", icon="",template="blocks/html_raw_block.html",blank=True, null=True, required=False, help_text="for this page only", label="Custom (local) HTML 📜")

    class Meta:
        form_classname = 'gallery_stream_section'
        icon=""


class ColumnsBlock(StructBlock):
    row_id = IntegerBlock(blank=True, autoincrease=True, null=True, help_text="Row ID")
    row_style = RowStyleBlock(blank=True, null=True, required=False, label="Row Styles 🎨")
    row = StructBlock( [
        ("col",ListBlock(StructBlock( [
            ("col_style", ColStyleBlock(blank=True, null=True, required=False, label="Column Styles 🎨")),
            ("col_row", GalleryStreamBlock(blank=True, null=True, required=False, label='Column contents ⦋⦌⦋o⦌⦋⦌',help_text="choose any block/content type") ),
            ], label="Column⦋⦌")
        , label="Columns ⦋⦌⦋⦌⦋⦌"))
    ], label="Row contents ⊟o⊟")

    class Meta:  #noqa
        form_classname = "columns struct_block"
        template = "blocks/columns_block.html"
        label = "Row⊟"
        # icon=""


class AsideBaseStreamBlock(StreamBlock):
    heading = SingleLineTextElement(group="      SimpleText & RichText Blocks",blank=True, null=True, required=False)
    paragraph = HHRichTextBlock(group="      SimpleText & RichText Blocks",blank=True, null=True, required=False,help_text="you can use the mark-down code for font sizes, ex: [s1]=1rem [s2]=1.5rem..etc")
    marquee = MarqueeRichTextBlock(group="      SimpleText & RichText Blocks",icon="",blank=True, null=True, required=False,help_text="same as RichText Paragraph but with moving behaviours")
    carousel = sliderBlock(group="     Banner & Slider Blocks",blank=True, null=True, required=False)
    banner = BannerBlock(group="     Banner & Slider Blocks",blank=True, null=True, required=False, help_text="Only Saved inside this Page (can't be accessed or reused in other pages)..! ")
    image = ImageBlock(group="    Image & Card Blocks",blank=True, null=True, required=False)
    figure_image = FixedImageCard(group="    Image & Card Blocks",blank=True, null=True, required=False)
    itd = IconTitleDesc(group="    Image & Card Blocks",blank=True, null=True, required=False)
    local_tabs = TabsBlock(group="Complicated Blocks",blank=True, null=True, required=False)
    cd = CountDownBlock(group="Whatever Else",blank=True, null=True, required=False)
    empty_line = SpaceLine(group="Whatever Else",blank=True, null=True, required=False)
    hr = HrElement(group="Whatever Else",blank=True, null=True, required=False)
    embed = HHEmbedBlock(group="Whatever Else",blank=True, help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',null=True)
    embed_form = EmbedFormPage(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False)
    embed_form_modal = EmbedFormPageModal(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False)
    charts = ChartsStructBlock(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False, help_text="Some Chart and Plot Blocks", label="Charts/Plots Blocks 📊📈")
    table = HTableBlock(group="  Data Tables blocks",blank=True, null=True, required=False, help_text="Table Block", label="Table Block ")
    tablea = HHTableBlock(group="  Data Tables blocks",blank=True, null=True, required=False, help_text="Enhanced Table Block", label="Enhanced Table Block ")
    raw_code = RawHTMLBlock(group="Custom Local Code-Blocks", icon="",template="blocks/html_raw_block.html",blank=True, null=True, required=False, help_text="for this page only", label="Custom (local) HTML 📜")


class BlogStreamBlock(StreamBlock):
    cd = CountDownBlock(group="Whatever Else",blank=True, null=True, required=False)
    empty_line = SpaceLine(group="Whatever Else",blank=True, null=True, required=False)
    hr = HrElement(group="Whatever Else",blank=True, null=True, required=False)
    map = MapBlock(group="Whatever Else",blank=True, null=True, required=False)
    embed = HHEmbedBlock(group="Whatever Else",blank=True, help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',null=True)
    type_writer = TypeWriterText(blank=True, null=True, required=False)
    swapping_type_writer = SwapWordTypeWriting(blank=True, null=True, required=False)
    heading = SingleLineTextElement(group="      SimpleText & RichText Blocks",blank=True, null=True, required=False)
    paragraph = HHRichTextBlock(group="      SimpleText & RichText Blocks",blank=True, null=True, required=False,help_text="you can use the mark-down code for font sizes, ex: [s1]=1rem [s2]=1.5rem..etc")
    marquee = MarqueeRichTextBlock(group="      SimpleText & RichText Blocks",icon="",blank=True, null=True, required=False,help_text="same as RichText Paragraph but with moving behaviours")
    carousel = sliderBlock(group="     Banner & Slider Blocks",blank=True, null=True, required=False)
    banner = BannerBlock(group="     Banner & Slider Blocks",blank=True, null=True, required=False, help_text="Only Saved inside this Page (can't be accessed or reused in other pages)..! ")
    image = ImageBlock(group="    Image & Card Blocks",blank=True, null=True, required=False)
    figure_image = FixedImageCard(group="    Image & Card Blocks",blank=True, null=True, required=False)
    itd = IconTitleDesc(group="    Image & Card Blocks",blank=True, null=True, required=False)
    local_tabs = TabsBlock(group="Complicated Blocks",blank=True, null=True, required=False)
    modal = InnerColumnsBlock(group="Complicated Blocks",blank=True, null=True, required=False, help_text="Only One modal block is applicable per page..! ")
    embed_form = EmbedFormPage(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False)
    embed_form_modal = EmbedFormPageModal(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False)
    charts = ChartsStructBlock(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False, help_text="Some Chart and Plot Blocks", label="Charts/Plots Blocks 📊📈")
    sections = SectionsStructBlock(group="Complicated Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False, help_text="Some Chart and Plot Blocks", label="Sections of Summary-Details Blocks ")
    table = HTableBlock(group="  Data Tables blocks",blank=True, null=True, required=False, help_text="Table Block", label="Table Block ")
    tablea = HHTableBlock(group="  Data Tables blocks",blank=True, null=True, required=False, help_text="Enhanced Table Block", label="Enhanced Table Block ")
    custom_css = RawHTMLBlock(group="Custom Local Code-Blocks", icon="",template="blocks/custom_css_block.html",blank=True, null=True, required=False, help_text="for this page only", label="custom (local) CSS 🎨")
    
    class Meta:
        form_classname = 'gallery_stream_section'
        icon=""


class BlogsAsideStreamBlock(StreamBlock):
    heading = SingleLineTextElement(group="      SimpleText & RichText Blocks",blank=True, null=True, required=False)
    paragraph = HHRichTextBlock(group="      SimpleText & RichText Blocks",blank=True, null=True, required=False,help_text="you can use the mark-down code for font sizes, ex: [s1]=1rem [s2]=1.5rem..etc")
    marquee = MarqueeRichTextBlock(group="      SimpleText & RichText Blocks",icon="",blank=True, null=True, required=False,help_text="same as RichText Paragraph but with moving behaviours")
    carousel = sliderBlock(group="     Banner & Slider Blocks",blank=True, null=True, required=False)
    banner = BannerBlock(group="     Banner & Slider Blocks",blank=True, null=True, required=False, help_text="Only Saved inside this Page (can't be accessed or reused in other pages)..! ")
    image = ImageBlock(group="    Image & Card Blocks",blank=True, null=True, required=False)
    figure_image = FixedImageCard(group="    Image & Card Blocks",blank=True, null=True, required=False)
    itd = IconTitleDesc(group="    Image & Card Blocks",blank=True, null=True, required=False)
    local_tabs = TabsBlock(group="Complicated Blocks",blank=True, null=True, required=False)
    cd = CountDownBlock(group="Whatever Else",blank=True, null=True, required=False)
    empty_line = SpaceLine(group="Whatever Else",blank=True, null=True, required=False)
    hr = HrElement(group="Whatever Else",blank=True, null=True, required=False)
    embed = HHEmbedBlock(group="Whatever Else",blank=True, help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',null=True)
    embed_form = EmbedFormPage(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False)
    embed_form_modal = EmbedFormPageModal(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False)
    charts = ChartsStructBlock(group="    Data Collecting Form Blocks & Data Presentation Chart blocks",blank=True, null=True, required=False, help_text="Some Chart and Plot Blocks", label="Charts/Plots Blocks 📊📈")
    table = HTableBlock(group="  Data Tables blocks",blank=True, null=True, required=False, help_text="Table Block", label="Table Block ")
    tablea = HHTableBlock(group="  Data Tables blocks",blank=True, null=True, required=False, help_text="Enhanced Table Block", label="Enhanced Table Block ")
    raw_code = RawHTMLBlock(group="Custom Local Code-Blocks", icon="",template="blocks/html_raw_block.html",blank=True, null=True, required=False, help_text="for this page only", label="Custom (local) HTML 📜")


class MainBaseStreamBlock(StreamBlock):
    pass
