__all__ = (
    'OverloadException',
)


class OverloadException(Exception):
    """Base class of overload lib exception"""
    __slots__ = ()
    _text = 'Base overload exception.'
    _code = 0

    def __init__(self, text_=None):
        super().__init__(text_ or self._text)

    def __repr__(self):
        return f'<{self.code}> {self.__class__.__name__} class - {self._text}'

    @property
    def text(self):
        """Description of exception."""
        return self._text

    @property
    def code(self):
        """Code of exception."""
        return self._code
