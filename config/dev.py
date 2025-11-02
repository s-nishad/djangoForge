"""
Development settings for the project.
"""

from .settings import *  # Import all settings from the base settings file

# ----------- DEVELOPMENT OVERRIDES -----------

# Enable debugging mode during development
DEBUG = True

# debug tootbar 
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware'] 
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]


# ----------- DATABASE SETTINGS -----------

# Use SQLite for the development database (this is the default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite backend
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to the SQLite database file
    }
}

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

