
from wagtail.core.blocks import ChooserBlock
from functools import cached_property

class SlideChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from .models import CarouselItems
        return CarouselItems

    @cached_property
    def widget(self):
        from .widgets import SlideChooserWidget
        return SlideChooserWidget()

    def get_form_state(self, value):
        return self.widget.get_value_data(value)
