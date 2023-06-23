import os

os.environ['PYTEST_RUNNING'] = 'true'

from core.api.accounts.tests.fixtures import *  # noqa
from core.general.tests.fixtures import *  # noqa
