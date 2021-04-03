"""File contain function implementation class."""
from types import FunctionType
from typing import Union, Dict, List, Tuple, FrozenSet, Optional

from overload.type.type import _Type, _ArgsType, _KwargsType, Args, Kwargs
from overload.exception.overloader import MissedAnnotations
from overload.exception.type import SingleTypeError

from .base import ABCImplementation

__all__ = (
    'FunctionImplementation',
)


class FunctionImplementation(ABCImplementation):
    """Implementation for overload function."""
    __slots__ = (
        '__kwargs_annotations__',
        '__args_annotations__',
        '__default_kwargs__',
        '__default_args__',
        '__kwargs_without_defaults__',
        '__args_without_defaults__',
        '__only_args__',
        '__infinite_args__',
        '__infinite_kwargs__',
    )

    __kwargs_annotations__: Dict[str, _Type]
    __args_annotations__: Dict[str, _Type]
    __default_args__: FrozenSet[str]
    __default_kwargs__: FrozenSet[str]
    __kwargs_without_defaults__: FrozenSet[str]
    __args_without_defaults__: FrozenSet[str]
    __only_args__: FrozenSet[str]
    __infinite_args__: Optional[_ArgsType]
    __infinite_kwargs__: Optional[_KwargsType]

    @property
    def __all_annotations__(self) -> Dict[str, _Type]:
        return {**self.__args_annotations__, **self.__kwargs_annotations__}

    def compare(
            self,
            named: Dict[str, _Type] = None,
            unnamed: Union[List[_Type], Tuple[_Type, ...]] = None,
    ) -> bool:
        """Comparing kwargs parameters and args with storage annotations.

        Args:
            named (dict): Dict with format {parameter_name : type}.
            unnamed (list or tuple): Parameters passed without key.
                Sequence of type.

        """
        named = named or {}
        unnamed = unnamed or ()
        check_args = self.__args_annotations__.copy()

        # Check parameters count more than registered parameters count.
        if len(self.__all_annotations__) < len(named) + len(unnamed):
            return False

        # Compare named parameters.
        # Check: in named parameters missed kwargs only parameters without
        # default value and is only args in kwargs.
        set_named = set(named.keys())
        is_missed_kwargs = bool(self.__kwargs_without_defaults__ - set_named)
        is_only_args_in_kwargs = bool(self.__only_args__ & set_named)

        if is_missed_kwargs or is_only_args_in_kwargs:
            return False

        # Check kwargs parameter values types.
        for param, type_ in named.items():
            try:
                # Check type of parameter.
                if type_ != self.__kwargs_annotations__[param]:
                    return False

            # Parameter not fount in registered kwargs annotations.
            except KeyError:
                # Remove parameter from args and compare it.
                parameter_in_args = check_args.pop(param, None)
                parameter_has_def = param in self.__default_kwargs__

                # Parameter not found in args and nas not default value.
                if not parameter_in_args and not parameter_has_def:
                    return False

                # Parameter from args, check it.
                elif parameter_in_args:
                    try:
                        if type_ != self.__args_annotations__[param]:
                            return False

                    # Parameter not found in registered args or kwargs.
                    except KeyError:
                        return False

        # Compare unnamed parameters.
        # Check args without default count less than unnamed.
        check_args_keys = tuple(check_args.keys())
        if len(set(check_args_keys) - self.__default_args__) > len(unnamed):
            return False

        # Check args types.
        index = None
        for index, type_ in enumerate(unnamed):
            if type_ != check_args[check_args_keys[index]]:
                return False
        else:
            # Check args without defaults in check annotations.
            if self.__args_without_defaults__ & set(check_args_keys[index:]):
                return False

        return True

    def _separate_annotations(self, implementation: FunctionType,
                              annotations: Dict[str, _Type]) -> None:
        """Separate function annotations to de."""
        # Remove return annotations if it exist.
        annotations.pop('return', None)

        self.__args_annotations__ = {}
        self.__kwargs_annotations__ = {}
        self.__infinite_kwargs__ = None
        self.__infinite_args__ = None

        args_count = implementation.__code__.co_argcount
        kwargs_count = implementation.__code__.co_kwonlyargcount

        # Check all parameters has been annotation.
        parameters_count = args_count + kwargs_count
        if len(annotations) < parameters_count:
            raise MissedAnnotations(
                f'Implementation has {parameters_count} parameters, but '
                f'has been annotated only {len(annotations)} parameters. All '
                f'implementation parameters must be annotated.'
            )

        args_only = getattr(implementation.__code__, 'co_posonlyargcount', 0)
        self.__only_args__ = frozenset(tuple(annotations.keys())[:args_only])

        # Split annotations to args and kwargs. Counter track parameter index.
        counter = 0
        for key, value in annotations.items():
            if counter < args_count:
                self.__args_annotations__[key] = value
            elif isinstance(value, _ArgsType):
                if self.__infinite_args__:
                    raise SingleTypeError(type_=Args)
                else:
                    self.__infinite_args__ = value
            elif isinstance(value, _KwargsType):
                if self.__infinite_kwargs__:
                    raise SingleTypeError(type_=Kwargs)
                else:
                    self.__infinite_kwargs__ = value
            else:
                self.__kwargs_annotations__[key] = value

            counter += 1

        # Getting kwargs default values.
        if implementation.__kwdefaults__:
            self.__default_kwargs__ = frozenset(
                implementation.__kwdefaults__.keys()
            )
            self.__kwargs_without_defaults__ = frozenset(
                field for field in self.__kwargs_annotations__.keys()
                if field not in self.__default_kwargs__
            )

        else:
            self.__default_kwargs__ = frozenset()
            self.__kwargs_without_defaults__ = frozenset(
                self.__kwargs_annotations__.keys()
            )

        # Getting args default values.
        args_annotations_keys = tuple(self.__args_annotations__.keys())

        if implementation.__defaults__:
            defaults_count = len(implementation.__defaults__)
            self.__default_args__ = frozenset(
                args_annotations_keys[-defaults_count:]
            )
            self.__args_without_defaults__ = frozenset(
                args_annotations_keys[:-defaults_count]
            )
        else:
            self.__default_args__ = frozenset()
            self.__args_without_defaults__ = frozenset(args_annotations_keys)
