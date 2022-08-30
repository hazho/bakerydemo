import json
import logging

from bs4 import BeautifulSoup
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from wagtail.admin.rich_text.converters.contentstate import \
    ContentstateConverter
from wagtail.blocks import (ListBlock, RichTextBlock, StreamBlock,
                                 StructBlock)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import PageRevision, get_page_models
from wagtail.rich_text import features

logger = logging.getLogger(__name__)
converter = ContentstateConverter(features.get_default_features())


def fix_common_html_problems(value):
  soup = BeautifulSoup(value, "html.parser")
  for li in soup.findAll("li"):
    # First, let's find all <li> elements without a parent <ul>
    parent = li.parent
    if parent.name != "ul":
      # Add a parent <ul>
      ul = soup.new_tag("ul")

      current_element = li.next_sibling
      li.wrap(ul)
      while current_element and current_element.name == "li":
        # If there's multiple <li> in succession, let's put them under
        # the same parent
        li = current_element
        current_element = current_element.next_sibling
        ul.append(li.extract())

    for el in soup.findAll(["embed", "ul", "p"]):
      # This is another common problem in the hallo-created html
      # Find any embeds, uls, p tags wrapped in inline elements
      parents = el.find_parents(["a", "b", "strong", "i", "em"])
      if parents:
        # Extract the block level element as a sibling of the last offending parent
        parents[-1].insert_after(el.extract())
        for parent in parents:
          # If the offending tags are now empty, remove them.
          if not parent.contents:
            parent.unwrap()
    return str(soup)


def update_html_if_unreadable(value):
  try:
    # Test if Wagtail can convert the html itself without errors
    converter.from_database_format(value)
    return value
  except (AttributeError, AssertionError):
    # If not, we will need to try and rewrite it.
    # We can't fix all malformed html, but we can catch common
    # problems in the hallo.js generated html
    new_content = fix_common_html_problems(value)

    # Let's check if Draftail can open them now
    # If not, this will throw an exception
    converter.from_database_format(new_content)
    return new_content


def fix_rich_text_block(block, stream):
  """Rewrites a base block to Draftail-compatible format"""
  if isinstance(block, RichTextBlock):
    new_value = update_html_if_unreadable(stream)
    return new_value
  return stream


def fix_rich_text_blocks(stream_block, value):
  """Loops over list-of-dicts formatted StreamField (stream) to update any unreadable html to Draftail-readable format"""
  stream = json.loads(value)
  stream_block_handler = get_block_handler(stream_block)
  updated_stream = stream_block_handler.map_over_json(stream, fix_rich_text_block)
  return json.dumps(updated_stream, cls=DjangoJSONEncoder)


class BaseBlockHandler:
  def __init__(self, block):
    self.block = block

  def map_over_json(self, stream, func):
    """
    Apply a function, func, to each of the base blocks' values (ie not Struct, List, Stream) of a StreamField in
    list of dicts (imported json) format and return a copy of the rewritten streamfield.
    """
    value = func(self.block, stream)
    return value


class ListBlockHandler(BaseBlockHandler):
  def map_over_json(self, stream, func):
    updated_stream = []
    new_block = self.block.child_block
    new_block_handler = get_block_handler(new_block)
    for element in stream:
      new_value = new_block_handler.map_over_json(element, func)
      updated_stream.append(new_value)
    return updated_stream


class StreamBlockHandler(BaseBlockHandler):
  def map_over_json(self, stream, func):
    updated_stream = []
    for element in stream:
      new_block = self.block.child_blocks.get(element["type"])
      new_block_handler = get_block_handler(new_block)
      new_stream = element["value"]
      new_value = new_block_handler.map_over_json(new_stream, func)
      new_block_value = {"type": element["type"], "value": new_value}
      block_id = element.get("id")
      if block_id:
        new_block_value['id'] = block_id
      updated_stream.append(new_block_value)
    return updated_stream


class StructBlockHandler(BaseBlockHandler):
  def map_over_json(self, stream, func):
    updated_stream = {}
    for key in stream:
      new_block = self.block.child_blocks.get(key)
      new_block_handler = get_block_handler(new_block)
      new_stream = stream[key]
      new_value = new_block_handler.map_over_json(new_stream, func)
      updated_stream[key] = new_value
    return updated_stream


def get_block_handler(block):
  # find the handler class for the most specific class in the block's inheritance tree
  for block_class in type(block).__mro__:
    if block_class in HANDLERS_BY_BLOCK_CLASS:
      handler_class = HANDLERS_BY_BLOCK_CLASS[block_class]
      return handler_class(block)
  return BaseBlockHandler(block)


HANDLERS_BY_BLOCK_CLASS = {
  ListBlock: ListBlockHandler,
  StreamBlock: StreamBlockHandler,
  StructBlock: StructBlockHandler,
}


class Command(BaseCommand):
  help = "Try to convert rich text fields and blocks to Draftail-readable HTML"

  def add_arguments(self, parser):
    parser.add_argument(
      "--latest-only",
      action="store_true",
      help="Rewrite only the latest revision for each page",
    )

  def handle(self, *args, **options):
    latest_only = options.get("latest_only")

    classes = get_page_models()
    contenttypes = ContentType.objects.get_for_models(*classes)

    for klass, contenttype in contenttypes.items():
      fields = [
        field
        for field in klass._meta.get_fields()
        if isinstance(field, RichTextField) or isinstance(field, StreamField)
      ]

      if not fields:
        continue

      revisions = PageRevision.objects.filter(page__content_type=contenttype)
      if latest_only:
        revisions = revisions.order_by("page", "-created_at").distinct("page")

      pages = klass.objects.exclude(
        pk__in=revisions.values_list("page", flat=True)
      )
      # We only need to rewrite pages with no revisions - pages with revisions will load the latest
      # revision in the Wagtail Admin instead

      revisions_to_update = []

      for revision in revisions:
        content = json.loads(revision.content_json)
        updated = False
        for field in fields:
          value = content.get(field.name, "")
          if not value:
              continue

          new_value = value

          try:
            if isinstance(field, RichTextField):
              new_value = update_html_if_unreadable(value)
            elif isinstance(field, StreamField):
              new_value = fix_rich_text_blocks(field.stream_block, value)
          except (AttributeError, AssertionError):
            logger.exception(
                f"Failed to rewrite field {field.name} on revision {revision.pk} in a Draftail-parseable format"
            )

          if new_value != value:
            updated = True
            content[field.name] = new_value
        if updated:
          revision.content_json = json.dumps(content, cls=DjangoJSONEncoder)
          revisions_to_update.append(revision)

      pages_to_update = []

      for page in pages:
        updated = False
        for field in fields:
          value = field.get_prep_value(field.value_from_object(page))
          if not value:
            continue

          new_value = value

          try:
            if isinstance(field, RichTextField):
              new_value = update_html_if_unreadable(value)
            elif isinstance(field, StreamField):
              new_value = fix_rich_text_blocks(field.stream_block, value)
          except (AttributeError, AssertionError):
              message = f"Failed to rewrite field {field.name} on page {page.pk} in a Draftail-parseable format"
              logger.exception(
                message
              )
              print(message)

          if new_value != value:
            updated = True
            setattr(page, field.name, new_value)
        if updated:
          pages_to_update.append(page)

      if pages_to_update or revisions_to_update:
        PageRevision.objects.bulk_update(revisions_to_update, ["content_json"])
        klass.objects.bulk_update(pages, [field.name for field in fields])
        print(
          f"{klass.__name__}: {len(pages_to_update)} pages and {len(revisions_to_update)} revisions updated"
        )