# Release notes

## v01.03.00

- **TODO** - FIll me in...


## v01.02.00

- On api server, pip install requests


## v01.01.00

- On celery server, update `selfieclub-celery-config/localsettings.py`, updating existing `AMAZON_SNS_ARN` value:

        AMAZON_SNS_ARN = 'arn:aws:sns:us-east-1:892810128873:app/APNS/' + \
            'Selfieclub-APNS'

    or, on devint:

        AMAZON_SNS_ARN = 'arn:aws:sns:us-east-1:892810128873:app/APNS_SANDBOX/' + \
            'Selfieclub-APNS_SANDBOX'

- On celery server, update `selfieclub-celery-config/localsettings.py`, adding below `AWS_CREDENTIALS`:

        AMAZON_SNS_ENV = 'APNS'

    or, on devint:

        AMAZON_SNS_ENV = 'APNS_SANDBOX'

- Repeat the above two changes on api server in `selfieclub-config/localsettings.py`

- DB change 1:

        CREATE TABLE `tbl_nexmo_source` (
          `id` int(11) NOT NULL,
          `phone_number` varchar(12) NOT NULL,
          `created` datetime NOT NULL,
          `updated` datetime NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        
        INSERT INTO `tbl_nexmo_source` (`id`, `phone_number`, `created`, `updated`) VALUE ('1', '19189620405', NOW(), NOW());
        INSERT INTO `tbl_nexmo_source` (`id`, `phone_number`, `created`, `updated`) VALUE ('2', '12132633816', NOW(), NOW());
        INSERT INTO `tbl_nexmo_source` (`id`, `phone_number`, `created`, `updated`) VALUE ('3', '12132633822', NOW(), NOW());
        INSERT INTO `tbl_nexmo_source` (`id`, `phone_number`, `created`, `updated`) VALUE ('4', '12132633823', NOW(), NOW());
        INSERT INTO `tbl_nexmo_source` (`id`, `phone_number`, `created`, `updated`) VALUE ('5', '12134657627', NOW(), NOW());
        INSERT INTO `tbl_nexmo_source` (`id`, `phone_number`, `created`, `updated`) VALUE ('6', '12525573328', NOW(), NOW());

- DB change 2:

        CREATE TABLE `tbl_counter` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `name` varchar(32) NOT NULL,
          `description` varchar(64) NOT NULL,
          `counter` int(11) NOT NULL,
          PRIMARY KEY (`id`),
          UNIQUE KEY `name` (`name`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        
        INSERT INTO `tbl_counter` (`name`, `description`, `counter`) VALUE ('NEXMO_PHONE_SEQ', 'Counter used in modulo operation to get next phone number', 0);


## v01.00.00

- On celery servers, update `selfieclub-celery-config/localsettings.py`, adding (with the real API Key and Secret from Nexmo.com):

        # -----------------------------------------------------------------------------
        # Nexmo
        NEXMO_USERNAME = 'XXXXXXXX'
        NEXMO_PASSWORD = 'XXXXXXXX' 

- On celery and api servers, update `selfieclub-celery-config/localsettings.py`:

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
