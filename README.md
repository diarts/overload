# Overload
[![versions](https://img.shields.io/badge/python-3.7%2F3.8%2F3.9-green)](https://github.com/diarts/overload)

- [About](#about)
- [Usage](#usage)

## About
"Overload" is a Python 3 package for functions overloading.
"Overload" use pure python3 typing and hasn't requirements.
Support python version >= 3.7.

## Usage
### Install package
```
pip install overloader
```

### Overloading functions example.
To overload function you need importing overload decorator from package 
and using it with your overloading target function. Now this function becomes 
a default implementation and will be called in the last place or when call 
arguments will success compare with it.
For registering new implementation of it, use it "register" method.
Untyped variables be ignored.
```python
from overload import overload

@overload
def my_function(var1: int, var2: str):
    # function logic.
    print('I am a default function.')

@my_function.register
def _(var1:str, var2: int):
    # implementation logic.
    print('I am an implementation.')

```
When you call "overload object", will called implementation with success 
compare variables types or default implementation.
```python
my_function(1, 'string')
# stdout: I am a default function.

my_function('string', 1)
# stdout: I am an implementation.
```

### Overloading function specific parameters typing.
For typing specific parameters, like *args or **kwargs, must use special type
Args and Kwargs.

```python
from typing import Union
from overload import Args, Kwargs, overload

@overload
def my_function(*args: Args[int], **kwargs: Kwargs[Union[str, int]]):
    pass
```
If you ignored special types and set type for it like regular parameter
*args: int, this will interpret not as *args parameter, but args. 

### Overloading function parameters.
Overload decorator has two settings:
- strict (bool, default=True)
- overlapping (bool, default=False)

<b>Strict</b> - activate validation of implementation annotations count 
compared overload object annotations.
```python
@overload(strict=True)
def my_function(var1: str):
    ...

@my_function.register
def _(var1: str, var2: int):
    ...

# Will raised AnnotationCountError.
```
<b>Overlapping</b> - activate registration of implementation with 
same annotations as the default overload object.
```python
@overload(overlapping=False)
def my_function(var1: str):
    ...

@my_function.register
def _(var1: str):
    ...

# Will raised OverlappingError.
```