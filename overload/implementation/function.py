"""File contain function implementation class."""
from types import FunctionType
from typing import Union, Dict, List, Tuple, FrozenSet, Optional, Set

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
        check_kwargs = self.__kwargs_annotations__.copy()

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
                if not self._compare_type(
                        type_,
                        check_kwargs.pop(param),
                ):
                    return False

            # Parameter not found in registered kwargs annotations.
            except KeyError:
                # Parameter not found in args and nas not default value and
                # implementation hasn't kwargs.
                if (
                        param not in self.__args_annotations__
                        and not self.__infinite_kwargs__
                ):
                    return False

                # Parameter from args, check it.
                elif param in self.__args_annotations__:
                    try:
                        # Slice check_args.
                        found_border = False
                        for key, value in self.__args_annotations__.items():
                            if found_border:
                                # Transition args to kwargs.
                                try:
                                    check_kwargs[key] = check_args.pop(key)
                                except KeyError:
                                    break

                            # Find parameter in args.
                            elif key == param:
                                found_border = True

                                # Check parameter type.
                                if not self._compare_type(
                                        type_,
                                        check_args.pop(param),
                                ):
                                    return False

                    # Parameter not found in registered args or kwargs.
                    except KeyError:
                        return False

                # Parameters not in kwargs and args check it with infinite.
                elif type_ not in self.__infinite_kwargs__:
                    return False

        # Compare unnamed parameters.
        check_args_keys = tuple(check_args.keys())

        # Check args types.
        index = -1
        for index, type_ in enumerate(unnamed):
            try:
                if not self._compare_type(
                        type_,
                        check_args.pop(check_args_keys[index]),
                ):
                    return False

            # Check args is ended, but unnamed exists. Check it with infinite.
            except IndexError:
                if (
                        not self.__infinite_args__
                        or type_ not in self.__infinite_args__
                ):
                    return False

        if check_args:
            # Check args without defaults in check annotations.
            if set(check_args_keys[index + 1:]) - self.__default_args__:
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
        only_args = {}

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

        # Split annotations to args and kwargs. Counter track parameter index.
        counter = 0
        for key, value in annotations.items():
            # First simple args.
            if counter < (args_count - args_only):
                self.__args_annotations__[key] = value

            # Second only args.
            elif counter < args_count:
                only_args[key] = value

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

        # Switch only args and simple args position.
        self.__only_args__ = frozenset(only_args.keys())

        only_args.update(self.__args_annotations__)
        self.__args_annotations__ = only_args

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

    @staticmethod
    def _compare_type(type_: _Type,
                      parameter: Union[_Type, Set[_Type]]) -> bool:
        """Compare type with annotation parameter type."""
        return False if (
                (isinstance(parameter, _Type) and type_ != parameter)
                or (isinstance(parameter, set) and type_ not in parameter)
        ) else True
