"""sig implementation

This is a fun (out of the question about speed, if you need
a really fast and stable signature change, then take a closer
look at makefun) implementation option for dynamic signature
change, it is a bit "dangerous" compared to makefun's implementation
(but I do everything to somehow make this work with kwonly and
posonly args).
"""

from __future__ import annotations

__all__ = [
    "change_args",
    "from_function",
]

import inspect
from dataclasses import dataclass
from types import CodeType, FunctionType
from typing import TYPE_CHECKING, Any, Callable, List, Sequence, Tuple, cast

from funchacks.internal import MISSING
from funchacks.sig.marks import Argument

if TYPE_CHECKING:
    from funchacks.typehints import FunctionT, ShouldReturn


def code_template(
    initial: CodeType,
    /,
    argcount: int,
    posonlycount: int,
    kwonlycount: int,
    varnames: Tuple[str, ...],
) -> CodeType:
    return CodeType(
        argcount,
        posonlycount,
        kwonlycount,
        initial.co_nlocals,
        initial.co_stacksize,
        initial.co_flags,
        initial.co_code,
        initial.co_consts,
        initial.co_names,
        varnames,
        initial.co_filename,
        initial.co_name,
        initial.co_firstlineno,
        initial.co_lnotab,
        initial.co_freevars,
        initial.co_cellvars,
    )


@dataclass
class ArgdefSignature:
    argnames: List[str]
    defaults: List[Any]
    argcount: int
    kwonlycount: int
    posonlycount: int

    @classmethod
    def unwrap_args(cls, sig: Sequence[Argument]) -> ArgdefSignature:
        kwonlyc = 0
        posonlyc = 0
        argnames = []
        defaults = []
        for param in sig:
            if param.type is inspect.Parameter.POSITIONAL_ONLY:
                posonlyc += 1

            elif param.type is inspect.Parameter.KEYWORD_ONLY:
                kwonlyc += 1

            default = param.default
            if default is not MISSING:
                defaults.append(param.default)

            argnames.append(param.name)

        return cls(
            argnames=argnames,
            defaults=defaults,
            argcount=len(sig) - kwonlyc,
            kwonlycount=kwonlyc,
            posonlycount=posonlyc,
        )

    @classmethod
    def unwrap_from_function(cls, fn: FunctionT, /) -> ArgdefSignature:
        sig = inspect.Signature.from_callable(cast(Callable[..., Any], fn))
        args = []
        for param_name, param in sig.parameters.items():
            if param.kind in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
                continue

            default = param.default
            if default is param.empty:
                default = MISSING

            args.append(
                Argument(
                    name=param_name,
                    type=param.kind,
                    default=default,
                )
            )

        return cls.unwrap_args(args)

    def filter_varnames(self, code: CodeType, /) -> List[str]:
        fnargs = inspect.getargs(code)._asdict()["args"]
        _fn_co_varnames = code.co_varnames
        if _fn_co_varnames:
            varnames = list(code.co_varnames)
            for var in _fn_co_varnames:
                if var in fnargs:
                    varnames.remove(var)
        else:
            varnames = []

        return varnames


def change_args(*args: Argument) -> ShouldReturn[FunctionT]:
    def inner(fn: FunctionT) -> FunctionT:
        sig = ArgdefSignature.unwrap_args(args)
        code = fn.__code__

        self = FunctionType(
            code_template(
                code,
                sig.argcount,
                sig.posonlycount,
                sig.kwonlycount,
                tuple(sig.argnames + sig.filter_varnames(code)),
            ),
            fn.__globals__,
            fn.__name__,
            tuple(sig.defaults),
            fn.__closure__,
        )
        setattr(self, "__sig__", sig)
        return self

    return inner


def from_function(fn: FunctionT, /) -> ShouldReturn[FunctionT]:
    def inner(_: FunctionT) -> FunctionT:
        sig = ArgdefSignature.unwrap_from_function(fn)
        code = fn.__code__

        self = FunctionType(
            code_template(
                code,
                sig.argcount,
                sig.posonlycount,
                sig.kwonlycount,
                tuple(sig.argnames + sig.filter_varnames(code)),
            ),
            fn.__globals__,
            fn.__name__,
            tuple(sig.defaults),
            fn.__closure__,
        )
        setattr(self, "__sig__", sig)
        return self

    return inner
