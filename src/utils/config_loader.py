import configparser
import sys
import traceback
from os import path
from .customInterpolation import EnvInterpolation

requiredConfig = {
    }
PROJECT_PATH = path.join(
    path.dirname(path.abspath(__file__)),
    path.pardir
)

config_file_default = path.join(PROJECT_PATH, 'config.ini')

def load(config_file=config_file_default):
  """
  Reads configuration file
  """

  try:
    # Load configuration from file
    config = configparser.ConfigParser(
        interpolation=EnvInterpolation()
        )
    number_read_files = config.read(config_file)

    # check the config file exist and can be read
    if len(number_read_files) != 1:
      print("Configuration file '{0}' cannot be read or does not exist. Stopping.".format(config_file))
      sys.exit(1)

    # Force load of all required fields to avoid errors in runtime
    for section, options in requiredConfig.items():
      for option in options:
        try:
          config.get(section, option)
        except configparser.NoSectionError:
          print("Section '{0}' not present in config file. Stopping.".format(section))
          sys.exit(2)
        except configparser.NoOptionError:
          print("Option '{0}' not present in section {1} in config file. Stopping.".format(option, section))
          sys.exit(2)
    return config

  except IOError as e:
    traceback.print_exc(file=sys.stdout)
    sys.exit(e)
    