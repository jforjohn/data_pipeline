from os import path
from configparser import BasicInterpolation

class EnvInterpolation(BasicInterpolation):
    """Interpolation which expands environment variables in values."""
    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return path.expandvars(value)