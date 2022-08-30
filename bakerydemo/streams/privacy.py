from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django import forms
from wagtail.blocks import ChooserBlock, StructBlock, ListBlock
from wagtail.admin.widgets import AdminChooser
from wagtail.blocks.field_block import PageChooserBlock

from .icon_blocks import IconBlock
from .emoji import PopularEmojiBlock
'''
You can extend the ChooserBlock to build your own chooser, but this gets complicated quickly as you need to also build a custom model chooser. The code below is NOT fully function but gives you an idea of what might be needed.

If you can use additional libraries, it might be worth looking into adding a Wagtail Generic Chooser, here are some quick results from Google (I have not used these).

https://github.com/wagtail/wagtail-generic-chooser
https://github.com/Naeka/wagtailmodelchooser/
https://github.com/neon-jungle/wagtailmodelchooser
https://github.com/springload/wagtailmodelchoosers
Remember that a chooser block is specific to StreamField implementations and chooser akin to a specific type of Django widget. You will need to build or get both if you want to use StreamFields for this implementation.

If you need to build your own I recommend to dig into the Wagtail internals to get an idea of how some other choosers are built.

ChooserBlock - https://github.com/wagtail/wagtail/blob/master/wagtail/core/blocks/field_block.py
AdminChooser - https://github.com/wagtail/wagtail/blob/master/wagtail/admin/widgets.py
POC (non functional) code example

as an example is PageChooserBlock
class PageChooserBlock(ChooserBlock):
    def __init__(self, page_type=None, can_choose_root=False, target_model=None, **kwargs):
        # We cannot simply deprecate 'target_model' in favour of 'page_type'
        # as it would force developers to update their old migrations.
        # Mapping the old 'target_model' to the new 'page_type' kwarg instead.
        if target_model:
            page_type = target_model

        if page_type:
            # Convert single string/model into a list
            if not isinstance(page_type, (list, tuple)):
                page_type = [page_type]
        else:
            page_type = []

        self.page_type = page_type
        self.can_choose_root = can_choose_root
        super().__init__(**kwargs)

    @cached_property
    def target_model(self):
        """
        Defines the model used by the base ChooserBlock for ID <-> instance
        conversions. If a single page type is specified in target_model,
        we can use that to get the more specific instance "for free"; otherwise
        use the generic Page model.
        """
        if len(self.target_models) == 1:
            return self.target_models[0]

        return resolve_model_string('wagtailcore.Page')

    @cached_property
    def target_models(self):
        target_models = []

        for target_model in self.page_type:
            target_models.append(
                resolve_model_string(target_model)
            )

        return target_models

    @cached_property
    def widget(self):
        from wagtail.admin.widgets import AdminPageChooser
        return AdminPageChooser(target_models=self.target_models,
                                can_choose_root=self.can_choose_root)

    def get_form_state(self, value):
        value_data = self.widget.get_value_data(value)
        if value_data is None:
            return None
        else:
            return {
                'id': value_data['id'],
                'parentId': value_data['parent_id'],
                'adminTitle': value_data['display_title'],
                'editUrl': value_data['edit_url'],
            }

    def render_basic(self, value, context=None):
        if value:
            return format_html('<a href="{0}">{1}</a>', value.url, value.title)
        else:
            return ''

    def deconstruct(self):
        name, args, kwargs = super().deconstruct()

        if 'target_model' in kwargs or 'page_type' in kwargs:
            target_models = []

            for target_model in self.target_models:
                opts = target_model._meta
                target_models.append(
                    '{}.{}'.format(opts.app_label, opts.object_name)
                )

            kwargs.pop('target_model', None)
            kwargs['page_type'] = target_models

        return name, args, kwargs

    class Meta:
        icon = "redirect"

in addition to block, it's better to create a db table for restrictions, example as pageprivacy:
class BaseViewRestriction(models.Model):
    NONE = 'none'
    PASSWORD = 'password'
    GROUPS = 'groups'
    LOGIN = 'login'

    RESTRICTION_CHOICES = (
        (NONE, _("Public")),
        (LOGIN, _("Private, accessible to logged-in users")),
        (PASSWORD, _("Private, accessible with the following password")),
        (GROUPS, _("Private, accessible to users in specific groups")),
    )

    restriction_type = models.CharField(
        max_length=20, choices=RESTRICTION_CHOICES)
    password = models.CharField(verbose_name=_('password'), max_length=255, blank=True)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True)

    def accept_request(self, request):
        if self.restriction_type == BaseViewRestriction.PASSWORD:
            passed_restrictions = request.session.get(self.passed_view_restrictions_session_key, [])
            if self.id not in passed_restrictions:
                return False

        elif self.restriction_type == BaseViewRestriction.LOGIN:
            if not request.user.is_authenticated:
                return False

        elif self.restriction_type == BaseViewRestriction.GROUPS:
            if not request.user.is_superuser:
                current_user_groups = request.user.groups.all()

                if not any(group in current_user_groups for group in self.groups.all()):
                    return False

        return True

    def mark_as_passed(self, request):
        """
        Update the session data in the request to mark the user as having passed this
        view restriction
        """
        has_existing_session = (settings.SESSION_COOKIE_NAME in request.COOKIES)
        passed_restrictions = request.session.setdefault(self.passed_view_restrictions_session_key, [])
        if self.id not in passed_restrictions:
            passed_restrictions.append(self.id)
            request.session[self.passed_view_restrictions_session_key] = passed_restrictions
        if not has_existing_session:
            # if this is a session we've created, set it to expire at the end
            # of the browser session
            request.session.set_expiry(0)

    class Meta:
        abstract = True
        verbose_name = _('view restriction')
        verbose_name_plural = _('view restrictions')

    def save(self, user=None, specific_instance=None, **kwargs):
        """
        Custom save handler to include logging.
        :param user: the user add/updating the view restriction
        :param specific_instance: the specific model instance the restriction applies to
        """
        is_new = self.id is None
        super().save(**kwargs)

        if specific_instance:
            PageLogEntry.objects.log_action(
                instance=specific_instance,
                action='wagtail.view_restriction.create' if is_new else 'wagtail.view_restriction.edit',
                user=user,
                data={
                    'restriction': {
                        'type': self.restriction_type,
                        'title': force_str(dict(self.RESTRICTION_CHOICES).get(self.restriction_type))
                    }
                }
            )

    def delete(self, user=None, specific_instance=None, **kwargs):
        """
        Custom delete handler to aid in logging
        :param user: the user removing the view restriction
        :param specific_instance: the specific model instance the restriction applies to
        """
        if specific_instance:
            PageLogEntry.objects.log_action(
                instance=specific_instance,
                action='wagtail.view_restriction.delete',
                user=user,
                data={
                    'restriction': {
                        'type': self.restriction_type,
                        'title': force_str(dict(self.RESTRICTION_CHOICES).get(self.restriction_type))
                    }
                }
            )
        return super().delete(**kwargs)

'''
class ModelChooser(AdminChooser):
    # ... implement __init__ etc
    pass


class AuthGroupBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from django.contrib.auth.models import Group
        return Group

    @cached_property
    def widget(self):
        return ModelChooser(self.target_model)


class PrivacyBlock(StructBlock):
    visible_groups = ListBlock(
        AuthGroupBlock(
            label='Limit view to groups',
            required=False,
            blank=True
        )
    )

    class Meta:
        icon = "user"


# class PrivacyBlock(StructBlock):
#     visible_groups = ListBlock(
#         SnippetChooserBlock(
#             Group,
#             label='Limit view to groups',
#             required=False,
#             blank=True
#         )
#     )

#     class Meta:
#         icon = "user"
