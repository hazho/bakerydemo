
from django.utils.translation import gettext_lazy as _

from generic_chooser.views import ModelChooserViewSet

from .models import CarouselItems


class SlideChooserViewSet(ModelChooserViewSet):
    icon = 'user'
    model = CarouselItems
    page_title = _("Choose a Slide")
    per_page = 2