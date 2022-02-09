import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, 'screenshots')
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'download')

# =====================================

LOGGING_CONFIG = {
    'formatters': {
        'brief': {
            'format': '[%(asctime)s][%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief'
        }
    },
    'loggers': {
        'main': {
            'propagate': False,
            'handlers': ['console'],
            'level': 'INFO'
        }
    },
    'version': 1
}


