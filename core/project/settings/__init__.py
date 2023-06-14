# from pathlib import Path

# from split_settings.tools import include, optional

# # BASE_DIR = Kollab
# BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# LOCAL_SETTINGS_PATH = str(BASE_DIR / "local/settings.dev.py")

# include(
#     # first load django settings
#     "base.py",
#     "logging.py",
#     # then load our own custom settings
#     "custom.py",
#     # then load local settings
#     optional(LOCAL_SETTINGS_PATH),
#     # look for system environment variables
#     # 'envvars.py',
#     "docker.py",
# )
import os.path
from pathlib import Path

from split_settings.tools import include, optional


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENVVAR_SETTINGS_PREFIX = 'CORE_SETTING_'
LOCAL_SETTINGS_PATH = os.getenv(f'{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH')

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = 'local/settings.dev.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    'base.py',
    'logging.py',
    # 'rest_framework.py',
    # 'channels.py',
    # 'aws.py',
    'custom.py',
    optional(LOCAL_SETTINGS_PATH),
    # 'envvars.py',
    'docker.py',
)
