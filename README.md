# fileparse
[![Build Status](https://travis-ci.org/tobiasli/fileparse.svg?branch=master)](https://travis-ci.org/tobiasli/fileparse)<br/>
[![Coverage Status](https://coveralls.io/repos/tobiasli/fileparse/badge.svg?branch=master&service=github)](https://coveralls.io/github/tobiasli/fileparse?branch=master)<br/>
[![PyPI version](https://badge.fury.io/py/fileparse-tobiasli.svg)](https://badge.fury.io/py/fileparse-tobiasli)<br/>

`fileparse` is a package for reading the contents of a file and populating a data model with the information found.

## Install

```
pip install fileparse-tobiasli
```

## Usage

Say you have som text, and you have an idea of the structure of this text.

```python
nested_text = """# This is a title.
This is contents.
And some more.

## This is a subtitle.
with subtitle contents.

# This is another title.
With some contents.
"""
```

You can then define some simple classes defining this content structure and patterns that match each content type. Finally we define a model.Finder, which allows us to search for the content type in the text file.

```python
import re

from fileparse import parse, read

class Text(parse.Content):
    pass
text_match = re.compile('^(?P<text>[^#].+)$')
text_finder = parse.ContentFinder(start_pattern=text_match,
                                  content_type=Text)

class SubTitle(parse.Content):
    pass
subtitle_match = re.compile('^## ?(?P<subtitle>[^#].+)$')
subtitle_finder = parse.ContentFinder(start_pattern=subtitle_match,
                                  content_type=SubTitle,
                                  sub_content_finders=[text_finder]
                                  )
                                  
class Title(parse.Content):
    pass
title_match = re.compile('^# ?(?P<title>[^#].+)$')
title_finder = parse.ContentFinder(start_pattern=title_match,
                               content_type=Title,
                               sub_content_finders=[subtitle_finder, text_finder])                                      
```
Notice two things:
* The regex patterns are named capture groups. The named capture groups are added as property to their content type. I.e. a `SubTitle` instance will receive a `SubTitle.subtitle` property.
* `Text` content can be found within both a `Title` and a `SubTitle`. And that a `SubTitle` only can be found within a `Title`. 

Finally, we define the Parser.

````python
 file_finder = parse.Parser(finders=[title_finder])   
````

The file_finder is now ready to parse text content.

For this specific content, we need a text stream able to parse a string. We define it like this:

````python
stream = read.TextStream(reader=read.StringReader(string=nested_text))
````

We can now parse the text with the rules defined in file_finder, and se what comes out of it. To get information out of a file-object, use the `file.get_contents_by_type(content_type)` method.

````python
file = file_finder.parse_stream(stream)

print(file.get_contents_by_type(SubTitle)[0].subtitle == 'This is a subtitle.')
print(file.get_contents_by_type(SubTitle)[0].contents[0].text == 'with subtitle contents.')
````

Happy parsing.
