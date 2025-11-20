# GetAJob
Webpage for CSC 131 section 4 group 5

### Description
Our job platform is a web-based system that connects contractors and clients to small or large job opportunities. Our purpose is to provide an easy to use, streamlined system where someone can list / find jobs no matter the size.

### Database field
 - __User__:
    | Fields |
    | ------ |
    | user_id |
    | user_name |
    | email |
    | password |
    |age |
    | address |
    | first_name |
    | last_name |
    | location |
    | profile |
    | pfp |
    | is_admin |
    | is_banned |
    | create_time |
    | modify_time |

 - __Post__
    | Fields |
    | ------ |
    | post_id |
    | title |
    | description |
    | owner_id |
    | location |
    | budget |
    | create_time |
    | modify_time |

### Database api
 - __User__:    
    | Function Name | Input | Return Value | Description |
    | ------------- | ----- | ------------ | ----------- |
    | create_account | username, password, email | success | Insert user into database |
    | get_user_info | username or user id or email | email, phone... | get all user data except password with either username, user id or email|
    | verify_password | username, password | True/False | check if password match the user's password, use for logging in account |
    | update_user_name | new username, old username | success | change username from old to new |
    | update_password | username, new password | success | change user password |
    | update_user_profile | username, email, phone... | success | update a user's profile(pass in only the one that needs to be updated) |
    | ban_user | username | success | ban a user (only admin has permision to ban) |
    | unban_user | username | success | unban a user (only admin has permision to unban) |
    | delete_user | username or user id or email | success | delete your account |

- __Post__:
    | Function Name | Input | Return Value | Description |
    |---------------|-------|--------------|-------------|
    | create_post | title, description, owner_id | success | create post |
    | delete_post | post_id | success | delete post with post id |
    | update_post | post_id, fields that needs to be updated | success | update post with id |
    | select_post | post_id | all fields of the selected post | select post with post id |
    | select_user_post | user_id | all posts created by the user | select posts created by a user |
    | select_latest_n_posts | limit, offset| latest n posts |  select the last n post that's modified |

### Contact Information
- anthonybelcher@csus.edu
- mboyle@csus.edu
- jaredshicks@csus.edu
- dvillasenor2@csus.edu
- chenwang@csus.edu
