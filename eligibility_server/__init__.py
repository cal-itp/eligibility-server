from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("eligibility-server")
except PackageNotFoundError:
    # package is not installed
    pass
