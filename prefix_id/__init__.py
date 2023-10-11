import importlib.metadata

from .field import PrefixIDField  # noqa: F401

__all__ = ["PrefixIDField"]

__version__ = importlib.metadata.version("django-prefix-id")
VERSION = __version__
