import cx_Oracle
from enum import Enum
from verify_email import verify_email


class Connection:
    def __init__(self):
        self.connection = cx_Oracle.connect(
            user="admin",
            password="admin",
            dsn="DESKTOP-KQ6B5GR:1521/XEPDB1")

        self.cursor = self.connection.cursor()

    def user_exist(self, user, password):
        rs = self.cursor.execute('SELECT COUNT(*) from consumer where name = :1 and password = :2',
                            (user, password)).fetchone()
        if rs[0] == 1:
            return True, user
        else:
            rs = self.cursor.execute('SELECT COUNT(*) from consumer where email = :1 and password = :2',
                                (user, password)).fetchone()
            if rs[0] == 1:
                rs = self.cursor.execute('SELECT name from consumer where email = :1', user).fetchone()
                return True, rs[0]
            else:
                return False

    class CreateUserCode(Enum):
        SUCCESS = 0
        NAME_TAKEN = 1
        NAME_LENGTH = 2
        EMAIL_INCORRECT = 3
        EMAIL_LENGTH = 4
        EMAIL_TAKEN = 5
        PASSWORD_LENGTH = 6

    def create_user(self, username, email, password):
        if len(username) < 4 or len(username) > 20:
            return self.CreateUserCode.NAME_LENGTH
        if len(password) < 4 or len(password) > 20:
            return self.CreateUserCode.PASSWORD_LENGTH
        if len(email) > 20:
            return self.CreateUserCode.EMAIL_LENGTH
        rs = self.cursor.execute('SELECT COUNT(*) from consumer where name = :username', (username, )).fetchone()
        if rs[0] == 1:
            return self.CreateUserCode.NAME_TAKEN
        if not verify_email(email):
            return self.CreateUserCode.EMAIL_INCORRECT
        rs = self.cursor.execute('SELECT COUNT(*) from consumer where email = :email', (email, )).fetchone()
        if rs[0] == 1:
            return self.CreateUserCode.EMAIL_TAKEN
        self.cursor.execute(
            "insert into consumer (name, password, is_admin, email) values (:name, :password, 0, :email)",
            (username, password, email)
        )
        return self.CreateUserCode.SUCCESS

    def get_collections(self, username):
        return self.cursor.execute("""
            SELECT coll.name, coll.image
            from collection coll
            inner join consumer c
            on c.consumer_id = coll.consumer_id
            where c.name = :username
                and not c.name = 'General'
            order by coll.name
        """, (username, ))

    def create_collection(self, username, collection_name, description, image):
        self.cursor.execute('''
            insert into collection (name, consumer_id, description, image) 
            values (
                :collection_name, (select c.consumer_id from consumer c where c.name = :username), :description, :image
            )
            ''', (collection_name, username, description, image)
        )
        self.connection.commit()


connection = Connection()
