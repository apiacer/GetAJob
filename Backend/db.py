import sqlite3
import bcrypt
import threading
from abc import ABC, abstractmethod
DEBUG = True
DB_PATH = "test.db"
DEFULT_TAGS = ["test1", "test2", "test3", "test4", "test5"]

class Base:
    tables = []

    def __init__(self, db_path:str, debug:bool=False):
        self.name = None
        self.db_path = db_path
        self.debug = debug
    
    # sql 
    def _execute_sql(self, sql:str, params:list|tuple=None)->tuple[bool, list|None]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                if params is None:
                    cur.execute(sql)
                else:
                    cur.execute(sql, params)
                res = cur.fetchall()
                res = [dict(row) for row in res]
                if self.debug:
                    print(
                        f"---- debug info ----\n"
                        f"execute sql:\n{sql}\n\n"
                        f"params:\n{params}\n\n"
                        f"res:\n{res}\n\n"
                        f"----------------\n"
                    )
                return True, res
        
        except Exception as e:
            msg = (
                f"----error msg ----\n"
                f"SQL Error:\n{sql}\n\n"
                f"params: {params}\n\n"
                f"Error: {e}\n\n"
                f"----------------\n"
            )
            print(msg)
            return False, msg 
        
    def _sql_insert(self, param:dict)->tuple[bool, list|None]:
        param = {key:val for key, val in param.items() if val}
        columns = ", ".join(param.keys())
        placeholders = ", ".join("?" for _ in param) 
        val = list(param.values())
        sql= f"""INSERT INTO {self.name} ({columns}) VALUES ({placeholders})"""
        return self._execute_sql(sql, val)
    
    def _get_columns(self)->tuple[bool, list|None]:
        return self._execute_sql(f"PRAGMA table_info({self.name});")
    
class User(Base):
    def __init__(self, db_path:str, debug:bool = True):
        super().__init__(db_path, debug)
        self.name = "user"
        self._create_table()
        self._trigger_update_modify_time()
        User.tables.append(self.name)
        
    # utils for user
    @staticmethod
    def _hash(data:str)->bytes:
        hashed = bcrypt.hashpw(data.encode(), bcrypt.gensalt())
        return hashed

    def _validate_password(self, password:str)->tuple[bool, str]:
        # check password length
        if len(password) < 8:
            return False, "password too short"
        
        # check for special character requirement
        # if ["_", ".", "#", "@", "!"] not in password:
        #     return False, "need at least one special character"
        return True, "valid password"

    def _validate_user_name(self, user_name:str)->tuple[bool, str]:
        # check user name length
        if len(user_name) < 4:
            return False, "username too short"
        return True, "valid password"
    
    def _validate_phone(self, phone:str)->tuple[bool, str]:
        return True, "valid phone number"

    def _validate_email(self, email:str)->tuple[bool, str]:
        return True, "valid email"

    # sql
    def _create_table(self)->None:
        table = f"""
            CREATE TABLE IF NOT EXISTS {self.name} (
                user_id INTEGER PRIMARY KEY,
                user_name TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT UNIQUE,
                password_hash BLOB NOT NULL,
                age INTEGER,
                address TEXT,
                first_name TEXT,
                last_name TEXT,
                location TEXT,
                profile TEXT,
                pfp BLOB,
                avg_rating INTEGER,
                rate_num INTEGER,
                is_admin BOOLEAN DEFAULT 0,
                is_banned BOOLEAN DEFAULT 0,
                create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                modify_time DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """
        self._execute_sql(table)

    def _trigger_update_rating(self)->None:
        pass

    def _trigger_update_modify_time(self)->None:
        trigger = f"""
            CREATE TRIGGER IF NOT EXISTS update_user_modify_time
            AFTER UPDATE ON user
            FOR EACH ROW
            WHEN OLD.modify_time = NEW.modify_time
            BEGIN
                UPDATE user
                SET modify_time = CURRENT_TIMESTAMP
                WHERE user_id = OLD.user_id;
            END;
        """
        self._execute_sql(trigger)
    
    def create_account(self, user_name:str, password:str, email:str)->tuple[bool, str]:
        val_user_name = self._validate_user_name(user_name)
        val_password = self._validate_password(password)
        val_email = self._validate_email(email)
        msg = ""
        if not val_user_name[0]:
            msg += val_user_name[1] + "\n"

        if not val_email[0]:
            msg += val_email[1] + "\n"

        if not val_password[0]:
            msg += val_password[1] + "\n"

        if msg:
            return False, msg

        password_hash = self._hash(password)
        return self._sql_insert({"user_name":user_name, "password_hash":password_hash, "email":email})

    # log in
    def verify_password(self, user_name:str, password:str)->tuple[bool, str]:
        sql = f"""
            SELECT password_hash
            FROM {self.name}
            WHERE user_name = ?;
        """
        res = self._execute_sql(sql, user_name)
        
        if not res[0]:
            return res
        
        # Verify password with bcrypt
        if bcrypt.checkpw(password.encode(), res[1][0]):
            return True, "log in success"

        return False, "Invalid password"

    # user info
    def get_user_info(self, user_name:str=None, user_id:int=None, email:str=None)->tuple[bool, dict|str]:
        if user_name is None and user_id is None and email is None:
            return False, "please enter either user_name, user_id or email to get user info"
        
        elif user_name:
            condition_clause = "user_name"
            condition_val = user_name
        
        elif user_id:
            condition_clause = "user_id"
            condition_val = user_id

        elif email:
            condition_clause = "email"
            condition_val = email

        sql = f"""
            SELECT user_id, user_name, email, phone, age, address, first_name, last_name,
                location, profile, pfp, is_admin, is_banned, create_time, modify_time
            FROM {self.name}
            WHERE {condition_clause}=?;
        """
        res = self._execute_sql(sql, [condition_val, ])
        if not res[0]:
            return res
        if not res[1]:
            return False, "user not found"
        return res[0], res[1][0]
    
    def update_user_info(self, user_id:str, user_name:str=None, password:str=None, email:str=None, 
                            phone:str=None, age:int=None, address:str=None, 
                            first_name:str=None, last_name:str=None, location:str=None,
                            profile:str=None, pfp:str=None)->tuple[bool, str]:
        set_clause = []
        param = []
        error_msg = ""

        if user_name:
            res = self._validate_user_name(user_name)
            if res[0]:
                set_clause.append("user_name=?")
                param.append(user_name)
            else:
                error_msg += res[1]+"\n"

        if password:
            res = self._validate_password(password)
            if res[0]:
                set_clause.append("password_hash=?")
                param.append(self._hash(password))
            else:
                error_msg += res[1]+"\n"

        if email:
            res = self._validate_email(email)
            if res[0]:
                set_clause.append("email=?")
                param.append(email)
            else:
                error_msg += res[1]+"\n"

        if phone:
            res = self._validate_phone(phone)
            if res[0]:
                set_clause.append("phone=?")
                param.append(phone)
            else:
                error_msg += res[1]+"\n"

        if age:
            set_clause.append("age=?")
            param.append(age)

        if address:
            set_clause.append("address=?")
            param.append(address)

        if first_name:
            set_clause.append("first_name=?")
            param.append(first_name)

        if last_name:
            set_clause.append("last_name=?")
            param.append(last_name)

        if location:
            set_clause.append("location=?")
            param.append(location)

        if profile:
            set_clause.append("profile=?")
            param.append(profile)

        if pfp:
            set_clause.append("pfp=?")
            param.append(pfp)

        if not set_clause:
            return False, "no user info passed in to update"

        if error_msg:
            return False, error_msg

        param.append(user_id)

        sql = f"""
            UPDATE {self.name} 
            SET {", ".join(set_clause)}
            WHERE user_id=?
        """

        return self._execute_sql(sql, param)
    
    def clear_user_info(self, user_id:str, 
                            phone:bool=False, age:bool=False, address:bool=False, 
                            first_name:bool=False, last_name:bool=False, location:bool=False,
                            profile:bool=False, pfp:bool=False)->tuple[bool, str]:
        set_clause = []
        # username email not null
        if phone:
            set_clause.append("phone=None")

        if age:
            set_clause.append("age=None")

        if address:
            set_clause.append("address=None")

        if first_name:
            set_clause.append("first_name=None")

        if last_name:
            set_clause.append("last_name=None")

        if location:
            set_clause.append("location=None")

        if profile:
            set_clause.append("profile=None")

        if pfp:
            set_clause.append("pfp=None")

        if not set_clause:
            return False, "no user fields set to None"
        
        sql = f"""
            UPDATE {self.name} 
            SET {", ".join(set_clause)}
            WHERE user_id=?
        """

        return self._execute_sql(sql, [user_id])

    def delete_user(self, user_name:str=None, user_id:str=None, email:str=None):
        if user_id is None and user_name is None and email is None:
            return False, "please enter either user_name, user_id or email to delete user"
        
        elif user_name:
            condition_clause = "user_name"
            condition_val = user_name

        elif user_id:
            condition_clause = "user_id"
            condition_val = user_id

        elif email:
            condition_clause = "email"
            condition_val = email

        sql = f"""
            DELETE FROM {self.name}
            WHERE {condition_clause}=?
        """

        return self._execute_sql(sql, [condition_val])
    
    # admin
    def admin_action(self, user_name:str=None, user_id:int=None, email:str=None, is_banned:bool=None, is_admin:bool=None):
        if not user_name and not user_id and not email:
            return False, "please enter either user_name, user_id or email"

        if not is_admin and not is_banned:
            return False, "please enter an action to perform"
        elif user_name:
            condition_clause = "user_name"
            condition_val = user_name
        
        elif user_id:
            condition_clause = "user_id"
            condition_val = user_id

        elif email:
            condition_clause = "email"
            condition_val = email

        if is_banned:
            sql = f"""
                UPDATE {self.name}
                SET is_banned=1
                WHERE {condition_clause}=?
            """
            return self._execute_sql(sql, [condition_val])
        
        if is_admin:
            sql = f"""
                UPDATE {self.name}
                SET is_admin=1
                WHERE {condition_clause}=?
            """
            return self._execute_sql(sql, [condition_val])
    
    def get_all_banned_user(self)->tuple[bool, list]:
        sql = f"""
            SELECT * 
            FROM {self.name}
            WHERE is_banned=1
        """
        return self._execute_sql(sql)
    

class Post(Base):
    def __init__(self, db_path, debug = False):
        super().__init__(db_path, debug)
        self.name="post"
        
    def _create_table(self):
        sql = f"""
            CREATE TABLE IF NOT EXIST {self.name}
            post_id INTERGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            owner_id INTERGER NOT NULL REFERENCES user(user_id) ON DELETE CASCADE,
            location TEXT,
            budget TEXT,
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            modify_time DATETIME DEFAULT CURRENT_TIMESTAMP
        """

        return self._execute_sql(sql)
    
    def _trigger_update_modify_time(self):
        sql = f"""
            CREATE TRIGGER IF NOT EXISTS update_post_modify_time
            AFTER UPDATE ON post
            FOR EACH ROW
            WHEN OLD.modify_time = NEW.modify_time
            BEGIN
                UPDATE post
                SET modify_time = CURRENT_TIMESTAMP
                WHERE post_id = OLD.post_id;
            END;
        """

        return self._execute_sql(sql)
    
    def create_post(self, title:str, description:str, owner_id:int, location:str=None, budget:str=None):
        return self._sql_insert({"title":title, "description":description, "owner_id":owner_id, "location":location, "budget":budget})
    
    def update_post(self, post_id:int, title:str=None, description:str=None, locaiton:str=None, budget:str=None):
        set_clause = []
        param = []

        if title:
            set_clause.append("title=?")
            param.append(title)

        if description:
            set_clause.append("description=?")
            param.append(description)

        if locaiton:
            set_clause.append("location=?")
            param.append(locaiton)

        if budget:
            set_clause.append("budget=?")
            param.append(budget)

        if not set_clause:
            return False, "no post info passed in to update"
        
        param.append(post_id)
        sql = f"""
            UPDATE {self.name}
            SET {", ".join(set_clause)}
            WHERE post_id=?
        """
        return self._execute_sql(sql, param)

    def delete_post(self, post_id:int):
        sql = f"""
        DELETE FROM {self.name}
        WHERE post_id=?
        """
        return self._execute_sql(sql, [post_id])
    
    def select_post(self, post_id:int):
        sql = f"""
        SELECT * FROM {self.name}
        WHERE post_id=?
        """
        return self._execute_sql(sql, [post_id])

    def select_user_post(self, user_id:int):
        sql = f"""
        SELECT * FROM {self.name}
        WHERE user_id=?
        """
        return self._execute_sql(sql, [user_id])

    def search_posts(self, limit: int = 10, offset: int = 0,
                    tags: list = None, key_words: list = None):
        
        key_words = key_words or []   # ensure list
        tags = tags or []             # ensure list

        sql = """
            SELECT p.*
            FROM posts p
        """

        # Only join tag tables if tags are provided
        if tags:
            sql += """
                JOIN post_tag pt ON p.post_id = pt.post_id
                JOIN tags t ON pt.tag_id = t.tag_id
            """

        sql += " WHERE 1=1 "  # simplifies conditional appending

        conditions = []
        params = []

        # Keyword conditions (match ALL)
        for kw in key_words:
            conditions.append("(p.title LIKE ? OR p.content LIKE ?)")
            like = f"%{kw}%"
            params.extend([like, like])

        # Tag filter (match ALL tags)
        if tags:
            # only filter after JOIN
            placeholders = ",".join("?" for _ in tags)
            conditions.append(f"t.tag_name IN ({placeholders})")
            params.extend(tags)

        # Add WHERE conditions
        if conditions:
            sql += " AND " + " AND ".join(conditions)

        # Apply HAVING only when tags exist
        if tags:
            sql += " GROUP BY p.post_id HAVING COUNT(DISTINCT t.tag_name) = ?"
            params.append(len(tags))

        sql += " ORDER BY p.create_time DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        return self._execute_sql(sql, params)


class Db_api:
    def __init__(self, db_path:str=None, debug:bool=True):
        if not db_path:
            db_path = DB_PATH

        self.user = User(db_path, debug)
        self.post = Post(db_path, debug)
        
if __name__ == "__main__":
    Db_api(DB_PATH, DEBUG)
