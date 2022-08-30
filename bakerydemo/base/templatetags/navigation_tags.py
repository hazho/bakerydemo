from django.template import Library
from wagtail.models import Page, Site


register = Library()

@register.simple_tag(takes_context=True)
def get_site_host(context):
    if context['request']: 
        return Site.find_for_request(context['request'])
    else: return None


def has_menu_children(page):
    # https://tabo.pe/projects/django-treebeard/docs/4.0.1/api.html
    return (page.get_children().in_menu().exists() if page else False)


def has_children(page):
    # Generically allow index pages to list their children
    return (page.get_children().live().exists() if page else False)


def is_active(page, current_page): return (current_page.url_path.startswith(page.url_path) if current_page else False)


# Retrieves the top menu items
@register.inclusion_tag('tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    if parent:
        menuitems = parent.get_children().in_menu()
        for menuitem in menuitems:
            menuitem.show_dropdown = has_menu_children(menuitem)
            menuitem.active = (calling_page.url_path.startswith(menuitem.url_path)
                            if calling_page else False)
        parent.show_dropdown = False
        if parent.show_in_menus:
            menuitems = [parent] + list(menuitems)
    else: menuitems = []
    try:
        cont=context['request']
        
    except:
        cont=''
        pass
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'request': cont,
    }

@register.inclusion_tag('tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent, calling_page=None):
    if parent:
        menuitems_children = parent.get_children().in_menu()
        for menuitem in menuitems_children:
            menuitem.has_dropdown = has_menu_children(menuitem)
            menuitem.active = (calling_page.url_path.startswith(menuitem.url_path) if calling_page else False)
            menuitem.children = parent.get_children().in_menu()
    else: menuitems_children = []
    try:
        cont=context['request']
        
    except:
        cont=''
        pass
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        'request': cont,
    }

@register.inclusion_tag('tags/low_menu_children.html')
def low_menu_children(parent, calling_page=None):
    menuitems_grand_children = parent.get_children().in_menu()
    menuitems_grand_children = menuitems_grand_children.in_menu()
    for menuitem in menuitems_grand_children:
        menuitem.has_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url_path.startswith(menuitem.url_path) if calling_page else False)
        menuitem.children = parent.get_children().in_menu()
    return {
        'parent': parent,
        'menuitems_grand_children': menuitems_grand_children,
    }
