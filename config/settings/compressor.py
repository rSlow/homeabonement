from config.settings.base import STATIC_ROOT

COMPRESS_ROOT = STATIC_ROOT
COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'django_libsass.SassCompiler'),
]
COMPRESS_OFFLINE = True
COMPRESS_OUTPUT_DIR = 'sass-compressed'
LIBSASS_OUTPUT_STYLE = 'compressed'
