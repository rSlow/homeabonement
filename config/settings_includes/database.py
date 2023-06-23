from config.settings_includes.base import ENV

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": ENV.str("DB_NAME"),
        "USER": ENV.str("DB_USER"),
        "PASSWORD": ENV.str("DB_PASSWORD"),
        "HOST": ENV.str("DB_HOST"),
        "PORT": ENV.int("DB_PORT"),
        "OPTIONS": {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}
