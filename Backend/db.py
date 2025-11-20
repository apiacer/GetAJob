import sqlite3
import bcrypt
import threading
import re

DB_PATH = "test.db"
DEFULT_TAGS = ["test1", "test2", "test3", "test4", "test5"]
    
class Base:
    def __init__(self, cur:sqlite3.Cursor, conn:sqlite3.Connection, name:str, field:dict):
        self._lock = threading.Lock()
        self._cur = cur
        self._conn = conn
        self._name = name
        self._field = field

        self._create_table()

    # ----util----
    @staticmethod
    def _hash(data:str)->bytes:
        hashed = bcrypt.hashpw(data.encode(), bcrypt.gensalt())
        return hashed
    
    def _validate_columns(self, column_name:list)->tuple[bool, str]:
        # Validate all columns
        for column in column_name:
            if column not in self._field:
                # add logger later
                return False, f"invalid column: {column}"
            
        return True, "all column valid"

    # ----sql operation----
    def _create_table(self)->None:
        ### fix create table with constraints
        field = ", ".join([key+" "+" ".join(val) for key, val in self._field.items()])
        # test 
        # print(f"CREATE TABLE IF NOT EXISTS {self._name} ({field})")
        with self._lock:
            self._cur.execute(f"CREATE TABLE IF NOT EXISTS {self._name} ({field})")
            self._conn.commit()

    def _insert_data(self, data:dict)->tuple[bool, str]:
        try:
            # Validate all columns
            # print(data)
            v = self._validate_columns(data.keys())
            if not v[0]:
                return v
                
            columns = ", ".join(data.keys())
            placeholders = ", ".join("?" for _ in data) 
            val = list(data.values())
            with self._lock:
                self._cur.execute(f"""
                    INSERT INTO {self._name} ({columns}) VALUES ({placeholders})
                """, val)
                self._conn.commit()
            return True, "success"

        except sqlite3.Error as e:
            error_msg = f"insert failed: {e}"
            # add logger later
            self._conn.rollback()
            return False, error_msg
        
    # warning please always send in both params or will deletes all rows
    def _delete_data(self, condition_clause:str="1=1", condition_val:list=[])->tuple[bool, str]:
        try:
            # check if user exist
            res = self._select_data(condition_clause, condition_val)
            if not res[0]:
                return res
            
            with self._lock:
                self._cur.execute(f"""
                DELETE FROM {self._name} WHERE {condition_clause}
                """, condition_val)

                self._conn.commit()

            # check if user still exist
            res = self._select_data(condition_clause, condition_val)
            if res[0]:
                return False, "delete failed: user still exist after deleting"
            
            return True, "success"
        
        except sqlite3.Error as e:
            error_msg = f"delete failed: {e}"
            # add logger later
            self._conn.rollback()
            return False, error_msg

    def _select_data(self, condition_clause:str="1=1", condition_val:list=[], column:list[str]=["*"])->tuple[bool, list[dict]|str]:
        try:
            column = ", ".join(column)
            with self._lock:
                self._cur.execute(f"""
                SELECT {column} FROM {self._name}
                    WHERE {condition_clause}
                """, condition_val)

                rows = self._cur.fetchall()
                rows = [dict(row) for row in rows]
                # if select is empty
                if not rows:
                    return False, "data not found"
            
                return True, rows
        
        except sqlite3.Error as e:
            error_msg = f"select failed: {e}"
            return False, error_msg
    
    def _update_data(self, new_data:dict, condition_clause:str="1=1", condition_val:list=[])->tuple[bool, str]:
        try:
            # key validation check
            check = self._validate_columns(new_data.keys())
            if not check[0]:
                return False, check[1]
            
            # config set res
            set_clause = ", ".join([f"{key}=?" for key in new_data.keys()])
            set_val = list(new_data.values())
            
            val = set_val+condition_val
            with self._lock:
                self._cur.execute(f"""
                UPDATE {self._name} SET {set_clause}
                WHERE {condition_clause}
                """, val)
                self._conn.commit()
            return True, "success"
        
        except sqlite3.Error as e:
            error_msg = f"[WARN] update failed: {e}"
            # add logger later
            self._conn.rollback()
            return False, error_msg
 
class User(Base):
    def __init__(self, cur, conn):
        field = {
            "user_id": ["INTEGER", "PRIMARY KEY"],
            "user_name": ["TEXT", "UNIQUE", "NOT NULL"],
            "email": ["TEXT", "UNIQUE", "NOT NULL"],
            "phone": ["TEXT", "UNIQUE"],
            "password_hash": ["BLOB", "NOT NULL"],
            "age": ["INTEGER", ],
            "address": ["TEXT",],
            "first_name": ["TEXT", ],
            "last_name": ["TEXT", ],
            "location": ["TEXT", ],
            "profile": ["TEXT", ],
            "pfp":["BLOB"],
            "is_admin": ["BOOLEAN", "DEFAULT 0"],
            "is_banned": ["BOOLEAN", "DEFAULT 0"],
            "report_id": ["INTEGER", "UNIQUE"],
            "create_time": ["DATETIME", "DEFAULT CURRENT_TIMESTAMP"],
            "modify_time": ["DATETIME", "DEFAULT CURRENT_TIMESTAMP"]
        }
        super().__init__(cur=cur, conn=conn, field=field, name="user")
        self._trigger_update_modify_time()

    # auto update after update
    def _trigger_update_modify_time(self):
        self._cur.execute("""
            CREATE TRIGGER IF NOT EXISTS update_user_modify_time
            AFTER UPDATE ON user
            FOR EACH ROW
            WHEN OLD.modify_time = NEW.modify_time
            BEGIN
                UPDATE user
                SET modify_time = CURRENT_TIMESTAMP
                WHERE user_id = OLD.user_id;
            END;
        """)
        self._conn.commit()

    # utils
    def _validate_password(self, password:str)->tuple[bool, str]:
        # check password length
        if len(password) < 8:
            return False, "password too short"
        
        # check for special character requirement
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, password):
            return False, "password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
        return True, "valid password"

    def _validate_user_name(self, user_name:str)->tuple[bool, str]:
        # check user name length
        if len(user_name) < 4:
            return False, "username too short"
        return True, "valid username"
    
    def _validate_phone(self, phone:str)->tuple[bool, str]:
        pass

    def _validate_email(self, email:str)->tuple[bool, str]:
        pass

    # actions
    
    def create_account(self, user_name:str, password:str, email:str, first_name:str=None, last_name:str=None)->tuple[bool, str]:
        # check requirement 
        v1 = self._validate_password(password)
        v2 = self._validate_user_name(user_name)
        if not v1[0] and not v2[0]:
            return False, v1[1]+" "+v2[1]
        
        if not v1[0]:
            return v1
        
        if not v2[0]:
            return v2

        param = {"user_name":user_name, "password_hash":self._hash(password), "email":email, "first_name": first_name, "last_name": last_name}
        # remove any None fields (if blank)
        param = {k: v for k, v in param.items() if v is not None}
        return super()._insert_data(param)
    
    # get
    def get_user_profile(self, user_name:str)->tuple[bool, dict|str]:
        res = self._select_data("user_name=?", [user_name], 
        ["email", "phone", "age", "address", "first_name", "last_name", 
         "location", "profile", "pfp"])
        if not res[0]:
            return res
        
        return True, res[1][0]
    
    def if_user_banned(self, user_name:str)->tuple[bool, bool|str]:
        res = self._select_data("user_name=?", [user_name], ["is_banned"])
        if not res[0]:
            return res
        
        return True, bool(res[1][0]["is_banned"])

    def get_user_id(self, user_name:str)->tuple[bool, int|str]:
        res = self._select_data("user_name=?", [user_name], ["user_id"])
        if not res[0]:
            return res
        return True, res[1][0]["user_id"]

    # log in
    def verify_password(self, user_name:str, password:str)->tuple[bool, str]:
        try:
            res = self._select_data("user_name=?", [user_name], ["password_hash"])
            if not res[0]:
                return False, res[1]
            
            if bcrypt.checkpw(password.encode(), res[1][0]['password_hash']):
                return True, "log in success"
            
            return False, "Invalid password"
        except Exception as e:
            return False, f"Verification failed: {e}"

    # updates
    def update_user_name(self, new_user_name:str, old_user_name:str)->tuple[bool, str]:
        # check reqirements
        v = self._validate_user_name(new_user_name)
        if not v[0]:
            return v
        
        return self._update_data({"user_name": new_user_name}, "user_name=?", [old_user_name])
    
    def update_password(self, user_name:str, new_password:str)->tuple[bool, str]:
        v = self._validate_password(new_password)
        if not v[0]:
            return v
        
        return self._update_data({"password_hash": self._hash(new_password)}, "user_name=?", [user_name])

    def update_user_profile(self, user_name:str, email:str=None, phone:str=None, 
                            age:int=None, address:str=None, first_name:str=None, 
                            last_name:str=None, location:str=None,
                            profile:str=None, pfp=None):
        param = {
            "email":email, "phone":phone, "age":age, "address":address, "first_name":first_name,
            "last_name":last_name, "location":location, "profile":profile, "pfp":pfp
        }
        param = {k: v for k, v in param.items() if v is not None}

        return self._update_data(param, "user_name=?", [user_name])

    # admin
    def ban_user(self, user_name:str)->tuple[bool, str]:
        return self._update_data({"is_banned":1}, "user_name=?", [user_name])

    def unban_user(self, user_name:str)->tuple[bool, str]:
        return self._update_data({"is_banned":0}, "user_name=?", [user_name])

    # delete account
    def delete_user(self, user_name:str):
        return self._delete_data(f"user_name=?", [user_name])

class Post(Base):
    def __init__(self, cur, conn):
        field = {
            "post_id": ["INTEGER", "PRIMARY KEY"],
            "title": ["TEXT", "NOT NULL"],
            "description": ["TEXT", "NOT NULL"],
            "owner_id": ["INTEGER", "NOT NULL", "REFERENCES user(user_id) ON DELETE CASCADE"],
            "create_time": ["DATETIME", "DEFAULT CURRENT_TIMESTAMP"],
            "modify_time": ["DATETIME", "DEFAULT CURRENT_TIMESTAMP"],
        }
        super().__init__(cur=cur, conn=conn, name="post", field=field)

    def create_post(self, title:str, description:str, owner_id:int):
        return self._insert_data({"title":title, "description":description, "owner_id":owner_id})

    def delete_post(self, post_id:int):
        return self._delete_data("post_id=?", [post_id])

    def update_post(self, post_id:int, title:str=None, description:str=None):
        return self._update_data({"title":title, "description":description}, "post_id=?", [post_id])

    def select_post(self, post_id:int):
        return self._select_data("post_id=?", [post_id])
    
    def select_user_post(self, user_id:int):
        return self._select_data("owner_id=?", [user_id])

    def get_latest_n_post(self, n:int=10):
        return self._select_data()
    
class Message(Base):
    def __init__(self, cur, conn):
        field = {
            "message_id":["INTEGER", "PRIMARY KEY"],
            "sender_id":["INTEGER", "NOT NULL", "REFERENCES user(user_id)"],
            "receiver_id":["INTEGER", "NOT NULL", "REFERENCES user(user_id)"],
            "if_read":["BOOLEAN", "DEFAULT 0"],
            "message":["TEXT", "NOT NULL"],
            "timestamp":["DATETIME", "DEFAULT CURRENT_TIMESTAMP"],
        }
        super().__init__(cur=cur, conn=conn, name="message", field=field)

    def get_chat_room(self, user1:int, user2:int):
        return self._select_data("(sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)", [user1, user2, user2, user1])

    def read(self, sender_id:int, receiver_id:int):
        return self._update_data({"if_read":1}, "sender_id=? AND receiver_id=?", [sender_id, receiver_id])

    def send_message(self, sender_id:int, receiver_id:int, msg:str):
        return self._insert_data({"sender_id":sender_id, "receiver_id":receiver_id, "message":msg})
    
class Post_tag(Base):
    def __init__(self, cur, conn):
        field = {
            "post_id": ["INTEGER", "NOT NULL", "REFERENCES post(post_id) ON DELETE CASCADE"],
            "tag_id": ["INTEGER", "NOT NULL", "REFERENCES tag(tag_id) ON DELETE CASCADE"],
            "PRIMARY KEY": ["(post_id, tag_id)"]
        }

        super().__init__(cur=cur, conn=conn, name="post_tag", field=field)

    def add_tag_to_post(self, post_id:int, tag_id:int):
        return self._insert_data({"post_id":post_id, "tag_id":tag_id})

    def delete_tag_from_post(self, post_id:int, tag_id:int):
        return self._delete_data({"post_id":post_id, "tag_id":tag_id})

    def get_tagged_post_id(self, tag_id:int):
        res = self._select_data("tag_id=?", [tag_id], ["post_id"])
        if not res[0]:
            return res
        return True, [val["post_id"] for val in res[1]]
    
class Tag(Base):
    def __init__(self, cur, conn):
        field = {
            "tag_id": ["INTEGER", "PRIMARY KEY"],
            "tag_name": ["TEXT", "UNIQUE", "NOT NULL"]
        }

        super().__init__(cur=cur, conn=conn, name="tag", field=field)

        # load defult tag
        for tag in DEFULT_TAGS:
            self.create_tag(tag)

    def create_tag(self, tag_name:str)->tuple[bool, str]:
        return self._insert_data({"tag_name": tag_name})

    def delete_tag(self, tag_name:str)->tuple[bool, str]:
        return self._delete_data("tag_name=?", [tag_name])

    def get_tag_id(self, tag_name:str):
        res = self._select_data("tag_name=?", [tag_name], ["tag_id"])
        if not res[0]:
            return res
        return True, res[1][0]["tag_id"]
    
class User_report(Base):
    def __init__(self, cur, conn):
        field = {
            "report_id": ["INTEGER", "PRIMARY KEY"],
            "user_id": ["INTEGER", "NOT NULL", "REFERENCES user(user_id)"],
            "description": ["TEXT", "NOT NULL"]
        }
        super().__init__(cur=cur, conn=conn, name="user_report", field=field)

    # user
    def report_user(self, user_id:int, description:str)->tuple[bool, str]:
        return self._insert_data({"user_id":user_id, "description":description})

    # admin
    def get_reported_users(self)->tuple[bool, list[str]|str]:
        return self._select_data(column=["DISTINCT user_id"])

    def get_user_reports(self, user_id:int)->tuple[bool, list[str]|str]:
        return self._select_data("user_id=?", [user_id], ["report_id", "description"])

    def delete_report(self, report_id:int)->tuple[bool, str]:
        return self._delete_data("report_id=?", [report_id])


class Database_api:
    def __init__(self, db_path:str=DB_PATH):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)

        # set return sqlite3.Row objects when selecting
        self._conn.row_factory = sqlite3.Row
        
        self._cur = self._conn.cursor()

        # load all table
        self.tag = Tag(self._cur, self._conn)
        self.user = User(self._cur, self._conn)
        self.message = Message(self._cur, self._conn)
        self.post = Post(self._cur, self._conn)
        self.post_tag = Post_tag(self._cur, self._conn)
        self.report = User_report(self._cur, self._conn)

        # enforce foreign key after load all tables
        self._conn.execute("PRAGMA foreign_keys = ON;")
        self._conn.commit()

    # call terminal to manual check databse for debug 
    def terminal(self):
        print("in terminal")
        while True:
            msg = input()
            if msg == "commit":
                self._conn.commit()

            elif msg == "rollback":
                self._conn.rollback()

            elif msg == "q":
                print("quit terminal")
                break

            try:
                self._cur.execute(msg)
                rows = self._cur.fetchall()
                rows = [dict(row) for row in rows]
                print(rows)
            except Exception as e:
                print(e)

### add update modify time on all update function