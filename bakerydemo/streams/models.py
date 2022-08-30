from django.db import models
from wagtail.search import index
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import Site, Orderable
from wagtail.admin.panels import FieldPanel,InlinePanel,FieldPanel # ,FieldRowPanel,MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class PageSection(index.Indexed, ClusterableModel, BaseSetting):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    panels = [InlinePanel('caro_item_section_model', label="Slide", classname="object collapsible multi-field")]

    def __str__(self): return f"Slides of {self.site}"
    class Meta:
        managed = True
        verbose_name = 'Slides'
        verbose_name_plural = 'Slides'


def create_page_sections(sender, **kwargs):
    if kwargs['created']:
        PageSection.objects.create(site=kwargs['instance'])
models.signals.post_save.connect(create_page_sections, sender=Site)


# @register_model_chooser
class CarouselItems(Orderable):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    page = ParentalKey('PageSection', related_name='caro_item_section_model', on_delete=models.CASCADE)
    img=models.ForeignKey("wagtailimages.Image",null=True,blank=True,on_delete=models.SET_NULL,related_name="+")
    slide_title=models.CharField(max_length=100, blank=True, null=True, verbose_name='Slide Heading/Title')
    slide_text=models.CharField(max_length=1000, blank=True, null=True, verbose_name='Slide Promotional Pragraph Text')
    slide_url_linking=models.CharField(max_length=500, blank=True, verbose_name='or     Slide-Link External URL')
    slide_page_linking=models.ForeignKey("wagtailcore.Page",null=True,blank=True,related_name="+",on_delete=models.PROTECT, verbose_name='Slide-Link Internal Page-Chooser')
    slide_in_new_tab=models.BooleanField(default=False, blank=True, verbose_name='open Slide-Link in a new Browser-Tab?')

    panels=[FieldPanel("img",heading="slide background"),FieldPanel("slide_title"),FieldPanel("slide_text"),FieldPanel("slide_page_linking"),FieldPanel("slide_url_linking"),FieldPanel("slide_in_new_tab")]

    @property
    def link(self):
        if self.slide_page_linking:
            return self.slide_page_linking.url
        elif self.slide_url_linking:
            return self.slide_url_linking
        return None

    def __str__(self):
        if self.slide_title:
            string = 'slide:' + self.slide_title + '| #' + str(self.id)
        else:
            string = 'slide: #' + str(self.id)
        return string

    class Meta:
        verbose_name="slide"
        verbose_name_plural="slides"
