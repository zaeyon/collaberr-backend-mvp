import os

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, "templates"),  # type: ignore
]
IN_DOCKER = False

# SECURITY WARNING: disable this setting in production!
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
