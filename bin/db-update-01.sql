
INSERT INTO tbl_newsfeed_user_event_type (`id`, `name`, `description`, `updated`, `created`) VALUES
    (1, "ALL", "All newsfeed types", NOW(), NOW()),
    (2, "VERIFIED", "Verified (likes/upvotes has surpassed threshold)", NOW(), NOW()),
    (3, "RECEIVED_UPVOTE", "Received an upvote / like on a photo submission", NOW(), NOW()),
    (4, "RECEIVED_REPLY", "Received a photo reply to a photo submission", NOW(), NOW()),
    (5, "CLUB_JOIN", "Club invite was accepted", NOW(), NOW()),
    (6, "CLUB_QUIT", "Someone quit a club owned by the this user", NOW(), NOW()),
    (7, "CLUB_INVITATION", "Received a club invitation", NOW(), NOW()),
    (8, "CLUB_PHOTO_SUBMITION", "A photo was submitted to a club this user owns", NOW(), NOW()),
    (9, "CLUB_REPLY", "A photo/reply was submitted to a club", NOW(), NOW())
    ;
