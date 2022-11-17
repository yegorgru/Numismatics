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
                return False, None

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
            SELECT coll.name, coll.image, coll.collection_id
            from collection coll
            inner join consumer c
            on c.consumer_id = coll.consumer_id
            where c.name = :username
            order by
                (CASE coll.name
                    WHEN 'General' THEN 2
                    ELSE 1
                END) DESC,
            coll.name DESC
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

    def get_collection_info(self, collection_id):
        return self.cursor.execute("""
                    SELECT name, description, image
                    from collection
                    where collection_id = :collection_id
                """, (collection_id,)).fetchone()

    def get_coins(self, collection_id):
        return self.cursor.execute("""
            SELECT coin.coin_id, td.value, currency.name, td.year, td.image_obverse
            from coin
            inner join collection_coin cc
                on cc.coin_id = coin.coin_id
            inner join collection c
                on c.collection_id = cc.collection_id
            inner join token_details td
                on coin.token_details_id = td.token_details_id
            inner join currency
                on currency.currency_id = td.currency_id
            where c.collection_id = :collection_id
        """, (collection_id,))

    def get_token_types(self):
        return self.cursor.execute("select type from token_type").fetchall()

    def get_edge_types(self):
        return self.cursor.execute("select name from edge").fetchall()

    def get_material_names(self):
        return self.cursor.execute("select name from material").fetchall()

    def get_currencies(self):
        return self.cursor.execute("select name, country from currency").fetchall()

    def create_token_details(
            self, value, currency_name, currency_country, year, token_type, material, image_obverse, image_reverse,
            description, subject
    ):
        type_id = self.cursor.execute('''select token_type_id from token_type
            where type = :type''', (token_type, )).fetchone()[0]
        material_id = self.cursor.execute('''select material_id from material
            where name = :name''', (material, )).fetchone()[0]
        currency_id = self.cursor.execute('''select currency_id from currency
            where name = :name and country = :country''', (currency_name, currency_country)).fetchone()[0]

        token_details_id = self.cursor.var(cx_Oracle.NUMBER)
        self.cursor.execute('''
            insert into token_details (
                value, currency_id, year, type_id, material_id, image_obverse, image_reverse, description, subject
            ) 
            values (
                :value, :currency_id, :year, :type_id, :material_id, :image_obverse, 
                :image_reverse, :description, :subject
            )
            returning token_details_id into :token_details_id
            ''', (value, currency_id, year, type_id, material_id, image_obverse, image_reverse, description, subject,
                  token_details_id)
        )
        self.connection.commit()
        return token_details_id.getvalue()[0]

    def create_coin_details(self, diameter, weight, edge):
        edge_id = self.cursor.execute('''select edge_id from edge
            where name = :name''', (edge, )).fetchone()[0]

        coin_details_id = self.cursor.var(cx_Oracle.NUMBER)
        self.cursor.execute('''
            insert into coin_details (
                diameter, weight, edge_id
            ) 
            values (
                :diameter, :weight, :edge_id
            )
            returning coin_details_id into :coin_details_id
            ''', (diameter, weight, edge_id, coin_details_id)
        )
        self.connection.commit()
        return coin_details_id.getvalue()[0]

    def create_coin(self, token_details_id, coin_details_id, collection_id):
        coin_id = self.cursor.var(cx_Oracle.NUMBER)
        self.cursor.execute('''
            insert into coin (
                token_details_id, coin_details_id
            ) 
            values (
                :token_details_id, :coin_details_id
            )
            returning coin_id into :coin_id
            ''', (token_details_id, coin_details_id, coin_id)
        )
        coin_id = coin_id.getvalue()[0]
        self.cursor.execute('''
           insert into collection_coin (
               coin_id, collection_id
           ) 
           values (
               :coin_id, :collection_id
           )
           ''', (coin_id, collection_id)
        )
        self.connection.commit()


connection = Connection()
