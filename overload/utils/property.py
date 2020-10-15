__all__ = (
    'cached_property',
)


class _CachedProperty:
    """Realisation of cashed property for python < 3.8."""

    __slots__ = ('_cash', '_method',)

    def __repr__(self):
        return '<class CashedProperty>'

    def __init__(self, method_):
        self._method = method_

    def __get__(self, obj, cls):
        if not hasattr(self, '_cash'):
            self._cash = self._method(obj)

        return self._cash


def cached_property(function_) -> _CachedProperty:
    """Change method to _CashedProperty class,
    who cashing it result."""
    cls = _CachedProperty(function_)

    return cls
