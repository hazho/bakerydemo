from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel,FieldRowPanel,InlinePanel,MultiFieldPanel,FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormSubmission, AbstractFormField, FORM_FIELD_CHOICES
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Collection, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from bakerydemo.streams.blocks import AsideBaseStreamBlock, ColumnsBlock


@register_snippet
class People(index.Indexed, ClusterableModel):
    """
    A Django model to store People objects.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/base/people/)
    `People` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """

    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("first_name", classname="col6"),
                        FieldPanel("last_name", classname="col6"),
                    ]
                )
            ],
            "Name",
        ),
        FieldPanel("job_title"),
        FieldPanel("image"),
    ]

    search_fields = [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image.get_rendition("fill-50x50").img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ""

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"


@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """

    body = RichTextField()

    panels = [
        FieldPanel("body"),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = "Footer Text"



class RootPage(Page):
    parent_page_types = ['wagtailcore.Page']
    subpage_types  = ['base.HomePage']
    is_creatable=True

    @classmethod
    def can_create_at(cls, parent): return super(RootPage, cls).can_create_at(parent)

    class Meta:
        verbose_name='Reseller Page'

SE_INDEXING_CHOICES = ((True, "Don't Index"), (False, 'Index (Default)'))

class HHPage(RootPage):
    nav_title=models.CharField(max_length=45, verbose_name="Custom title for main nav-bar menu", null=True, blank=True, help_text="if not used, the page's title will be used in the nav-bar menu")
    clickablity=models.BooleanField(default=True,verbose_name="Clickable/Visitable?", null=True, blank=True, help_text="If it is not checked, the page contents will NOT be shown to visitors and the menu title will NOT be clickable")
    show_share_to=models.BooleanField(verbose_name="Show (Share to) button", null=True, blank=True, help_text="to Show the (share to) button on this page")
    no_se_index=models.BooleanField(verbose_name="No SE Indexing (for this page)", null=True, blank=True, help_text="Use this to control on indexing this page or not (in search engines, like: bing, google or ... any other one)")
    custom_metadata=models.TextField(blank=True, null=True, help_text="add as much elements as you need ")
    maino=StreamField([("multi_columns_row", ColumnsBlock(required=False, blank=True, null=True)),], null=True, blank=True, verbose_name="Main section's Grid(Rows & Columns)")
    aside=StreamField(AsideBaseStreamBlock(required=False, blank=True, null=True), verbose_name="", blank=True, null=True)

    # show_in_menus = Page.show_in_menus.help_text=_("Whether a link to this page will appear in top navbar menu"))
    content_panels=Page.content_panels + [
        MultiFieldPanel([
        FieldPanel('show_in_menus',classname="nav_menu_control col3"),
        FieldPanel('clickablity',classname="nav_menu_link col3", widget=forms.CheckboxInput()),
        FieldPanel('nav_title',classname="nav_menu_title col6"),
        ],_('For main nav bar Menu '), classname="collapsible"),
        StreamFieldPanel('maino',classname="main_section"),
    ]
    aside_panels = [StreamFieldPanel('aside',classname="aside_section"),]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
            FieldPanel('no_se_index',classname="no_se_index", widget=forms.CheckboxInput()),
            FieldPanel('custom_metadata'),
            FieldPanel('show_share_to', widget=forms.CheckboxInput()),
        ], _('For search engines and other METAs'), classname="collapsible"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Main Section'),
            ObjectList(aside_panels, heading="Right Sidebar Section"),
            ObjectList(promote_panels, heading='SEO'),
            ObjectList(Page.settings_panels, heading='Other Settings'),
        ]
    )
    is_creatable=False 
 
    def get_admin_display_title(self): return f"{self.title} ({self.slug}) Page"

    def __str__(self): 
        if self.nav_title is None:
            return f"{self.title} - {self.slug}"
        return f"{self.nav_title} - {self.slug}"


class HomePage(HHPage):
  parent_page_types = ['RootPage']
  subpage_types  = ['base.StandardPage','base.FormPage']
  is_creatable=True


class StandardPage(HHPage):
  is_creatable=True
  parent_page_types = ['HomePage', 'StandardPage']
  subpage_types  = ['base.StandardPage','base.FormPage']


class SpecialPage(HHPage):
  is_creatable=False # TODO: except the special users from this condition 
  parent_page_types = ['HomePage']


class HHFormBuilder(FormBuilder):
    def create_image_field(self, field, options): return WagtailImageField(**options)


class HHFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    def get_data(self):
        form_data=super().get_data()
        form_data["submitted_by"] = self.user
        # print(form_data)
        # import json
        # json_dict = json.loads(form_data)
        return form_data

    def __str__(self): return f'{self.form_data}'
    # pass


class HHSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if not self.is_export:
            # generate a list of field types, the first being the injected 'submission date'
            field_types=['submission_date'] + ['user'] + [field.field_type for field in self.form_page.get_form_fields()]
            data_rows=context['data_rows']
            ImageModel=get_image_model()
            for data_row in data_rows:
                fields=data_row['fields']
                for idx, (value, field_type) in enumerate(zip(fields, field_types)):
                    if field_type == 'image' and value:
                        image=ImageModel.objects.get(pk=value)
                        rendition=image.get_rendition('fill-60x37|jpegquality-30')
                        preview_url=rendition.url
                        url=reverse('wagtailimages:edit', args=(image.id,))
                        # build up a link to the image, using the image title & id
                        fields[idx]=format_html(
                            "<a href='{}'><img alt='Uploaded image - {}' src='{}' /><br>{}... ({})</a>",
                            url,image.title,preview_url,image.title[:7],value
                        )
        return context


class FormPage(AbstractEmailForm):
    subpage_types=[]
    parent_page_types = ['base.HomePage', 'StandardPage']
    is_creatable=True
    nav_title=models.CharField(max_length=45, verbose_name="Custom title for main nav-bar menu", null=True, blank=True, help_text="if not used, the page's title will be used in the nav-bar menu")
    no_se_index=models.BooleanField(verbose_name="No SE Indexing", null=True, blank=True, help_text="Use this to control on indexing this page or not (in search engines, like: bing, google or ... any other one)")
    custom_metadata=models.TextField(blank=True, null=True, help_text="add as much elements as you need ")

    form_builder=HHFormBuilder
    # submissions_list_view_class=HHSubmissionsListView
    uploaded_image_collection=models.ForeignKey('wagtailcore.Collection',null=True,blank=True,on_delete=models.SET_NULL,help_text=_('collection for uploaded image (if that field had been used), Default: Root') ,)
    thank_you_text=models.CharField(max_length=200, blank=True)
    more_submissions=models.BooleanField(verbose_name="Can a User Submit more than Once?",default=True, null=True, blank=True, help_text="uncheck this if you want to prevent a user from submitting more than once (Users should be registered))")

    content_panels=Page.content_panels + [
        FieldPanel('more_submissions', classname="col4"),
        FieldPanel('subject', classname="full"),
        FieldRowPanel([FieldPanel('from_address', classname="col6"),FieldPanel('to_address', classname="col6"),]),
        FieldPanel('thank_you_text', classname="full"),
    ]
    form_fields_panels = [
        MultiFieldPanel([InlinePanel('form_fields', label="Field", classname="collapsible" ),FieldPanel('uploaded_image_collection', classname="col6"),],heading="Fields", classname=""),
    ]
    
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
            FieldPanel('custom_metadata')
        ], _('For search engines and other METAs'), classname="collapsible"),
    ]
    
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Main Section'),
            ObjectList(form_fields_panels, heading="Form Fields Section"),
            ObjectList(promote_panels, heading='SEO'),
            ObjectList(Page.settings_panels, heading='Other Settings'),
        ]
    )
    
    def get_admin_display_title(self): return f"{self.title} ({self.slug}) Form"

    def get_uploaded_image_collection(self):
        """ Returns a Wagtail Collection, using this form's saved value if present, otherwise returns the 'Root' Collection. """
        collection=self.uploaded_image_collection
        return collection or Collection.get_first_root_node()
    
    @staticmethod
    def get_image_title(filename): return filename
    def get_submission_class(self): return HHFormSubmission

    def process_form_submission(self, form):
        """ Processes the form submission, if an Image upload is found, pull out the files data, create an actual Wgtail Image and reference it in the stored form response. """
        from django.contrib.auth import get_user_model
        user = get_user_model()
        cleaned_data=form.cleaned_data
        for name, field in form.fields.items():
            if isinstance(field, WagtailImageField):
                image_file_data=cleaned_data[name]
                if image_file_data:
                    ImageModel=get_image_model()
                    kwargs={'file': cleaned_data[name],
                        'title': self.get_image_title(cleaned_data[name].name),
                        'collection': self.get_uploaded_image_collection(),}
                    if form.user and not form.user.is_anonymous: kwargs['uploaded_by_user']=form.user
                    else: kwargs['uploaded_by_user']=user.objects.get(id=8)
                    image=ImageModel(**kwargs)
                    image.save()
                    # saving the image id (alternatively we can store a path to the image via image.get_rendition)
                    cleaned_data.update({name: image.pk})
                else:
                    # remove the value from the data
                    del cleaned_data[name]
        submission=self.get_submission_class().objects.create(form_data=cleaned_data,page=self, user=form.user)
        # important: if extending AbstractEmailForm, email logic must be re-added here
        if self.to_address: self.send_mail(form)
        return submission

    def get_form_fields(self):
        fields = list(super().get_form_fields())
        # append instances of FormField (not actually stored in the db)
        # field_type can only be one of the following:
        # 'singleline', 'multiline', 'email', 'number', 'url', 'checkbox', 'checkboxes', 'dropdown', 'multiselect', 'radio', 'date', 'datetime', 'hidden'
        # Important: Label MUST be unique in each form
        # `insert(0` will prepend these items, so here ID will be first

        fields.insert(1000, FormField(
            label='I am not a Human',
            field_type='singleline',
            required=False,
            help_text="Only fill this field if you are not a human"))
        return fields

    class Meta:
        verbose_name="Form"
        # verbose_name_plurer="Forms"
    

class FormField(AbstractFormField):
    field_type=models.CharField(verbose_name='field type',max_length=16,choices=list(FORM_FIELD_CHOICES) + [('image', 'Upload Image'), ] ) # todo  ('user', 'submited by'), 
    page=ParentalKey('base.FormPage', related_name='form_fields', on_delete=models.CASCADE)
