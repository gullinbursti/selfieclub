
ALTER TABLE `tbl_club_label_club` ADD CONSTRAINT `club_id_refs_id` FOREIGN KEY (`club_id`) REFERENCES `club` (`id`);

