"""
Development settings for the project.
"""

from .settings import *  # Import all settings from the base settings file

# ----------- DEVELOPMENT OVERRIDES -----------

# Enable debugging mode during development
DEBUG = True

# debug tootbar
if DEBUG and 'debug_toolbar' not in INSTALLED_APPS:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware'] 

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]


# ----------- DATABASE SETTINGS -----------
# Use PostgreSQL for production database
# DATABASES = {
#     'default': {
#         'ENGINE': config('DATABASE_ENGINE', 'django.db.backends.postgresql'),  # PostgreSQL database engine
#         'NAME': config('DATABASE_NAME', 'mydatabase'),  # Database name (from environment variable)
#         'USER': config('DATABASE_USERNAME', 'myuser'),  # Database user (from environment variable)
#         'PASSWORD': config('DATABASE_PASSWORD', 'mypassword'),  # Database password (from environment variable)
#         'HOST': config('DATABASE_HOST', 'localhost'),  # Database host (from environment variable)
#         'PORT': config('DATABASE_PORT', '5432'),  # Database port (default: 5432)
#     }
# }

# Use SQLite for the development database (this is the default)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # SQLite backend
#         'NAME': BASE_DIR / 'db.sqlite3',  # Path to the SQLite database file
#     }
# }

# ----------- LOGGING SETTINGS -----------

# Configure logging to display debug messages to the console
LOGGING = {
    'version': 1,  # Logging version
    'disable_existing_loggers': False,  # Don't disable existing loggers
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',  # Log to console
        },
    },
    'root': {
        'handlers': ['console'],  # Log to console
        'level': 'DEBUG',  # Log at the debug level
    },
}

# ----------- EMAIL SETTINGS -----------

# Use file-based email backend for development (saves sent emails to files)
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'  # Directory to save emails in development

