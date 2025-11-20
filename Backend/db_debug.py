from db import Db_api, DB_PATH
import random
import os


def delete_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_post(db:Db_api):
    print("---- test all post functions")
    print("create new post")
    res = db.post.create_post("test_title", "test_description", 1)
    res = db.post.create_post("test_title0", "test_description0", 1)
    print(res)
    print()
    print("create post with non-exist user (test if foreign key constraint works)")
    res = db.post.create_post("test_title", "test_description", 1000)
    print(res)
    print()
    print("select post by id")
    res = db.post.select_post(1)
    print(res)
    print()
    print("select non-exist post by id")
    res = db.post.select_post(100)
    print(res)
    print()
    print("select post own by user id 1")
    res = db.post.select_user_post(1)
    print(res)
    print()
    print("select post own by non-exist user")
    res = db.post.select_user_post(1000)
    print(res)
    print()
    print("modify post")
    res = db.post.update_post(1, "new title", "new description", "my location", "0-100")
    print(res)
    print()
    print("select 10 latest post")
    res = db.post.select_latest_n_posts()
    print(f"data length: {len(res[1])}")
    print(res)
    print()
    print(f"delete user_id=1 (test for on delete cascade)")
    res = db.post.select_latest_n_posts(None)
    print(f"post num before delete: {len(res[1])}")
    res = db.user.delete_user(user_id=1)
    print(f"delete user: {res}")
    res = db.post.select_latest_n_posts(None)
    print(f"post num after delete: {len(res[1])}")
    print()

def test_message(db:Db_api):
    pass

def test_post_tag(db:Db_api):
    pass

def test_tag(db:Db_api):
    pass

def test_user_report(db:Db_api):
    pass

# do we need a post report seperate from user report? 
def test_post_report(db:Db_api):
    pass

# all test case success
def test_user(db:Db_api):
    # test create account
    print("---- test create account ----")
    print("insert invalid user:")
    res = db.user.create_account("1", "12345678", "example@gmail.com")
    print(res)
    print()
    print("insert a user:")
    res = db.user.create_account("test_user", "test_password", "example@gmail.com")
    print(res)
    print()
    print("insert duplicate user:")
    res = db.user.create_account("test_user", "test_password", "example@gmail.com")
    print(res)
    print()

    # test get/update user profile
    print("---- test get user info ----" )
    print("get user by user name")
    res = db.user.get_user_info(user_name="test_user")
    print(res)
    print()
    print("get user by user id")
    res = db.user.get_user_info(user_id=res[1]["user_id"])
    print(res)
    print()
    print("get user by email")
    res = db.user.get_user_info(email="example@gmail.com")
    print(res)
    print()
    print("get non-exist user by user name")
    res = db.user.get_user_info("do_not_exist")
    print(res)
    print()
    os.system("pause")


    print("update user profile")
    res = db.user.update_user_info("test_user", email="new@gmail.com", phone="1234567890", first_name="user_frist_name", last_name="user_last_name")
    print(res)
    print()
    print("get user info after updated")
    res = db.user.get_user_info("test_user")
    print(res)
    print()
    
    # test ban/if_banned/unban function
    print("---- test ban/if_banned/unban function ----")
    print("ban user")
    res = db.user.ban_user("test_user")
    print(res)
    print()
    print("check if user is banned")
    res = db.user.get_user_info("test_user")
    print(res)
    print()
    print("check all banned user")
    res = db.user.get_all_banned_user()
    print(res)
    print()
    print("unban user")
    res = db.user.unban_user("test_user")
    print(res)
    print()
    print("check if user is banned")
    res = db.user.get_user_info("test_user")    
    print(res)
    print()
    
    # test verify/update password
    print("---- test verify/update password ----")
    print("verify password (if login) with wrong password")
    res = db.user.verify_password("test_user", "test")
    print(res)
    print()
    print("verify password with correct password")
    res = db.user.verify_password("test_user", "test_password")
    print(res)
    print()
    print("update password")
    res = db.user.update_password("test_user", "new_password")
    print(res)
    print()
    print("verify with old password")
    res = db.user.verify_password("test_user", "test_password")
    print(res)
    print()
    print("verify with new password")
    res = db.user.verify_password("test_user", "new_password")
    print(res)
    print()

    print("---- test update user name / delete user ----")
    print("update user name")
    res = db.user.update_user_name("new_user", "test_user")
    print(res)
    print()
    print("delete user with old name")
    res = db.user.delete_user("test_user")
    print(res)
    print()
    print("delete user with new name")
    res = db.user.delete_user("new_user")
    print(res)
    print()

def apply_test_data(db:Db_api):
    print("---- insert test users ----")
    # generate test user
    test_user = [{"user_name":f"test_user{n+1}", "email":f"test_email{n+1}", "password":f"test_password{n+1}"} for n in range(10)]
    for i in test_user:
        res = db.user.create_account(i["user_name"], i["password"], i["email"])
        print(f"add {i['user_name']}: {res}")

    # # generate test posts
    # test_post = [{"title":f"test_title{n+1}", "description":f"test_description{n+1}", "owner_id":random.randint(1, 10)} for n in range(10)]
    # for i in test_post:
    #     res = db.create_post(i["title"], i["description"], i["owner_id"])
    #     print(f"add new post: {res}")

    print("---- finish adding test data ----\n")

if __name__ == "__main__":
    delete_db()
    db = Db_api()
    apply_test_data(db)
    test_user(db)
    # test_post(db)
    # db.terminal()
