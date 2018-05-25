import logging.config

LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'generic': {
            'format': '%(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'NOTSET',
            'formatter': 'generic',
            'stream': 'ext://sys.stdout'
        },
        'applog': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'generic',
            'filename': '/var/log/py_libgit/app.log',
            'maxBytes': 1000000,
            'backupCount': 15
        }
    },
    'loggers': {
        'py_libgit': {
            'level': 'INFO',
            'handlers': ['applog'],
            'propagate': False
        }
    },
    'root': {
        'level': 'WARN',
        'handlers': ['console']
    }
}

logging.config.dictConfig(LOGGING_CONF)
