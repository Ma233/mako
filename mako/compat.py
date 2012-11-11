import sys
import time

py3k = sys.version_info >= (3, 0)
py3kwarning = getattr(sys, 'py3kwarning', False) or py3k
py26 = sys.version_info >= (2, 6)
py25 = sys.version_info >= (2, 5)
jython = sys.platform.startswith('java')
win32 = sys.platform.startswith('win')
pypy = hasattr(sys, 'pypy_version_info')

if py3k:
    from io import StringIO
    import builtins as compat_builtins
    from urllib.parse import quote_plus, unquote_plus
    from html.entities import codepoint2name, name2codepoint
    string_types = str,
    binary_type = bytes
    text_type = str

    def u(s):
        return s

    def octal(lit):
        return eval("0o" + lit)

else:
    import __builtin__ as compat_builtins
    try:
        from cStringIO import StringIO
    except:
        from StringIO import StringIO
    from urllib import quote_plus, unquote_plus
    from htmlentitydefs import codepoint2name, name2codepoint
    string_types = basestring,
    binary_type = str
    text_type = unicode

    def u(s):
        return unicode(s, "utf-8")

    def octal(lit):
        return eval("0" + lit)

def exception_as():
    return sys.exc_info()[1]

try:
    import threading
    if py3k:
        import _thread as thread
    else:
        import thread
except ImportError:
    import dummy_threading as threading
    if py3k:
        import _dummy_thread as thread
    else:
        import dummy_thread as thread

if win32 or jython:
    time_func = time.clock
else:
    time_func = time.time

try:
    from functools import partial
except:
    def partial(func, *args, **keywords):
        def newfunc(*fargs, **fkeywords):
            newkeywords = keywords.copy()
            newkeywords.update(fkeywords)
            return func(*(args + fargs), **newkeywords)
        return newfunc

if not py25:
    def all(iterable):
        for i in iterable:
            if not i:
                return False
        return True

    def exception_name(exc):
        try:
            return exc.__class__.__name__
        except AttributeError:
            return exc.__name__
else:
    all = all

    def exception_name(exc):
        return exc.__class__.__name__

try:
    from inspect import CO_VARKEYWORDS, CO_VARARGS
    def inspect_func_args(fn):
        if py3k:
            co = fn.__code__
        else:
            co = fn.func_code

        nargs = co.co_argcount
        names = co.co_varnames
        args = list(names[:nargs])

        varargs = None
        if co.co_flags & CO_VARARGS:
            varargs = co.co_varnames[nargs]
            nargs = nargs + 1
        varkw = None
        if co.co_flags & CO_VARKEYWORDS:
            varkw = co.co_varnames[nargs]

        if py3k:
            return args, varargs, varkw, fn.__defaults__
        else:
            return args, varargs, varkw, fn.func_defaults
except ImportError:
    import inspect
    def inspect_func_args(fn):
        return inspect.getargspec(fn)

if py3kwarning:
    def callable(fn):
        return hasattr(fn, '__call__')
else:
    callable = callable

################################################
# cross-compatible exec_()
# Copyright (c) 2010-2012 Benjamin Peterson
if py3k:
    import builtins
    exec_ = getattr(builtins, "exec")


    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value


    print_ = getattr(builtins, "print")
    del builtins

else:
    def exec_(code, globs=None, locs=None):
        """Execute code in a namespace."""
        if globs is None:
            frame = sys._getframe(1)
            globs = frame.f_globals
            if locs is None:
                locs = frame.f_locals
            del frame
        elif locs is None:
            locs = globs
        exec("""exec code in globs, locs""")
################################################

################################################
# cross-compatible metaclass implementation
# Copyright (c) 2010-2012 Benjamin Peterson
def with_metaclass(meta, base=object):
    """Create a base class with a metaclass."""
    return meta("%sBase" % meta.__name__, (base,), {})
################################################


