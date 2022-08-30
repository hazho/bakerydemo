import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.functional import cached_property
from wagtail.blocks import BooleanBlock, CharBlock, ChoiceBlock, StructBlock, PageChooserBlock, IntegerBlock, DateTimeBlock

from wagtail.images.blocks import ImageChooserBlock

Now=timezone.now()
OPACITYCHOISES=[("FF", "100%"),("E6", "90%"),("CC", "80%"),("B3", "70%"),("99", "60%"),("80", "50%"),("66", "40%"),("4D", "30%"),("33", "20%"),("1A", "10%"),("03", "01%")]
beh_choices=[('slide', 'Slide'), ('scrolling', 'Scrolling'),('alternate', 'Alternate')]
dir_choices=[('Up', 'Up'),('Down', 'Down'), ('left', 'Left'),('right', 'Right')]

class TimeLineProperty(StructBlock):  #  TODO template
    s_at = DateTimeBlock(form_classname="start_at",required=False, blank=True, null=True, label="Appear at", help_text = " This element/block will be displayed starting from this date/time")
    e_at = DateTimeBlock(form_classname="end_at",required=False, blank=True, null=True, label="Disappear at", help_text = " This element/block will be disappearing at this date/time")
    class Meta: form_classname = "struct-block scheduling_property"

class ElementHoverStyleBlock(StructBlock):  #  TODO template
    title = CharBlock(form_classname="infotip",required=False, max_length=580, blank=True, null=True, label="Hover Text(infotip) ", help_text = " when visitor hovers on this element, this text will be shown as an infotip")
    h_width = CharBlock(form_classname="h_width",required=False, max_length=28, blank=True, null=True, label="Width ", help_text = " px, em, rem or % ")
    h_height = CharBlock(required=False, max_length=28, blank=True, null=True, label="Height ", help_text = " px, em, rem or % ")
    h_padding = CharBlock(required=False, max_length=28, blank=True, null=True, label="Padding", help_text = "clockwise(top right bottom left) px, rem or % ",)
    h_margin = CharBlock(required=False, max_length=28, blank=True, null=True, label="Margin", help_text = "clockwise(top right bottom left) px, rem or % ")
    h_font_size = CharBlock(required=False, max_length=28, blank=True, null=True, label="Font Size", help_text = " px, em, rem or % ")
    
    h_box_shadow = CharBlock(required=False, max_length=180, blank=True, null=True, label="box-shadow ", help_text = "ex: 0px 0px 1px red % ")
    h_b_radius = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Corner Radius", help_text = "Example: 1rem Solid red")
    h_b_top = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Top Border", help_text = "Example: 1rem Solid red")
    h_b_right = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Right Border", help_text = "Example: 1rem Solid red")
    h_b_bottom = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Bottom Border", help_text = "Example: 1rem Solid red")
    h_b_left = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Left Border", help_text = "Example: 1rem Solid red")
    
    h_color = CharBlock(required=False, max_length=28, blank=True, null=True, default="",  label="Text Color ", help_text = "....")
    h_color_opacity = ChoiceBlock(choices=OPACITYCHOISES, default="", required=False, max_length=6, blank=True, null=True,  label="Color Opacity", help_text = ". . . . . .")
    h_use_bg_color = BooleanBlock(required=False, blank=True, null=True,  label="Use", help_text = "Use bg color")
    h_bg_c = CharBlock(required=False, max_length=28, blank=True, null=True,  label="BG-Color ", help_text = "Background Color ")
    h_bg_color_opacity = ChoiceBlock(choices=OPACITYCHOISES, default="", required=False, max_length=6, blank=True, null=True,  label="BG Color Opacity", help_text = ". . . . . .")
    h_image = ImageChooserBlock(required=False, blank=True, null=True, label="BG Image")
    class Meta:
        form_classname = "hover_styling_config element_hover_style"
        template = "includes/hover_element_style.html"


class ElementStyleBlock(StructBlock):  #  TODO template
    no_mobile = BooleanBlock(required=False, blank=True, null=True, default=False, label="No Mobile", help_text = "....",template="includes/mobile_desktop.html")
    no_desktop = BooleanBlock(required=False, blank=True, null=True, default=False, label="No Desktop", help_text = "....",template="includes/mobile_desktop.html")
    
    el_class=CharBlock(required=False,max_length=800, blank=True, null=True, help_text = "....", label="Class")
    el_id=CharBlock(required=False,max_length=800, blank=True, null=True, help_text = "....", label="ID")
    
    width = CharBlock(group="sizing",required=False, max_length=28, blank=True, null=True, label="Width ", help_text = " px, em, rem or % ")
    height = CharBlock(group="sizing",required=False, max_length=28, blank=True, null=True, label="Height ", help_text = " px, em, rem or % ")
    
    padding = CharBlock(group="sizing",default=".5rem", required=False, max_length=28, blank=True, null=True, label="Padding", help_text = "clockwise(top right bottom left) px, rem or % ",)
    margin = CharBlock(group="sizing",required=False, max_length=28, blank=True, null=True, label="Margin", help_text = "clockwise(top right bottom left) px, rem or % ")
    
    z_index=CharBlock(required=False,max_length=800, blank=True, null=True, help_text = "depth (layer ordering)", label="z-index")
    transform=CharBlock(required=False,max_length=50, blank=True, null=True, help_text = "ex: rotateZ(90deg)", label="Transform")
    font_size = CharBlock(group="sizing",required=False, max_length=28, blank=True, null=True, label="Font Size", help_text = " px, em, rem or % ")
    text_align = ChoiceBlock(choices=[('left', _('Left')), ('center', _('Center')), ('right', _('Right'))],required=False, max_length=6, blank=True, null=True, label="text align", help_text = "left, right or center")   
    text_shadow = CharBlock(default="0 0 0 yellow", required=False, max_length=150, blank=True, null=True, label="text Shadow", help_text = "example: 1px 1px 2px white, 2px 2px 4px grey")   
    position = ChoiceBlock(choices=[("absolute", _("Absolute")) ,("fixed", _("Fixed")) ,("inherit", _("Inherit")) ,("initial", _("Initial")) ,("relative", _("Relative")) ,("revert", _("Revert")) ,("static", _("Static")) ,("sticky", _("Sticky")) ,("unset", _("Unset"))],required=False, max_length=6, blank=True, null=True, default="none", label="Position", help_text = ". . . . .")   
    left = CharBlock(required=False, max_length=28, blank=True, null=True, label="left Position", help_text = " px, em, rem or % ")
    top = CharBlock(required=False, max_length=28, blank=True, null=True, label="top Position", help_text = " px, em, rem or % ")
    floating = ChoiceBlock(choices=[('left', _('Left')), ('none', _('None(Default)')), ('right', _('Right'))],required=False, max_length=6, blank=True, null=True, default="none", label="Floating", help_text = "left or right")   
    overflow = ChoiceBlock(required=False,choices=[('auto', _('Auto(Default')), ('scroll', _('Scroll')), ('visible', _('Visible')), ('hidden', _('Hidden')), ('inherit', _('Inherit')), ('initial', _('Initial')), ('overlay', _('Overlay')), ('revert', _('Revert')), ('unset', _('Unset'))], default="auto", blank=True, null=True, label="Overflow ", help_text = "....")
    
    box_shadow = CharBlock(required=False, max_length=180, blank=True, null=True, label="box-shadow ", help_text = "ex: 0px 0px 1px red % ")
    b_radius = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Corner Radius", help_text = "Border Raidus Example: 50%")
    b_top = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Top Border", help_text = "Example: 1rem Solid red")
    b_right = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Right Border", help_text = "Example: 1rem Solid red")
    b_bottom = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Bottom Border", help_text = "Example: 1rem Solid red")
    b_left = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Left Border", help_text = "Example: 1rem Solid red")
    
    color = CharBlock(required=False, max_length=28, blank=True, null=True, default="#000", label="Text Color ", help_text = "....")
    color_opacity = ChoiceBlock(choices=OPACITYCHOISES, default="FF",required=False, max_length=6, blank=True, null=True,  label="Color Opacity", help_text = ". . . . . .")
    use_bg_color = BooleanBlock(required=False, blank=True, null=True, default=False, label="Use", help_text = "Use Background color")
    bg_c = CharBlock(required=False, max_length=28, blank=True, null=True, default="", label="BG-Color ", help_text = "Background Color ")
    bg_color_opacity = ChoiceBlock(choices=OPACITYCHOISES, default="FF",required=False, max_length=6, blank=True, null=True,  label="BG-Color Opacity", help_text = ". . . . . .")
    
    paralax = BooleanBlock(required=False, blank=True, null=True, default=False, label="Paralaxed BG")
    image = ImageChooserBlock(required=False, blank=True, null=True, label="BG Image")
    
    el_pg_link=PageChooserBlock(required=False, blank=True, null=True, help_text = "Link this element to a local page", label="Page Link")
    el_url_link=CharBlock(required=False,max_length=800, blank=True, null=True, help_text = "Link this element to another website", label="External URL")
    new_tab = BooleanBlock(required=False, blank=True, null=True, default=False, label="New Tab", help_text = "Check here to open the link in a New Tab")
    
    live = TimeLineProperty(required=False, blank=True, null=True, label="Scheduling(appearing/disappearing period)")
    hover_styling = ElementHoverStyleBlock(required=False, blank=True, null=True, label="Hover Styling")

    class Meta:
        form_classname = "styling_config element_style"
        template = "includes/element_style.html"


class ElementStyleNoHoverBlock(StructBlock):  #  TODO template
    no_mobile = BooleanBlock(required=False, blank=True, null=True, default=False, label="No Mobile", help_text = "....",template="includes/mobile_desktop.html")
    no_desktop = BooleanBlock(required=False, blank=True, null=True, default=False, label="No Desktop", help_text = "....",template="includes/mobile_desktop.html")
    
    el_class=CharBlock(required=False,max_length=800, blank=True, null=True, help_text = "....", label="Class")
    el_id=CharBlock(required=False,max_length=800, blank=True, null=True, help_text = "....", label="ID")
    
    width = CharBlock(required=False, max_length=28, blank=True, null=True, default="100%", label="Width ", help_text = " px, em, rem or % ")
    height = CharBlock(required=False, max_length=28, blank=True, null=True, label="Height ", help_text = " px, em, rem or % ")
    
    padding = CharBlock(default=".5rem", required=False, max_length=28, blank=True, null=True, label="Padding", help_text = "clockwise(top right bottom left) px, rem or % ",)
    margin = CharBlock(required=False, max_length=28, blank=True, null=True, label="Margin", help_text = "clockwise(top right bottom left) px, rem or % ")
    
    z_index=CharBlock(required=False,max_length=800, blank=True, null=True, help_text = "depth (layer ordering)", label="z-index")
    font_size = CharBlock(required=False, max_length=28, blank=True, null=True, label="Font Size", help_text = " px, em, rem or % ")
    text_align = ChoiceBlock(choices=[('left', _('Left')), ('center', _('Center')), ('right', _('Right'))],required=False, max_length=6, blank=True, null=True, label="text align", help_text = "left, right or center")   
    text_shadow = CharBlock(default="0px 0px 0px", required=False, max_length=150, blank=True, null=True, label="text Shadow", help_text = "example: 1px 1px 2px white, 2px 2px 4px grey")   
    position = ChoiceBlock(choices=[("absolute", _("Absolute")) ,("fixed", _("Fixed")) ,("inherit", _("Inherit")) ,("initial", _("Initial")) ,("relative", _("Relative")) ,("revert", _("Revert")) ,("static", _("Static")) ,("sticky", _("Sticky")) ,("unset", _("Unset"))],required=False, max_length=6, blank=True, null=True, default="none", label="Position", help_text = ". . . . .")   
    left = CharBlock(required=False, max_length=28, blank=True, null=True, label="left Position", help_text = " px, em, rem or % ")
    top = CharBlock(required=False, max_length=28, blank=True, null=True, label="top Position", help_text = " px, em, rem or % ")
    floating = ChoiceBlock(choices=[('left', _('Left')), ('none', _('None(Default)')), ('right', _('Right'))],required=False, max_length=6, blank=True, null=True, label="Floating", help_text = "left or right")   
    overflow = ChoiceBlock(required=False,choices=[('auto', _('Auto(Default')), ('scroll', _('Scroll')), ('visible', _('Visible')), ('hidden', _('Hidden')), ('inherit', _('Inherit')), ('initial', _('Initial')), ('overlay', _('Overlay')), ('revert', _('Revert')), ('unset', _('Unset'))], default="unset", blank=True, null=True, label="Overflow ", help_text = "....")
    
    box_shadow = CharBlock(required=False, max_length=180, blank=True, null=True, label="box-shadow ", help_text = "ex: 0px 0px 1px red % ")
    b_radius = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Corner Radius", help_text = "Border Raidus Example: 50%")
    b_top = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Top Border", help_text = "Example: 1rem Solid red")
    b_right = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Right Border", help_text = "Example: 1rem Solid red")
    b_bottom = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Bottom Border", help_text = "Example: 1rem Solid red")
    b_left = CharBlock(required=False, max_length=60, blank=True, null=True,  label="Left Border", help_text = "Example: 1rem Solid red")
    
    color = CharBlock(required=False, max_length=28, blank=True, null=True, default="#000", label="Color ", help_text = "....")
    color_opacity = ChoiceBlock(choices=OPACITYCHOISES, default="FF",required=False, max_length=6, blank=True, null=True,  label="Color Opacity", help_text = ". . . . . .")
    use_bg_color = BooleanBlock(required=False, blank=True, null=True, default=False, label="Use BG-Color", help_text = "Use Background color")
    bg_c = CharBlock(required=False, max_length=28, blank=True, null=True, default="", label="BG-Color ", help_text = "Background Color ")
    bg_color_opacity = ChoiceBlock(choices=OPACITYCHOISES, default="FF",required=False, max_length=6, blank=True, null=True,  label="BG-Color Opacity", help_text = ". . . . . .")
    
    paralax = BooleanBlock(required=False, blank=True, null=True, default=False, label="Is paralaxed BG")
    image = ImageChooserBlock(required=False, blank=True, null=True, label="BG Image")
    
    el_pg_link=PageChooserBlock(required=False, blank=True, null=True, help_text = "Link this element to a local page", label="Page Link")
    el_url_link=CharBlock(required=False,max_length=800, blank=True, null=True, help_text = "Link this element to another website", label="URL Link")
    new_tab = BooleanBlock(required=False, blank=True, null=True, default=False, label="New Tab", help_text = "Check here to open the link in a New Tab")
    
    live = TimeLineProperty(required=False, blank=True, null=True, label="Scheduling(appearing/disappearing period)")

    
    class Meta:
        form_classname = "styling_config element_style"
        template = "includes/element_style.html"


class MarqueeSettings(StructBlock):
    loop=           CharBlock(required=False, max_length=60, blank=True, null=True, help_text = "how many times the moving will be repeated before it stops, default: no stoping")
    use_bg_color =  BooleanBlock(required=False, blank=True, null=True, default=False, label="Use BG-Color", help_text = "Use Background color")
    bg_c=           CharBlock(default="#01010100",required=False, max_length=60, blank=True, null=True, label="BG-Color ", help_text = "Background Color ")
    behavior=       ChoiceBlock(default="slide", required=False, max_length=60, blank=True, null=True, choices=beh_choices)
    dir=            ChoiceBlock(default="left", required=False, max_length=60, blank=True, null=True, choices = dir_choices)
    scrollamount=   CharBlock(default="4", required=False, max_length=60, blank=True, null=True,  label="Speed", help_text = "Speed: 1, 2, ...")
    width =         CharBlock(default="100%", required=False, max_length=28, blank=True, null=True, label="Width ", help_text = " px, em, rem or % ")
    height =        CharBlock(required=False, max_length=28, blank=True, null=True, label="Height ", help_text = " px, em, rem or % ")
    padding =       CharBlock(required=False, max_length=28, blank=True, null=True, label="Padding", help_text = "clockwise(top right bottom left) px, rem or % ",)
    margin =        CharBlock(required=False, max_length=28, blank=True, null=True, label="Margin", help_text = "clockwise(top right bottom left) px, rem or % ")
    box_shadow =    CharBlock(required=False, max_length=180, blank=True, null=True, label="box-shadow ", help_text = "ex: 0px 0px 1px red % ")
    b_radius =      CharBlock(required=False, max_length=60, blank=True, null=True,  label="Corner Radius", help_text = "Border Raidus Example: 50%")
    border =        CharBlock(required=False, max_length=60, blank=True, null=True,  label="Border", help_text = "Example: 4px Solid red")
    
    class Meta:
        form_classname = "styling_config element_style"
        form_template = "block_forms/ms.html"