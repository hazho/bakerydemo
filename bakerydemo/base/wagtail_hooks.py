from django.contrib.auth.models import Permission
# from django.contrib import admin
from django.templatetags.static import static
from django.views.generic import TemplateView
from django.urls import path, reverse
from django.utils.html import format_html #  , format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.site_summary import SummaryItem
from wagtail.admin.navigation import get_site_for_user
from wagtail.admin.menu import MenuItem, SubmenuMenuItem, reports_menu # , AdminOnlyMenuItem
from wagtail.models import Site
from wagtail import hooks
from wagtail.admin.search import SearchArea
from wagtail.documents.permissions import permission_policy as doc_perm_pol

# from .admin_site import * # noqa
# from .models import HHPage


# construct_main_menu_name='construct_main_menu'
# construct_settings_menu_name='construct_settings_menu'
# construct_reports_menu_name='construct_reports_menu'
# @hooks.register('construct_reports_menu')
# # @hooks.register(construct_main_menu_name)
# def hide_some_menu_items(request, menu_items):
#     # for i in menu_items: print(i.name.lower())
#     if not request.user.is_superuser:
#         # for i in menu_items: print(i)
#         menu_items[:] = [item for item in menu_items if item.name.lower() not in ["site-history", "workflows","workflow-tasks"] ]
#         # print(menu_items)

# # @hooks.register('construct_main_menu')
# # def hide_sidebar_menu_items(request, menu_items): menu_items[:] = [item for item in menu_items if item.name not in [] ]


# @hooks.register('register_permissions')
# def view_email_app(): return Permission.objects.filter(codename="view_emails")


# @hooks.register('register_permissions')
# def view_email_receipt(): return Permission.objects.filter(codename="view_email_receipt")


# class HelpSummaryItem(SummaryItem):
#     order=10
#     template_name='documentation/help_summary.html'
#     icon_name='question-circle'

#     def get_context_data(self, parent_context):
#         site_name = get_site_for_user(self.request.user)['site_name']
#         icon_name=self.icon_name
#         return {'site_name': site_name,'icon_name': icon_name,}
        
#     def is_shown(self):
#         # return self.request.user.has_perm('add')
#         return True


# @hooks.register('construct_homepage_summary_items')
# def add_help_summary_item(request, items):
#     items.append(HelpSummaryItem(request))


# class AdminDocumentationView(TemplateView):
#     template_name = "documentation/help_page.html"
#     def get_context_data(self, **kwargs):      
#         context = super().get_context_data(**kwargs)
#         context["self"]=HHPage.objects.get(slug="help")
#         return context


# @hooks.register('register_admin_urls')
# def doc_url(): return [path('help/', AdminDocumentationView.as_view(), name='help'),]

# @hooks.register('register_admin_menu_item')
# def help_menu_item(): return MenuItem("Help", reverse('help'), icon_name='help', order=10)


# @hooks.register('construct_page_chooser_queryset')
# def show_for_site(pages, request):
#     site = Site.find_for_request(request)
#     if not request.user.is_superuser:
#         descendable_pages = pages.filter(numchild__gt=0)
#         if not descendable_pages:
#             pages = pages.live().in_site(site).descendant_of(site.root_page, inclusive=False)
#         else:
#             pages = pages.live().in_site(site)
#     else:
#         pages = pages
#     return pages


@hooks.register('insert_editor_js')
def editor_js(): return format_html('\n <script src="https://cdnjs.cloudflare.com/ajax/libs/handsontable/6.2.2/handsontable.full.min.js"></script>')


@hooks.register('insert_editor_css')
def handsontable_editor_css(): return format_html('\n <link href="https://cdnjs.cloudflare.com/ajax/libs/handsontable/6.2.2/handsontable.full.min.css" rel="stylesheet">')


# @hooks.register('construct_page_listing_buttons')
# def remove_view_from_form_page(buttons, page, page_perms, is_parent=False, context=None):
#     if "Form" in page.get_verbose_name():
#         for button in buttons:
#             if button.label == "View live":
#                 del buttons[buttons.index(button)]

