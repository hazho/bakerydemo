from django import template
from wagtail.images.models import Image
from django.utils.safestring import mark_safe


register = template.Library()


# Retrieves a single gallery item and returns a gallery of images
@register.inclusion_tag('tags/gallery.html', takes_context=True)
def gallery(context, gallery):
    images = Image.objects.filter(collection=gallery)
    return { 'images': images, 'request': context['request'], }

@register.filter(needs_autoescape=True)
def replace(value, arg, autoescape=True):
    if arg == "[but]": result = value.replace(arg, "<button class='button rt_button'>")
    elif arg == "[s.5]": result = value.replace(arg, "<span style='font-size: .5em ;line-height: .5'>")
    elif arg == "[s.8]": result = value.replace(arg, "<span style='font-size: .8em ;line-height: .8'>")
    elif arg == "[s1]": result = value.replace(arg, "<span style='font-size:1em ;line-height: 1'>")
    elif arg == "[s1.2]": result = value.replace(arg, "<span style='font-size:1.2em ;line-height: 1.2'>")
    elif arg == "[s1.4]": result = value.replace(arg, "<span style='font-size:1.4em ;line-height: 1.4'>")
    elif arg == "[s1.6]": result = value.replace(arg, "<span style='font-size:1.6em ;line-height: 1.6'>")
    elif arg == "[s1.8]": result = value.replace(arg, "<span style='font-size:1.8em ;line-height: 1.8'>")
    elif arg == "[s2]": result = value.replace(arg, "<span style='font-size:2em ;line-height: 2'>")
    elif arg == "[s2.2]": result = value.replace(arg, "<span style='font-size:2.2em ;line-height: 2.2'>")
    elif arg == "[s2.4]": result = value.replace(arg, "<span style='font-size:2.4em ;line-height: 2.4'>")
    elif arg == "[s2.6]": result = value.replace(arg, "<span style='font-size:2.6em ;line-height: 2.6'>")
    elif arg == "[s2.8]": result = value.replace(arg, "<span style='font-size:2.8em ;line-height: 2.8'>")
    elif arg == "[s3]": result = value.replace(arg, "<span style='font-size:3em ;line-height: 3'>")
    elif arg == "[s3.2]": result = value.replace(arg, "<span style='font-size:3.2em ;line-height: 3.2'>")
    elif arg == "[s3.4]": result = value.replace(arg, "<span style='font-size:3.4em ;line-height: 3.4'>")
    elif arg == "[s3.6]": result = value.replace(arg, "<span style='font-size:3.6em ;line-height: 3.6'>")
    elif arg == "[s3.8]": result = value.replace(arg, "<span style='font-size:3.8em ;line-height: 3.8'>")
    elif arg == "[s4]": result = value.replace(arg, "<span style='font-size:4em ;line-height: 4'>")
    elif arg == "[s4.2]": result = value.replace(arg, "<span style='font-size:4.2em ;line-height: 4.2'>")
    elif arg == "[s4.4]": result = value.replace(arg, "<span style='font-size:4.4em ;line-height: 4.4'>")
    elif arg == "[s4.6]": result = value.replace(arg, "<span style='font-size:4.6em ;line-height: 4.6'>")
    elif arg == "[s4.8]": result = value.replace(arg, "<span style='font-size:4.8em ;line-height: 4.8'>")
    elif arg == "[s5]": result = value.replace(arg, "<span style='font-size:5em ;line-height: 5'>")
    elif arg == "[sp]": result = value.replace(arg, "&nbsp; ")
    elif arg == "[nl]": result = value.replace(arg, "<br>")
    elif arg == "[w3]": result = value.replace(arg, "<span style='font-weight:300 !important;'>")
    elif arg == "[w5]": result = value.replace(arg, "<span style='font-weight:500 !important;'>")
    elif arg == "[w7]": result = value.replace(arg, "<span style='font-weight:700 !important;'>")
    elif arg == "[w9]": result = value.replace(arg, "<span style='font-weight:900 !important;'>")
    else: result = value

    return mark_safe(result)

@register.filter()
def to_string(value):
    return str(value)

@register.filter()
def to_int(value):
    return int(value)

@register.filter()
def ends_with(value, args):
    return value.endswith(args)


@register.filter() 
def has_group(user, group_name=None, ends_with=None, starts_with=None, has=None):
    
    if not ends_with and not starts_with and not has:
        # return user.groups.filter(name=group_name).exists() 
        return group_name in [ gn[0] for gn in user.groups.values_list('name')] 

    elif not ends_with and not starts_with:
        if has in group_name:
            grp_name = group_name 
        return user.groups.filter(name=grp_name).exists() 

    elif not ends_with and not has:
        grp_name = group_name.startswith(starts_with)
        return user.groups.filter(name=grp_name).exists() 

    elif not has and not starts_with:
        grp_name = group_name.endswith(ends_with)
        return user.groups.filter(name=grp_name).exists() 