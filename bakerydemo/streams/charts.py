
from django.utils.translation import gettext_lazy as _
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlock, CharBlock, IntegerBlock, StreamBlock, ListBlock
from wplotly.blocks.plot import BarChartBlock,ContourPlotBlock,HeatmapPlotBlock,LinePlotBlock,PieChartBlock,ScatterPlotBlock
from .style_blocks import ElementStyleBlock
from wagtail_grafl.blocks import GraflBlock


class ChartsStreamBlock(StreamBlock):
    bar_chart = BarChartBlock(blank=True, null=True, required=False,label="Bar Chart") # , template = "blocks/bar_charts_plots.html"
    pie_chart = PieChartBlock(blank=True, null=True, required=False,label="Pie Chart")
    contour_plot = ContourPlotBlock(blank=True, null=True, required=False,label="Contour Plot")
    heatmap_plot = HeatmapPlotBlock(blank=True, null=True, required=False,label="Heatmap Plot")
    line_plot = LinePlotBlock(blank=True, null=True, required=False,label="Line Plot")
    scatter_plot = ScatterPlotBlock(blank=True, null=True, required=False,label="Scatter Plot")
    grafl_plot = GraflBlock(blank=True, null=True, required=False,label="Expremental JSON Plot(Processed by a third-party API)", help_text="If you are concerned about your Data, please Do NOT use this option, because it been processed by a third party API..!")


class ChartsStructBlock(StructBlock):
    c_style = ElementStyleBlock(blank=True, null=True, required=False, label="Chart Block Styles 🎨")
    c_type = ChartsStreamBlock(max_num=10, blank=True, null=True, required=False, label='Type of Chart/Plot',help_text="choose any Chart/Plot type")

    class Meta:
        template = "blocks/charts_plots.html"
        form_classname="charts_block struct_block"
        icon=""
        label="Chart & Plots Block "
        


''' the follwing are not in use yet '''
class ChartsPieBlock(StructBlock):
    el_styles = ElementStyleBlock(blank=True, null=True, required=False,label="Styles of Block 🎨")
    charts = StructBlock( [
        ("chart",ListBlock(StructBlock( [
            ("title", CharBlock(blank=True, null=True, required=False, label="Title/Heading")),
            ("value", IntegerBlock(blank=True, null=True, required=False,) ),
            ])
        , label=" - - - - - - - - "))
    ], label="Pie Charts")
            
    class Meta:  #noqa
        form_classname = "pie_chart struct_block"
        template = "blocks/chart_circle.html"
        label = _("Pie Charts Blocks")
        icon=""


class ChartsBarSingleValueBlock(StructBlock):
    el_styles = ElementStyleBlock(blank=True, null=True, required=False,label="Styles of Block 🎨")
    charts = StructBlock( [
        ("chart",ListBlock(StructBlock( [
            ("title", CharBlock(blank=True, null=True, required=False, label="Title/Heading")),
            ("value", IntegerBlock(blank=True, null=True, required=False,) ),
            ])
        , label=" - - - - - - - - "))
    ], label="Single Value Bar Chart")
            
    class Meta:  #noqa
        form_classname = "bar_chart struct_block"
        template = "blocks/chart_bar_1v.html"
        label = _("Single Value Bar Chart Blocks")
        icon=""


class ChartsBarDoubleValueBlock(StructBlock):
    el_styles = ElementStyleBlock(blank=True, null=True, required=False,label="Styles of Block 🎨")
    charts = StructBlock( [
        ("chart",ListBlock(StructBlock( [
            ("title", CharBlock(blank=True, null=True, required=False, label="Title/Heading")),
            ("value1", IntegerBlock(blank=True, null=True, required=False,) ),
            ("value2", IntegerBlock(blank=True, null=True, required=False,) ),
            ])
        , label=" - - - - - - - - "))
    ], label="Double Value Bar Chart")
            
    class Meta:  #noqa
        form_classname = "double_bar_chart struct_block"
        template = "blocks/chart_bar_2v.html"
        label = _("Double Value Bar Chart Blocks")
        icon=""
