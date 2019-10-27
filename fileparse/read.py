import codecs
import abc
import collections
import typing as ty


class Reader:
    """Superclass for all Reader-subclasses."""

    def read_line(self) -> ty.Union[str, None]:
        """Return the next line of the text contents."""
        # noinspection PyUnresolvedReferences
        return self._read_line()


class ReaderMeta(abc.ABCMeta):
    """Abstract base class for text readers."""

    @abc.abstractmethod
    def _read_line(self) -> ty.Union[str, None]:
        """Method for reading the next line of the contents. Should return None if end of file or if errors are
        encountered."""


class FileReader(Reader, metaclass=ReaderMeta):
    """Simple reader for reading file contents."""
    def __init__(self, filepath: str, encoding: str) -> None:
        self.stream = codecs.open(filename=filepath, encoding=encoding)
        self.lines = self.stream.readlines()

    def _read_line(self) -> str:
        if not self.lines:
            self.stream.close()
            line = None
        else:
            line = self.lines.pop(0)

        return line


class StringReader(Reader, metaclass=ReaderMeta):
    """Simple reader for reading string contents."""
    def __init__(self, string: str) -> None:
        self.strings = string.splitlines()

    def _read_line(self) -> str:
        """Return the next line of the string."""
        try:
            return self.strings.pop(0)
        except IndexError:
            return None


class TextStream:
    """Class for containing a text stream."""
    stream: codecs.StreamReaderWriter

    def __init__(self, reader: Reader) -> None:
        self.reader = reader
        self.history = collections.deque(maxlen=100)  # The reader can backtrack 100 lines of text.
        self.read_backlog = list()  # The read backlog is always emptied before fetching a book line from self.reader.
        self.index = 0

    def backtrack_reader_number_of_lines(self, number: ty.Optional[int] = 1) -> None:
        """Reset the reader to continue reading from the previous """
        for i in range(number):
            self.read_backlog.append(self.history.pop())

    def get_line(self) -> str:
        """Return the current line for parsing."""
        if self.read_backlog:
            new_line = self.read_backlog.pop()
        else:
            new_line = self.reader.read_line()

        self.history.append(new_line)
        return new_line

    def get_previous_line(self) -> str:
        return self.history[-2]
