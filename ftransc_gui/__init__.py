import pkg_resources

try:
    __version__ = pkg_resources.get_distribution('ftransc_gui').version
except pkg_resources.DistributionNotFound:
    __version__ = '0.0.1'

