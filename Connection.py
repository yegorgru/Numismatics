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
        rs = self.cursor.execute(
            'SELECT name from consumer where (name = :name or email = :email) and password = :password',
            (user, user, password)
        ).fetchone()
        if rs is None:
            return False, None
        else:
            return True, rs[0]

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

    def get_collections_preview(self, username):
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

    def get_coins_preview(self, collection_id):
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

    def create_coin(self, value, currency_name, currency_country, year, token_type, material, image_obverse,
                    image_reverse, description, subject, diameter, weight, edge, collection_id):
        self.cursor.execute('''
            DECLARE
                var_token_type_id    NUMBER;
                var_material_id      NUMBER;
                var_currency_id      NUMBER;
                var_token_details_id NUMBER;
                var_edge_id          NUMBER;
                var_coin_details_id  NUMBER;
                var_coin_id          NUMBER;
            BEGIN
                SELECT
                    token_type_id
                INTO var_token_type_id
                FROM
                    token_type
                WHERE
                    type = :type;
            
                SELECT
                    material_id
                INTO var_material_id
                FROM
                    material
                WHERE
                    name = :material_name;
            
                SELECT
                    currency_id
                INTO var_currency_id
                FROM
                    currency
                WHERE
                        name = :currency_name
                    AND country = :country;
            
                INSERT INTO token_details (
                    value,
                    currency_id,
                    year,
                    type_id,
                    material_id,
                    image_obverse,
                    image_reverse,
                    description,
                    subject
                ) VALUES (
                    :value,
                    var_currency_id,
                    :year,
                    var_token_type_id,
                    var_material_id,
                    :image_obverse,
                    :image_reverse,
                    :description,
                    :subject
                ) RETURNING token_details_id INTO var_token_details_id;
            
                SELECT
                    edge_id
                INTO var_edge_id
                FROM
                    edge
                WHERE
                    name = :edge_name;
            
                INSERT INTO coin_details (
                    diameter,
                    weight,
                    edge_id
                ) VALUES (
                    :diameter,
                    :weight,
                    var_edge_id
                ) RETURNING coin_details_id INTO var_coin_details_id;
            
                INSERT INTO coin (
                    token_details_id,
                    coin_details_id
                ) VALUES (
                    var_token_details_id,
                    var_coin_details_id
                ) RETURNING coin_id INTO var_coin_id;
            
                INSERT INTO collection_coin (
                    coin_id,
                    collection_id
                ) VALUES (
                    var_coin_id,
                    :collection_id
                );
                
                COMMIT;
            END;
            ''', (token_type, material, currency_name, currency_country, value, year, image_obverse, image_reverse,
                  description, subject, edge, diameter, weight, collection_id)
        )

    def get_coin(self, coin_id):
        return self.cursor.execute("""
            SELECT
                td.value,
                currency.name,
                currency.country,
                td.year,
                token_type.type,
                material.name,
                td.image_obverse,
                td.image_reverse,
                td.description,
                td.subject,
                cd.diameter,
                cd.weight,
                edge.name
            FROM
                     coin
                INNER JOIN token_details td ON td.token_details_id = coin.token_details_id
                INNER JOIN coin_details  cd ON cd.coin_details_id = coin.coin_details_id
                INNER JOIN currency ON td.currency_id = currency.currency_id
                INNER JOIN token_type ON td.type_id = token_type.token_type_id
                INNER JOIN material ON td.material_id = material.material_id
                INNER JOIN edge ON cd.edge_id = edge.edge_id
            WHERE
                coin.coin_id = :coin_id
        """, (coin_id, )).fetchone()

    def update_coin(self, coin_id, value, currency_name, currency_country, year, token_type, material, image_obverse,
                    image_reverse, description, subject, diameter, weight, edge):
        self.cursor.execute('''
            DECLARE
                var_token_type_id    NUMBER;
                var_material_id      NUMBER;
                var_currency_id      NUMBER;
                var_token_details_id NUMBER;
                var_edge_id          NUMBER;
                var_coin_details_id  NUMBER;
            BEGIN
                SELECT
                    token_details_id,
                    coin_details_id
                INTO
                    var_token_details_id,
                    var_coin_details_id
                FROM
                    coin
                WHERE
                    coin_id = :coin_id;
            
                SELECT
                    token_type_id
                INTO var_token_type_id
                FROM
                    token_type
                WHERE
                    type = :type;
            
                SELECT
                    material_id
                INTO var_material_id
                FROM
                    material
                WHERE
                    name = :material_name;
            
                SELECT
                    currency_id
                INTO var_currency_id
                FROM
                    currency
                WHERE
                        name = :currency_name
                    AND country = :country;
            
                UPDATE token_details
                SET
                    value = :value,
                    currency_id = var_currency_id,
                    year = :year,
                    type_id = var_token_type_id,
                    material_id = var_material_id,
                    image_obverse = :image_obverse,
                    image_reverse = :image_reverse,
                    description = :description,
                    subject = :subject
                WHERE
                    token_details_id = var_token_details_id;
            
                SELECT
                    edge_id
                INTO var_edge_id
                FROM
                    edge
                WHERE
                    name = :edge_name;
            
                UPDATE coin_details
                SET
                    diameter = :diameter,
                    weight = :weight,
                    edge_id = var_edge_id
                WHERE
                    coin_details_id = var_coin_details_id;
            
                COMMIT;
            END;
            ''', (coin_id, token_type, material, currency_name, currency_country, value, year, image_obverse,
                  image_reverse, description, subject, edge, diameter, weight)
        )
        print(self.get_coin(coin_id))

    def delete_coin(self, coin_id):
        self.cursor.execute('''
            DECLARE
                var_coin_id          NUMBER := :coin_id;
                var_token_details_id NUMBER;
                var_coin_details_id  NUMBER;
            BEGIN
                SELECT
                    token_details_id,
                    coin_details_id
                INTO
                    var_token_details_id,
                    var_coin_details_id
                FROM
                    coin
                WHERE
                    coin_id = var_coin_id;
            
                DELETE FROM collection_coin
                WHERE
                    coin_id = var_coin_id;
            
                DELETE FROM coin
                WHERE
                    coin_id = var_coin_id;
            
                DELETE FROM token_details
                WHERE
                    token_details_id = var_token_details_id;
            
                DELETE FROM coin_details
                WHERE
                    coin_details_id = var_coin_details_id;
            
                COMMIT;
            END;
            ''', (coin_id,)
        )

    def create_collection(self, username, collection_name, description, image):
        self.cursor.execute('''
            insert into collection (name, consumer_id, description, image) 
            values (
                :collection_name, (select c.consumer_id from consumer c where c.name = :username), :description, :image
            )
            ''', (collection_name, username, description, image)
        )
        self.connection.commit()

    def get_collection(self, collection_id):
        return self.cursor.execute("""
            select name, description, image
            from collection
            where collection_id = :collection_id
        """, (collection_id, )).fetchone()

    def update_collection(self, collection_id, name, description, image):
        self.cursor.execute('''
            update collection
            set name = :name, description = :description, image = :image 
            where collection_id = :collection_id
            ''', (name, description, image, collection_id)
        )
        self.connection.commit()

    def delete_collection(self, collection_id):
        self.cursor.execute('''
            DECLARE
                CURSOR coins IS
                SELECT
                    c.coin_id,
                    c.token_details_id,
                    c.coin_details_id
                FROM
                         coin c
                    INNER JOIN collection_coin cc ON cc.coin_id = c.coin_id
                    INNER JOIN collection      coll ON coll.collection_id = cc.collection_id
                WHERE
                    coll.collection_id = :collection_id;
            
            BEGIN
                FOR record IN coins LOOP
                    DELETE FROM collection_coin
                    WHERE
                        coin_id = record.coin_id;
            
                    DELETE FROM coin
                    WHERE
                        coin_id = record.coin_id;
            
                    DELETE FROM token_details
                    WHERE
                        token_details_id = record.token_details_id;
            
                    DELETE FROM coin_details
                    WHERE
                        coin_details_id = record.coin_details_id;
            
                END LOOP;
            
                DELETE FROM collection
                WHERE
                    collection_id = :collection_id;
            
                COMMIT;
            END;
            ''', (collection_id, )
        )


connection = Connection()
