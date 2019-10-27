"""Tests for the model compontents of the photo book."""
import re
import os

from fileparse import parse, read

FILENAME = os.path.join(os.path.split(__file__)[0], 'bin', 'context.md')

SIMPLE_TEXT = """This is a test.
# this is content
¤ this is not
fin"""

NESTED_TEXT = """# This is a title.
This is contents.
And some more.

## This is a subtitle.
with subtitle contents.

# This is another title.
With some contents.
"""


def test_text_stream_previous():
    stream = read.TextStream(reader=read.StringReader(string=SIMPLE_TEXT))

    assert stream.get_line() == 'This is a test.'
    assert stream.get_line() == '# this is content'
    assert stream.get_previous_line() == 'This is a test.'
    stream.get_line()
    assert stream.get_line() is not None
    assert stream.get_line() is None  # End of file.


def test_text_stream_backtrack():
    stream = read.TextStream(reader=read.StringReader(string=SIMPLE_TEXT))

    assert stream.get_line() == 'This is a test.'
    assert stream.get_line() == '# this is content'
    assert stream.get_line() == '¤ this is not'
    assert stream.get_line() == 'fin'
    stream.backtrack_reader_number_of_lines(2)
    assert stream.get_line() == '¤ this is not'
    assert stream.get_line() == 'fin'
    assert stream.get_previous_line() == '¤ this is not'


def test_file_reader():
    # Read entire file:
    # import codecs
    # with codecs.open(FILENAME) as file:
    #     for line in file.readlines():
    #         print(line)
    stream = read.TextStream(reader=read.FileReader(filepath=FILENAME, encoding='utf-8'))
    line = ''
    while line is not None:
        line = stream.get_line()


def test_content_finder_simple():
    stream = read.TextStream(reader=read.StringReader(string=SIMPLE_TEXT))

    c = parse.ContentFinder(start_pattern=re.compile('^#(?P<stuff>.+)$'),
                            end_pattern=re.compile('^¤'))

    content = c.search_stream(stream)

    assert content.stuff == ' this is content'


def test_content_finder_nested():
    class Text(parse.Content):
        pass

    class Title(parse.Content):
        pass

    class SubTitle(parse.Content):
        pass

    text_match = re.compile('^(?P<text>[^#].+)$')
    title_match = re.compile('^# ?(?P<title>[^#].+)$')
    subtitle_match = re.compile('^## ?(?P<subtitle>[^#].+)$')
    stream = read.TextStream(reader=read.StringReader(string=NESTED_TEXT))

    text_finder = parse.ContentFinder(start_pattern=text_match,
                                      content_type=Text)
    subtitle_finder = parse.ContentFinder(start_pattern=subtitle_match,
                                          content_type=SubTitle,
                                          sub_content_finders=[text_finder]
                                          )
    title_finder = parse.ContentFinder(start_pattern=title_match,
                                       content_type=Title,
                                       sub_content_finders=[subtitle_finder, text_finder])

    file_finder = parse.Parser(finders=[title_finder])

    file = file_finder.parse_stream(stream)
    # TODO: Figure out why i can't find subtitles.
    assert file.get_contents_by_type(SubTitle)[0].subtitle == 'This is a subtitle.'
    assert file.get_contents_by_type(SubTitle)[0].contents[0].text == 'with subtitle contents.'



