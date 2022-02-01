<h1 align="center">funchacks</h1>
<p align="center">
<a href="https://github.com/psf/black"><img height="20" alt="PyPI version" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img height="20" alt="Supported python versions" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
<br>
<a href="https://www.python.org/dev/peps/pep-0008/"><img height="20" alt="CI status" src="https://img.shields.io/badge/flake8-checked-blue.svg"></a>
<a href="https://pypi.org/project/mypy/"><img height="20" alt="Mypy badge" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>

<div align="center">
    <a href="https://discord.com/invite/KKUFRZCt4f"><img src="https://discordapp.com/api/guilds/744099317836677161/widget.png?style=banner2" alt="" /></a>
</div>

# 👋 Introduction
Funchacks is a fun module that provides a small package of utilities.

**Dynamic signature change without compile, eval and exec?**
That was the main idea of the project! But this path is a little dangerous,
so the part could not be implemented, but if possible it will be implemented in the next versions!

**So is it worth using funchacks signature utilities?**
More likely no than yes. If you want a really optimized and safe implementation of this idea, it's better to
look into `makefun` (this was another reason why I wanted to do a dynamic signature change without compile, eval and exec).

# ⚙️ Installation
```bash
pip install funchacks
```

# 🚀 Quick start

- ### 🔎 Function locals
```py
from funchacks import inspections


def foo() -> None:
    some_local_var = 1
    other_var = 2

>>> dict(inspections.getlocals(foo.__code__))
{"some_local_var": 1, "other_var": 2}
```

- ### 🔗 Dynamic function signature
> `(!)` Note: if you add *positional only* or *positional arguments*, then there must be `*args` in the function signature.
> Accordingly, if you add *keyword only* or *keyword arguments* - `**kwargs`.

```py
import inspect
from typing import Any

from funchacks import sig
```

```py
@sig.change_args(
    sig.posonly("first"),
    sig.arg("second"),
)
def foo(*args: Any) -> None:
    """
    !!! Note:
        Temporarily positional only arguments are available only for
        the signature, there may be errors when calling the function.
    """

>>> inspect.Signature.from_callable(foo)
(first, /, second, *args)
```

```py
@sig.change_args(
    sig.kwarg("first", None),
    sig.kwonly("second"),
)
def bar(**kwargs: Any) -> None:
    """
    !!! Note:
        Temporarily keyword only arguments are available only for
        the signature, there may be errors when calling the function.
    """

>>> inspect.Signature.from_callable(bar)
(first=None, *, second, **kwargs)
```

```py
@sig.change_args(
    sig.arg("first"),
    sig.kwarg("second", None)
)
def baz(*args: Any, **kwargs: Any) -> None:
    """This should work.

    But how to access the arguments? locals?...
    """
    # All wrapped function has __sig__ attribute
    # that contains function signature.
    lvars = sig.Bind.from_locals(locals(), in_=baz)

    assert lvars.args() == ["first"]
    assert lvars.kwargs() == ["second"]

    return lvars.get("first") + lvars.get("second")

>>> inspect.Signature.from_callable(baz)
(first, second=None, *args, **kwargs)

>>> baz(1, 2)
3
```

#### Signature from function.
```py
def spam(a, /, b, c=None, *, d) -> None:
    pass


@sig.from_function(spam)
def eggs(*args: Any, **kwargs: Any) -> None:
    pass

>>> inspect.Signature.from_callable(eggs)
(a, /, b, c=None, *, d)
```
