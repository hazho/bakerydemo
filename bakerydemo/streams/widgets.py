from django.contrib.admin.utils import quote
from django.urls import reverse
from generic_chooser.widgets import AdminChooser

from .models import CarouselItems


class SlideChooserWidget(AdminChooser):
    model = CarouselItems
    choose_modal_url_name = 'slide_chooser:choose'

    def get_edit_item_url(self, item):
        return reverse('wagtailsnippets:edit', args=('base', 'carouselitems', quote(item.pk)))