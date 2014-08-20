# Release notes

## SC0002

- DB change:

        CREATE TABLE `tbl_messaging_callback` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `message_id` varchar(16) NOT NULL,
          `status_id` varchar(9) DEFAULT NULL,
          `error_id` smallint(6) DEFAULT NULL,
          `source_number` varchar(18) NOT NULL,
          `source_network` varchar(6) DEFAULT NULL,
          `destination_number` varchar(18) NOT NULL,
          `text` varchar(255) NOT NULL,
          `callback_timestamp` datetime NOT NULL,
          `created` datetime NOT NULL,
          `updated` datetime NOT NULL,
          PRIMARY KEY (`id`),
          UNIQUE KEY `message_id` (`message_id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

- On api servers, update `selfieclub-config/localsettings.py`, removing everything added last release


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

- DB change:

        ALTER TABLE `tbl_newsfeed_member_event` ADD `subject_member_id` int(11) DEFAULT NULL AFTER status_update_id;
