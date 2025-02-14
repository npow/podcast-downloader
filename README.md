# Podcast Downloader

![GitHub](https://img.shields.io/github/license/dplocki/podcast-downloader)
![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fdplocki%2Fpodcast-downloader%2Fbadge%3Fref%3Dmaster&style=flat)
![PyPI](https://img.shields.io/pypi/v/podcast-downloader)

The Python module for downloading files from given RSS feeds.
It is not using database of any sort. It require configuration file.

The script is analyzing the directory where it put the previously downloaded files.
It is compering the last added file with the rss feed, finding the missing ones, and downloading them.

As name suggested, the script is designed for podcasts. The files searched by default are mp3.

## Setup

### Installation from PyPI

```bash
pip install podcast_downloader
```

## Running the script

After installation, the script is called as Python module.

```bash
python -m podcast_downloader
```

### In action

Using the [example above](#example), the result will be:

```log
[2020-06-16 19:54:35] Loading configuration (from file: "~/.podcast_downloader_config.json")
[2020-06-16 19:54:35] Checking "The Skeptic Guide"
[2020-06-16 19:54:35] Last downloaded file "skepticast2020-06-13.mp3"
[2020-06-16 19:54:39] The Skeptic Guide: Nothing new
[2020-06-16 19:54:39] ------------------------------
[2020-06-16 19:54:39] Finished
```

## Configuration

### The configuration file

The configuration file is placed in home directory.

The name: `.podcast_downloader_config.json`. The file is format in [JSON](https://en.wikipedia.org/wiki/JSON).

### The settings hierarchy

The script will replace default values by read from configuration file.
Those will be cover by all values given by command line.

```
 command line parameters > configuration file > default values
```

### The main options

| Property             | Type       | Required | Default                  | Note |
|:---------------------|:----------:|:--------:|:------------------------:|:-----|
| `downloads_limit`    | number     | no       | infinity                 |      |
| `if_directory_empty` | string     | no       | download_last            | See [In case of empty directory](#in-case-of-empty-directory) |
| `podcast_extensions` | key-value  | no       | `{".mp3": "audio/mpeg"}` | The file filter |
| `podcasts`           | subsection | yes      | `[]`                     | See [Podcasts sub category](#podcasts-sub-category) |

### Podcasts sub category

`Podcasts` is the part of configuration file where you provide the array of objects with fallowing content:

| Property             | Type      | Required | Default                        | Note |
|:---------------------|:---------:|:--------:|:------------------------------:|:-----|
| `name`               | string    | yes      | -                              | The name of channel (used in logger) |
| `rss_link`           | string    | yes      | -                              | The URL of RSS channel |
| `path`               | string    | yes      | -                              | The path to directory, for podcast files |
| `file_name_template` | string    | no       | `%file_name%.%file_extension%` | The template for the downloaded files, more 
| `disable`            | boolean   | no       | `false`                        | This podcast will be ignored |
| `podcast_extensions` | key-value | no       | `{".mp3": "audio/mpeg"}`       | The file filter |
| `if_directory_empty` | string    | no       | `download_last`                | See [In case of empty directory](#in-case-of-empty-directory) |
| `require_date`       | boolean   | no       | `false`                        | **Deprecated** Is date of podcast should be added into name of file - use the `file_name_template`: `[%publish_date%] %file_name%.%file_extension%"` |

### An example of configuration file

```json
{
    "if_directory_empty": "download_from_4_days",
    "podcasts": [
        {
            "name": "The Skeptic Guide",
            "rss_link": "http://www.theskepticsguide.org/feed/rss.aspx",
            "path": "~/podcasts/SGTTU"
        }
    ]
}
```

## Script arguments

The script accept following command line arguments:

| Short version | Long name              | Parameter           | Default         | Note |
|:--------------|:-----------------------|:-------------------:|:---------------:|:-----|
|               | `--downloads_limit`    | number              | infinity        | The maximum number of downloaded mp3 files |
|               | `--if_directory_empty` | string              | `download_last` | The general approach on empty directory' |

## Adding date to file name

If RSS channel doesn't have single and constant name convention, it may causing the script to working incorrectly. The solution is force files to have common and meaningful prefix. The script is able to adding the date on beginning of downloaded file name.

Use [File name template](#file-name-template) and option `%publish_date%`.

## File name template

Use to change the name of downloaded file after its downloading.

Default value (the `%file_name%.%file_extension%`) will simple save up the file as it was uploaded by original creator. The file name and its extension is taken from the link to podcast file.

Template values:

| Name               | Notes |
|:-------------------|:------|
| `%file_name%`      | The file name taken from link, without extension |
| `%file_extension%` | The extension for the file, taken from link |
| `%publish_date%`   | The publish date of the RSS entry, in format `YEARMMDD` |
| `%title%`          | The title of the RSS entry |

Examples:

* `[%publish_date%] %file_name%.%file_extension%`
* `[%publish_date%] %title%.%file_extension%`

## File types filter

Podcasts are mostly stored as `*.mp3` files. By default Podcast Downloader will look just for them.

If your podcast support other types of media files, you can precised your own podcast file filter, by providing extension for the file (like `.mp3`), and type of link in RSS feed itself (for `mp3` it is `audio/mpeg`).

If you don't know the type of the file, you can check the RSS file. Seek for `enclosure` tags, should looks like this:

```xml
    <enclosure
        url="https://an.apple.supporter.page/podcast/episode23.m4a"
        length="14527149"
        type="audio/x-m4a" />
```

Notes: the dot on the file extension is require.

### Example

```json
  "podcast_extensions": {
    ".mp3": "audio/mpeg",
    ".m4a": "audio/x-m4a"
  }
```

## In case of empty directory

If a directory for podcast is empty, the script needs to recognize what to do. Due to lack of database, you can:

* [download all episodes from feed](#download-all-from-feed)
* [download only the last episode](#only-last)
* [download all new episode from last n days](#download-all-from-n-days)
* [download all new episode since day after, the last episode should appear](#download-all-episode-since-last-excepted)

### Download all from feed

The script will download all episodes from the feed.

Set by `download_all_from_feed`.

### Only last

The script will download only the last episode from the feed.
It is a good approach when you wish to start listening the podcast.
It is also default approach of the script.

Set by `download_last`.

### Download all from n days

The script will download all episodes which appear in last *n* days. I can be use when you are downloading on regular schedule.
The *n* number is given within the setup value: `download_from_n_days`. For example: `download_from_3_days` means download all episodes from last 3 days.

### Download all episode since last excepted

The script will download all episodes which appear after the day of release of last episode.

The *n* number is the day of the normal episode.
You can provide here week days as word (size of the letters is ignored)

| Full week day | Shorten name |
|:--------------|:-------------|
| Monday        | Mon          |
| Tuesday       | Tues         |
| Wednesday     | Weds         |
| Thursday      | Thurs        |
| Friday        | Fri          |
| Saturday      | Sat          |
| Sunday        | Sun          |

You can provide the number, it will means the day of the month. The script accepts only number from 1 to 28.

Set by `download_from_`.

Examples:

| Example value          | Meaning |
|------------------------|---------|
| `download_from_monday` | New episodes appear in Monday. The script will download all episodes since last Tuesday (including it) |
| `download_from_Fri`    | New episodes appear in Friday. The script will download all episodes since last Saturday (including it) |
| `download_from_12`     | New episodes appear each 12th of month. The script will download all episodes since 13 month before |

## The analyze of the RSS feed

The script is look through all the `items` nodes in RSS file. The `item` node can contain the `enclosure` node. Those nodes are used to passing the files. According to the convention the single `item` should contain only one `enclosure`, but script (as [the library used](https://pypi.org/project/feedparser/) under it) can handle the multiple files attached into podcast `item`.
