# Release notes

## v01.01.00

- **TODO** - FIll me in...


## v01.00.00

- On celery servers, update `selfieclub-celery-config/localsettings.py`, adding (with the real API Key and Secret from Nexmo.com):

        # -----------------------------------------------------------------------------
        # Nexmo
        NEXMO_USERNAME = 'XXXXXXXX'
        NEXMO_PASSWORD = 'XXXXXXXX' 

- On celery servers, update `selfieclub-celery-config/localsettings.py`:

    Near the AWS credentials, add this:

        AMAZON_SNS_ARN = 'arn:aws:sns:us-east-1:892810128873:Selfieclub_SMS_Dev'

- DB change 1:

        ALTER TABLE `tbl_newsfeed_member_event` ADD `subject_member_id` int(11) DEFAULT NULL AFTER status_update_id;

- DB change 2:

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
