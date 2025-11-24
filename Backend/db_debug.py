from db import Db_api, DB_PATH
import os


# ---------------------------------------------------
# Utility: Delete old DB
# ---------------------------------------------------
def delete_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


# ---------------------------------------------------
# Test User Module
# ---------------------------------------------------
def test_user(db: Db_api):
    print("\n==== TEST USER MODULE ====\n")

    print("1. Insert small invalid username:")
    print(db.user.create_account("1", "pass1234", "u1@mail"))
    print()

    print("2. Insert valid user:")
    print(db.user.create_account("test_user", "test_password", "example@gmail.com"))
    print()

    print("3. Insert duplicate user:")
    print(db.user.create_account("test_user", "test_password", "example@gmail.com"))
    print()

    print("4. Get by username:")
    print(db.user.get_user_info("test_user"))
    print()

    print("5. Update profile:")
    print(db.user.update_user_info(
        "test_user",
        email="new@mail",
        first_name="John",
        last_name="Doe",
        phone="12345"
    ))
    print()

    print("8. Delete user:")
    print(db.user.delete_user("test_user"))
    print()

    print("9. verify_password")
    print(db.user.verify_password("dne", "dne"))

# ---------------------------------------------------
# Test Post Module
# ---------------------------------------------------
def test_post(db: Db_api):
    print("\n==== TEST POST MODULE ====\n")

    print("1. Create posts owned by users 1,2,3:")
    p1 = db.post.create_post("T1", "D1", 1)
    p2 = db.post.create_post("T2", "D2", 2)
    p3 = db.post.create_post("T3", "D3", 3)
    print(p1, p2, p3)
    print()

    print("2. Create invalid post (FK fail):")
    print(db.post.create_post("Bad", "Bad", 9999))
    print()

    print("3. Select post by ID:")
    print(db.post.select_post(1))
    print()

    print("4. Update post:")
    print(db.post.update_post(1, "Updated", "Updated Desc", "LA", "100-200"))
    print()



# ---------------------------------------------------
# Test Tag Module
# ---------------------------------------------------
def test_tag(db: Db_api):
    print("\n==== TEST TAG MODULE ====\n")

    print("1. Create tags:")
    print(db.tag.create_tag("food"))
    print(db.tag.create_tag("sport"))
    print(db.tag.create_tag("music"))
    print()

    print("2. Duplicate tag:")
    print(db.tag.create_tag("food"))
    print()

    print("3. Fetch tag ID:")
    print("sport id:", db.tag.get_tag_id("sport"))
    print()

    print("4. Delete tag:")
    print(db.tag.delete_tag("music"))
    print()


# ---------------------------------------------------
# Test Post-Tag Module
# ---------------------------------------------------
def test_post_tag(db: Db_api):
    print("\n==== TEST POST_TAG MODULE ====\n")

    # ensure data exists
    db.post.create_post("Food post", "desc", 1)
    db.post.create_post("Sport post", "desc", 2)

    t_food = db.tag.get_tag_id("food")[1]
    t_sport = db.tag.get_tag_id("sport")[1]

    print("1. Add tags to posts:")
    print(db.post_tag.add_tag2post(1, t_food))
    print(db.post_tag.add_tag2post(1, t_sport))
    print(db.post_tag.add_tag2post(2, t_sport))
    print()

    print("2. Add duplicate relation (ignored):")
    print(db.post_tag.add_tag2post(1, t_food))
    print()

    print("3. Remove tag:")
    print(db.post_tag.delete_post_tag(1, t_food))
    print()

    print("4. Remove non-existing relation:")
    print(db.post_tag.delete_post_tag(1, 99999))
    print()


# ---------------------------------------------------
# Test Message Module
# ---------------------------------------------------
def test_message(db: Db_api):
    print("\n==== TEST MESSAGE MODULE ====\n")

    print("1. Send valid messages:")
    print(db.message.send_message(2, 3, "Hello from 2 to 3"))
    print(db.message.send_message(3, 2, "Reply from 3"))
    print(db.message.send_message(2, 3, "Another one"))
    print()

    print("2. Invalid sender/receiver (FK fail):")
    print(db.message.send_message(999, 3, "Bad sender"))
    print(db.message.send_message(2, 999, "Bad receiver"))
    print()

    print("3. List conversation (2 ↔ 3):")
    print(db.message.get_room(2, 3))
    print()

    print("4. Mark messages read (sender 3 → receiver 2):")
    print(db.message.read(3, 2))
    print()

    print("5. Check messages after read:")
    print(db.message.get_room(2, 3))
    print()


# ---------------------------------------------------
# Test data seeding
# ---------------------------------------------------
def seed_users(db:Db_api):
    print("---- inserting 3 users ----")
    for i in range(1, 4):
        db.user.create_account(f"user{i}", f"pass{i}", f"user{i}@mail")
    print("---- done ----\n")


# ---------------------------------------------------
# Main Runner
# ---------------------------------------------------
if __name__ == "__main__":
    delete_db()
    db = Db_api(debug=False)

    seed_users(db)

    test_user(db)
    test_post(db)
    test_tag(db)
    test_post_tag(db)
    test_message(db)

    print("\n==== ALL TESTS COMPLETE ====\n")
