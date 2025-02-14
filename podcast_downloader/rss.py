import re
import time
from dataclasses import dataclass
from functools import partial
from itertools import takewhile, islice
from typing import Callable, Generator, Iterator, List
import unicodedata

import feedparser


FILE_NAME_CHARACTER_LIMIT = 255


@dataclass
class RSSEntity:
    published_date: time.struct_time
    title: str
    type: str
    link: str


def link_to_file_name_with_extension(link: str) -> str:
    if link.find("?") > 0:
        link = link.rpartition("?")[0]

    return link.rpartition("/")[-1].lower()


def link_to_file_name(link: str) -> str:
    link = link_to_file_name_with_extension(link)
    if link.find(".") > 0:
        link = link.rpartition(".")[0]

    return link


def link_to_extension(link: str) -> str:
    link = link_to_file_name_with_extension(link)
    if link.find(".") > 0:
        return link.rpartition(".")[-1]

    return ""


def str_to_filename(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[\u0000-\u001F\u007F\*/:<>\?\\\|]", " ", value)

    return value.strip()[:FILE_NAME_CHARACTER_LIMIT]


def file_template_to_file_name(name_template: str, entity: RSSEntity) -> str:
    return (
        name_template.replace("%file_name%", link_to_file_name(entity.link))
        .replace("%publish_date%", time.strftime("%Y%m%d", entity.published_date))
        .replace("%file_extension%", link_to_extension(entity.link))
        .replace("%title%", str_to_filename(entity.title))
    )


def get_raw_rss_entries_from_web(
    rss_link: str,
) -> Generator[feedparser.FeedParserDict, None, None]:
    yield from feedparser.parse(rss_link).entries


def flatten_rss_links_data(
    source: Generator[feedparser.FeedParserDict, None, None]
) -> Generator[RSSEntity, None, None]:
    return (
        RSSEntity(rss_entry.published_parsed, rss_entry.title, link.type, link.href)
        for rss_entry in source
        for link in rss_entry.links
    )


def build_only_allowed_filter_for_link_data(
    allowed_types: List[str],
) -> Callable[[RSSEntity], bool]:
    return lambda link_data: link_data.type in allowed_types


def build_only_new_entities(
    to_name_function: Callable[[RSSEntity], str]
) -> Callable[[str, List[RSSEntity]], Generator[RSSEntity, None, None]]:
    return lambda from_file, raw_rss_entries: takewhile(
        lambda rss_entity: to_name_function(rss_entity) != from_file, raw_rss_entries
    )


def only_last_entity(raw_rss_entries: Iterator[RSSEntity]) -> Iterator[RSSEntity]:
    return islice(raw_rss_entries, 1)


def is_entity_newer(from_date: time.struct_time, entity: RSSEntity) -> bool:
    return entity.published_date[:3] >= from_date[:3]


def only_entities_from_date(from_date: time.struct_time) -> Callable[[RSSEntity], bool]:
    return partial(filter, partial(is_entity_newer, from_date))
