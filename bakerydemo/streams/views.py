from generic_chooser.views import ModelChooserViewSet

from .models import CarouselItems


class SlideChooserViewSet(ModelChooserViewSet):
    icon = 'cog'
    model = CarouselItems
    per_page = 10