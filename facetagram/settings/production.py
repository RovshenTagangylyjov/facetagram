import dj_database_url
from .base import *

DEBUG = False

ALLOWED_HOSTS = ["myfacetagram.herokuapp.com"]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 15768000  # set low, but when site is ready for deployment, set to at least 15768000 (6 months)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SAMESITE = 'Strict'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cloudinary configs
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "disbvkli0", 
    "API_KEY": "135669314646314", 
    "API_SECRET": "1QCScCqCT2YuzzkSe8bm7nErIiE"
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'