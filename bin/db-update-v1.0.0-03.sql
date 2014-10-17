
CREATE TABLE `hotornot-dev`.`tbl_status_update_viewer` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `status_update_id` INT(10) UNSIGNED NOT NULL,
    `member_id` INT(10) UNSIGNED NOT NULL,
    `viewed_on` TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`),
    UNIQUE KEY (`status_update_id`, `member_id`),
    INDEX `status_update_index` (`status_update_id`),
    CONSTRAINT FOREIGN KEY (`status_update_id`) REFERENCES `tblChallenges` (`id`),
    CONSTRAINT FOREIGN KEY (`member_id`) REFERENCES `tblUsers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

