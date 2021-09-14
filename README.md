# NAQT Tool

`naqtool.sh` is a very simple tool to assist with creating Anki flashcards from the You Gotta Know articles from the National Academic Quiz Tournaments website. Using the tool is a two-stage process. First, the `naqttool.sh fetch` command is used to download an article and parse it into a very basic text format. Then this text document is edited by hand into suitable flashcard items. Finally, flash cards can be created from the new document with `naqttool.sh anki`.

## Requirements

`naqttool.sh` depends on several external libraries: Requests, Beautiful Soup, and the Natural Language Toolkit. These should be installable with `pip install -r requirements.txt`. You may also need to download the Punkt language model for the NLTK. Instructions are here but the short version is `import nltk; nltk.download()` from a Python command prompt. You will also need the AnkiConnect add-on installed on your copy of Anki.

## Usage

### fetch
```
naqttool.sh fetch [-h] [--url URL] [--stdout] [-y] [--dest DEST]
                  [--cat CATEGORY] [--cloze] [--tag TAGS]
                  [PAGE]

positional arguments:
  PAGE            Page name on NAQT site

optional arguments:
  -h, --help      show this help message and exit
  --url URL       Explicit URL of page to parse
  --stdout        Send output to STDOUT
  -y              Overwrite existing files
  --dest DEST     Template filename
  --cat CATEGORY  Set category field for generated cards
  --cloze         Generate prompts as Cloze items
  --tag TAGS      Set tag(s) for generated cards
```

URLs from the You Gotta Know section on the NAQT are in the form

`https://www.naqt.com/you-gotta-know/western-european-rivers.html`

`PAGE` is just the last segment of the URL, without the `.html`. So you can download and create a template from the Western European Rivers YGK page with

```
naqttool.sh fetch western-european-rivers
```

By default, this will save the template as `western-european-rivers.txt` in the working directory. You can change this with the `--dest` option.

### anki

```
naqttool.sh anki [-h] TEMPLATE DECK

positional arguments:
  TEMPLATE    Template filename
  DECK        Anki deck name

optional arguments:
  -h, --help  show this help message and exit
```

`TEMPLATE` is the path to the template file; the `.txt` extension can be omitted if the file is in the current working directory. `DECK` is the name of the Anki deck to add the cards to; it will be created if it does not already exist. If the deck name is multiple words, be sure to put it in quotes.

### json

```
naqttool.sh json [-h] [--dest DEST] [--stdout] [-y] TEMPLATE

positional arguments:
  TEMPLATE     Template filename

optional arguments:
  -h, --help   show this help message and exit
  --dest DEST  JSON filename
  --stdout     Send output to STDOUT
  -y           Overwrite existing files
```

JSON export isn't really a core function; it is provided for testing and in case AnkiConnect isn't an option for some reason.

## Template Format

The template format is very simplistic. The parser splits the page into subject sections based on the bullets. Within each section, the paragraph is split into sentences. Broadly speaking, each sentence might potentially be the source of a flashcard, but that is by no means mandatory.

By way of an example, the command

`naqttool.sh fetch western-european-rivers -y --cat Rivers --tag geography,europe,naq`

produces a template `western-european-rivers.txt` that begins like this:

```
SOURCE: https://www.naqt.com/you-gotta-know/western-european-rivers.html
CATEGORY: Rivers
TAGS: geography, europe, naqt
===
SUBJECT: Rhine
---
TERM: Swiss Alps
TERM: Lake Constance
TERM: German-Swiss border
TERM: German-French border
PROMPT:  The Rhine begins in the Swiss Alps, passes through Lake Constance (in German, the Bodensee), flows west along the German-Swiss border, then turns north to form part of the German-French border.
EXTRA:
TAGS:
---
TERM: North Sea
PROMPT: The river then flows north and joins with the Meuse and Scheldt to enter the North Sea at a delta in the Netherlands.
EXTRA:
TAGS:
---
TERM: Basel
TERM: Strasbourg
TERM: Mainz
TERM: Bonn
TERM: Cologne
TERM: Rotterdam
TERM: Main
TERM: Mosel
TERM: Ruhr
PROMPT: Cities along its course include Basel, Strasbourg, Mainz, Bonn, Cologne, and Rotterdam, and tributaries include the Main, Mosel, and Ruhr.
EXTRA:
TAGS:
```

All the data in the header above the first `===` comes from the command line. The subject of each section is the phrase that is marked up as a `label` in the original HTML. The terms are the bolded phrases from each sentence (marked up as `ygk-term`).

To make a prompt into a question, edit the text however seems suitable and put a `*` in front of the `PROMPT` label. If you don't do anything else, the subject for the section will be treated as the correct response to the prompt. You can also put a `*` in front of one of the `TERM` labels to make that term the correct response. If you put a `*` in front of multiple terms, they will all be listed as answers. You can also add extra information to be shown on the back of the flashcard beside the 'EXTRA' label and/or a comma-separated list of additional tags by the `TAGS` label.

Here is an example of how the fragment above might be edited into a plausible template for a set of cards.

```
SOURCE: https://www.naqt.com/you-gotta-know/western-european-rivers.html
CATEGORY: Rivers
TAGS: geography, europe, naqt
===
SUBJECT: Rhine
---
TERM: Swiss Alps
TERM: Lake Constance
TERM: German-Swiss border
TERM: German-French border
*PROMPT:  This river begins in the Swiss Alps, passes through Lake Constance (in German, the Bodensee), flows west along the German-Swiss border, then turns north to form part of the German-French border.
EXTRA:
TAGS: rivers
---
*TERM: North Sea
*PROMPT: The Rhine then flows north and joins with the Meuse and Scheldt to enter the what seas at a delta in the Netherlands?
EXTRA:
TAGS: rivers,seas
---
*TERM: Basel
*TERM: Strasbourg
*TERM: Mainz
*TERM: Bonn
*TERM: Cologne
*TERM: Rotterdam
*TERM: Main
*TERM: Mosel
*TERM: Ruhr
PROMPT: These are the major cities along the Rhine.
EXTRA: This is a lousy question; it's just an example.
TAGS: rivers,cities
```

If you change the `PROMPT` label to `CLOZE` (and put a `*` in front of it), the card will be created as a Cloze item. Use normal Anki syntax within the `CLOZE` text to define the Cloze redactions.
```
SOURCE: https://www.naqt.com/you-gotta-know/western-european-rivers.html
CATEGORY: Rivers
TAGS: geography, europe, naqt
===
SUBJECT: Rhine
---
TERM: Swiss Alps
TERM: Lake Constance
TERM: German-Swiss border
TERM: German-French border
PROMPT:  The {{c1::Rhine}} begins in the {{c2::Swiss Alps}}, passes through {{c3::Lake Constance}} (in German, the Bodensee), flows west along the German-Swiss border, then turns north to form part of the German-French border.
EXTRA:
TAGS: rivers
```

If you run `naqttool.sh fetch` with the `--cloze` option, all of the labels will created as `CLOZE` instead of `PROMPT`, but you can mix and match by hand within the same template if you wish.

## Caveats

* This has only been tested on a few NAQT articles. It is possible that there are some that do not follow the normal conventions that will mess up the parsing.
* Essentially no error checking is done when cards are created. Be careful. Back stuff up.
* The code is sloppy. There are probably bugs.
