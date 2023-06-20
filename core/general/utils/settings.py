import os

from .misc import yaml_coerce


def get_settings_from_environment(prefix):
    """
    Iterate through the environment variables
    check if the key starts with the prefix
    and return a dictionary of the key-value pairs

    Example:
        'CORE_SETTING_IN_DOCKER = 1' will be returned as
        {'IN_DOCKER': 1}
    """
    prefix_len = len(prefix)
    return {key[prefix_len:]: yaml_coerce(value) for key, value in os.environ.items() if key.startswith(prefix)}
