import os

os.environ['PYTEST_RUNNING'] = 'true'

from core.apps.accounts.tests.fixtures import *  # noqa
from core.general.tests.fixtures import *  # noqa
