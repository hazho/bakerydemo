# Generated by Django 4.0.7 on 2022-08-30 05:25

from django.conf import settings
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.contrib.forms.models
import wagtail.fields
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('wagtailcore', '0069_log_entry_jsonfield'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', wagtail.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'Footer Text',
            },
        ),
        migrations.CreateModel(
            name='RootPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Reseller Page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HHPage',
            fields=[
                ('rootpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.rootpage')),
                ('nav_title', models.CharField(blank=True, help_text="if not used, the page's title will be used in the nav-bar menu", max_length=45, null=True, verbose_name='Custom title for main nav-bar menu')),
                ('clickablity', models.BooleanField(blank=True, default=True, help_text='If it is not checked, the page contents will NOT be shown to visitors and the menu title will NOT be clickable', null=True, verbose_name='Clickable/Visitable?')),
                ('show_share_to', models.BooleanField(blank=True, help_text='to Show the (share to) button on this page', null=True, verbose_name='Show (Share to) button')),
                ('no_se_index', models.BooleanField(blank=True, help_text='Use this to control on indexing this page or not (in search engines, like: bing, google or ... any other one)', null=True, verbose_name='No SE Indexing (for this page)')),
                ('custom_metadata', models.TextField(blank=True, help_text='add as much elements as you need ', null=True)),
                ('maino', wagtail.fields.StreamField([], blank=True, null=True, verbose_name="Main section's Grid(Rows & Columns)")),
                ('aside', wagtail.fields.StreamField([], blank=True, null=True, verbose_name='')),
            ],
            options={
                'abstract': False,
            },
            bases=('base.rootpage',),
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=254, verbose_name='First name')),
                ('last_name', models.CharField(max_length=254, verbose_name='Last name')),
                ('job_title', models.CharField(max_length=254, verbose_name='Job title')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='HHFormSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_data', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='submit time')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'form submission',
                'verbose_name_plural': 'form submissions',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('to_address', models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, validators=[wagtail.contrib.forms.models.validate_to_address], verbose_name='to address')),
                ('from_address', models.EmailField(blank=True, max_length=255, verbose_name='from address')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name='subject')),
                ('nav_title', models.CharField(blank=True, help_text="if not used, the page's title will be used in the nav-bar menu", max_length=45, null=True, verbose_name='Custom title for main nav-bar menu')),
                ('no_se_index', models.BooleanField(blank=True, help_text='Use this to control on indexing this page or not (in search engines, like: bing, google or ... any other one)', null=True, verbose_name='No SE Indexing')),
                ('custom_metadata', models.TextField(blank=True, help_text='add as much elements as you need ', null=True)),
                ('thank_you_text', models.CharField(blank=True, max_length=200)),
                ('more_submissions', models.BooleanField(blank=True, default=True, help_text='uncheck this if you want to prevent a user from submitting more than once (Users should be registered))', null=True, verbose_name='Can a User Submit more than Once?')),
                ('uploaded_image_collection', models.ForeignKey(blank=True, help_text='collection for uploaded image (if that field had been used), Default: Root', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailcore.collection')),
            ],
            options={
                'verbose_name': 'Form',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('clean_name', models.CharField(blank=True, default='', help_text='Safe name of the form field, the label converted to ascii_snake_case', max_length=255, verbose_name='name')),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.TextField(blank=True, help_text='Comma or new line separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices')),
                ('default_value', models.TextField(blank=True, help_text='Default value. Comma or new line separated values supported for checkboxes.', verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time'), ('hidden', 'Hidden field'), ('image', 'Upload Image')], max_length=16, verbose_name='field type')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='base.formpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('hhpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.hhpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('base.hhpage',),
        ),
        migrations.CreateModel(
            name='SpecialPage',
            fields=[
                ('hhpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.hhpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('base.hhpage',),
        ),
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('hhpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.hhpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('base.hhpage',),
        ),
    ]
