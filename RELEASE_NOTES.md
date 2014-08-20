# Release notes

## SC0001

- Starting specific selfieclub release notes, unrelated to vollyapi

- On celery servers, update `selfieclub-celery-config/localsettings.py`, adding (with the real API Key and Secret from Nexmo.com):

    # -----------------------------------------------------------------------------
    # Nexmo
    NEXMO_USERNAME = 'XXXXXXXX'
    NEXMO_PASSWORD = 'XXXXXXXX' 

- On api servers, update `selfieclub-config/localsettings.py`:

    In the `LOGGING` array, in the `handlers` key, add a new item:

        'nexmologfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/opt/log/selfieclub/nexmo.log',
            'formatter': 'verbose',
        },

    In the same array, in the `loggers` key, add a new item:

        # Log Nexmo callback calls to a specific Nexmo log
        'nexmo': {
            'handlers': ['nexmologfile'],
            'level': 'INFO',
            'propagate': False
        },

- On api servers, in `/opt/built-in-menlo/selfieclub` run:

    pip install -e git+https://github.com/marcuz/libpynexmo.git#egg=nexmomessage

- DB change:

    ALTER TABLE `tbl_newsfeed_member_event` ADD `subject_member_id` int(11) DEFAULT NULL AFTER status_update_id;
