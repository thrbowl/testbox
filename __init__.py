try:
    import pkg_resources
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = '<unknown>'
