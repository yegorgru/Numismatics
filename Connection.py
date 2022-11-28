import cx_Oracle
from enum import Enum
from verify_email import verify_email

from Utils import *


class UserCode(Enum):
    SUCCESS = 0
    NAME_TAKEN = 1
    NAME_LENGTH = 2
    EMAIL_INCORRECT = 3
    EMAIL_LENGTH = 4
    EMAIL_TAKEN = 5
    PASSWORD_LENGTH = 6


class MakeOfferCode(Enum):
    SUCCESS = 0
    SAME_CONSUMER = 1
    SMALL_PRICE = 2


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

    def create_user(self, username, email, password):
        if len(username) < 4 or len(username) > 20:
            return UserCode.NAME_LENGTH
        if len(password) < 4 or len(password) > 20:
            return UserCode.PASSWORD_LENGTH
        if len(email) > 30:
            return UserCode.EMAIL_LENGTH
        rs = self.cursor.execute('SELECT COUNT(*) from consumer where name = :username', (username, )).fetchone()
        if rs[0] == 1:
            return UserCode.NAME_TAKEN
        if not verify_email(email):
            return UserCode.EMAIL_INCORRECT
        rs = self.cursor.execute('SELECT COUNT(*) from consumer where email = :email', (email, )).fetchone()
        if rs[0] == 1:
            return UserCode.EMAIL_TAKEN
        img = get_general_image_bytes()
        self.cursor.execute('''
            DECLARE
                var_consumer_id NUMBER;
            BEGIN
                INSERT INTO consumer (
                    name,
                    password,
                    is_admin,
                    email
                ) VALUES (
                    :name,
                    :password,
                    0,
                    :email
                ) RETURNING consumer_id INTO var_consumer_id;
            
                INSERT INTO collection (
                    name,
                    consumer_id,
                    image
                ) VALUES (
                    :general_name,
                    var_consumer_id,
                    :image
                );
                
                INSERT INTO consumer_statistics (consumer_id) VALUES (var_consumer_id);
                
                COMMIT;
            
            END;
        ''', (username, password, email, GENERAL_COLLECTION_NAME, img)
        )
        return UserCode.SUCCESS

    def update_consumer(self, name, email, password, img, consumer_id):
        if len(name) < 4 or len(name) > 20:
            return UserCode.NAME_LENGTH
        if len(password) < 4 or len(password) > 20:
            return UserCode.PASSWORD_LENGTH
        if len(email) > 30:
            return UserCode.EMAIL_LENGTH
        if not verify_email(email):
            return UserCode.EMAIL_INCORRECT
        self.cursor.execute('''update consumer
                                set name = :name, email = :email, password = :password, image = :image 
                                where consumer_id = :consumer_id
                            ''', (name, email, password, img, consumer_id))
        self.connection.commit()
        return UserCode.SUCCESS

    def get_consumer(self, name):
        return self.cursor.execute('''select name, email, password, image, consumer_id from consumer 
                                    where name = :name''', (name, )).fetchone()

    def get_collections_preview(self, username):
        return self.cursor.execute("""
            SELECT coll.name, coll.image, coll.collection_id
            from collection coll
            inner join consumer c
            on c.consumer_id = coll.consumer_id
            where c.name = :username
            order by
                (CASE coll.name
                    WHEN :general_name THEN 2
                    ELSE 1
                END) DESC,
            coll.name DESC
        """, (username, GENERAL_COLLECTION_NAME))

    def get_collection_names(self, collection_id):
        names = self.cursor.execute("""
            SELECT name
            from collection
            where consumer_id = (select consumer_id from collection where collection_id = :collection_id)
        """, (collection_id, )).fetchall()
        name = self.get_collection_name(collection_id)
        return names, name

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

    def get_banknotes_preview(self, collection_id):
        return self.cursor.execute("""
            SELECT b.banknote_id, td.value, currency.name, td.year, td.image_obverse
            from banknote b
            inner join collection_banknote cb
                on cb.banknote_id = b.banknote_id
            inner join collection c
                on c.collection_id = cb.collection_id
            inner join token_details td
                on b.token_details_id = td.token_details_id
            inner join currency
                on currency.currency_id = td.currency_id
            where c.collection_id = :collection_id
        """, (collection_id,))

    def get_user_deals_coin_preview(self, username, active):
        if active:
            return self.cursor.execute("""
                SELECT coin.coin_id, td.value, currency.name, td.year, td.image_obverse, cd.price, cd.date_begin
                from  consumer c
                inner join coin_deal cd on cd.seller_id = c.consumer_id
                inner join coin on coin.coin_id = cd.coin_id
                inner join token_details td on td.token_details_id = coin.token_details_id
                inner join currency on currency.currency_id = td.currency_id
                where c.name = :username
                order by cd.date_begin desc
            """, (username,))
        else:
            return self.cursor.execute("""
                (SELECT cda.coin_deal_archive_id, td.value, currency.name, td.year, td.image_obverse, cda.price,
                        cda.date_end, c.name name1, ccc.name name2
                from  consumer c
                inner join coin_deal_archive cda on cda.seller_id = c.consumer_id
                left join coin on coin.coin_id = cda.coin_id
                left join token_details td on td.token_details_id = coin.token_details_id
                left join currency on currency.currency_id = td.currency_id
                inner join consumer ccc on ccc.consumer_id = cda.buyer_id
                where c.name = :username)
                UNION ALL
                (SELECT cda.coin_deal_archive_id, td.value, currency.name, td.year, td.image_obverse, cda.price,
                        cda.date_end, ccc.name name1, c.name name2
                from  consumer c
                inner join coin_deal_archive cda on cda.buyer_id = c.consumer_id
                left join coin on coin.coin_id = cda.coin_id
                left join token_details td on td.token_details_id = coin.token_details_id
                left join currency on currency.currency_id = td.currency_id
                inner join consumer ccc on ccc.consumer_id = cda.seller_id
                where c.name = :username)
                order by date_end desc
            """, (username, username))

    def get_user_deals_banknote_preview(self, username, active):
        if active:
            return self.cursor.execute("""
                SELECT banknote.banknote_id, td.value, currency.name, td.year, td.image_obverse, bd.price, bd.date_begin
                from  consumer c
                inner join banknote_deal bd on bd.seller_id = c.consumer_id
                inner join banknote on banknote.banknote_id = bd.banknote_id
                inner join token_details td on td.token_details_id = banknote.token_details_id
                inner join currency on currency.currency_id = td.currency_id
                where c.name = :username
                order by bd.date_begin desc
            """, (username,))
        else:
            return self.cursor.execute("""
                (SELECT bda.banknote_deal_archive_id, td.value, currency.name, td.year, td.image_obverse, bda.price,
                        bda.date_end, c.name name1, ccc.name name2
                from  consumer c
                inner join banknote_deal_archive bda on bda.seller_id = c.consumer_id
                left join banknote on banknote.banknote_id = bda.banknote_id
                left join token_details td on td.token_details_id = banknote.token_details_id
                left join currency on currency.currency_id = td.currency_id
                inner join consumer ccc on ccc.consumer_id = bda.buyer_id
                where c.name = :username)
                UNION ALL
                (SELECT bda.banknote_deal_archive_id, td.value, currency.name, td.year, td.image_obverse, bda.price,
                        bda.date_end, ccc.name name1, c.name name2
                from  consumer c
                inner join banknote_deal_archive bda on bda.buyer_id = c.consumer_id
                left join banknote on banknote.banknote_id = bda.banknote_id
                left join token_details td on td.token_details_id = banknote.token_details_id
                left join currency on currency.currency_id = td.currency_id
                inner join consumer ccc on ccc.consumer_id = bda.seller_id
                where c.name = :username)
                order by date_end desc
            """, (username,))

    def get_token_types(self):
        return self.cursor.execute("select type from token_type").fetchall()

    def get_edge_types(self):
        return self.cursor.execute("select name from edge").fetchall()

    def get_material_names(self):
        return self.cursor.execute("select name from material").fetchall()

    def get_currencies(self):
        return self.cursor.execute("select name, country from currency").fetchall()

    def create_coin(self, value, currency_name, currency_country, year, token_type, material, image_obverse,
                    image_reverse, description, subject, diameter, weight, edge, collection_name, collection_id):
        self.cursor.execute('''
            DECLARE
                var_token_type_id           NUMBER;
                var_material_id             NUMBER;
                var_currency_id             NUMBER;
                var_token_details_id        NUMBER;
                var_edge_id                 NUMBER;
                var_coin_details_id         NUMBER;
                var_coin_id                 NUMBER;
                var_previous_collection_id  NUMBER := :var_previous_collection_id;
                var_collection_id           NUMBER;
                var_tokens                  NUMBER;
                var_consumer_id             NUMBER;
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
                
                INSERT INTO coin_statistics (
                    coin_id
                ) VALUES (
                    var_coin_id
                );
                
                SELECT
                    coll.collection_id, coll.consumer_id
                INTO var_collection_id, var_consumer_id
                FROM
                    collection coll
                    inner join collection coll2 on coll2.consumer_id = coll.consumer_id
                WHERE
                    coll.name = :collection_name
                    and coll2.collection_id = var_previous_collection_id;
            
                INSERT INTO collection_coin (
                    coin_id,
                    collection_id
                ) VALUES (
                    var_coin_id,
                    var_collection_id
                );
                
                SELECT tokens INTO var_tokens FROM consumer_statistics
                where consumer_id = var_consumer_id;
                
                var_tokens := var_tokens + 1;
                
                UPDATE consumer_statistics
                SET tokens = var_tokens
                WHERE consumer_id = var_consumer_id;
                
                COMMIT;
            END;
            ''', (collection_id, token_type, material, currency_name, currency_country, value, year, image_obverse,
                  image_reverse, description, subject, edge, diameter, weight, collection_name)
        )

    def create_banknote(self, value, currency_name, currency_country, year, token_type, material, image_obverse,
                        image_reverse, description, subject, width, height, collection_name, collection_id):
        self.cursor.execute('''
            DECLARE
                var_token_type_id    NUMBER;
                var_material_id      NUMBER;
                var_currency_id      NUMBER;
                var_token_details_id NUMBER;
                var_banknote_details_id  NUMBER;
                var_banknote_id          NUMBER;
                var_previous_collection_id  NUMBER := :var_previous_collection_id;
                var_collection_id    NUMBER;
                var_tokens                  NUMBER;
                var_consumer_id             NUMBER;
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

                INSERT INTO banknote_details (
                    width,
                    height
                ) VALUES (
                    :diameter,
                    :weight
                ) RETURNING banknote_details_id INTO var_banknote_details_id;

                INSERT INTO banknote (
                    token_details_id,
                    banknote_details_id
                ) VALUES (
                    var_token_details_id,
                    var_banknote_details_id
                ) RETURNING banknote_id INTO var_banknote_id;
                
                INSERT INTO banknote_statistics (
                    banknote_id
                ) VALUES (
                    var_banknote_id
                );

                SELECT
                    coll.collection_id, coll.consumer_id
                INTO var_collection_id, var_consumer_id
                FROM
                    collection coll
                    inner join collection coll2 on coll2.consumer_id = coll.consumer_id
                WHERE
                    coll.name = :collection_name
                    and coll2.collection_id = var_previous_collection_id;

                INSERT INTO collection_banknote (
                    banknote_id,
                    collection_id
                ) VALUES (
                    var_banknote_id,
                    var_collection_id
                );
                
                SELECT tokens INTO var_tokens FROM consumer_statistics
                where consumer_id = var_consumer_id;
                
                var_tokens := var_tokens + 1;
                
                UPDATE consumer_statistics
                SET tokens = var_tokens
                WHERE consumer_id = var_consumer_id;

                COMMIT;
            END;
            ''', (collection_id, token_type, material, currency_name, currency_country, value, year, image_obverse,
                  image_reverse, description, subject, width, height, collection_name)
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
                edge.name,
                coin_deal.coin_deal_id
            FROM
                     coin
                INNER JOIN token_details td ON td.token_details_id = coin.token_details_id
                INNER JOIN coin_details  cd ON cd.coin_details_id = coin.coin_details_id
                INNER JOIN currency ON td.currency_id = currency.currency_id
                INNER JOIN token_type ON td.type_id = token_type.token_type_id
                INNER JOIN material ON td.material_id = material.material_id
                INNER JOIN edge ON cd.edge_id = edge.edge_id
                LEFT JOIN coin_deal ON coin_deal.coin_id = coin.coin_id
            WHERE
                coin.coin_id = :coin_id
        """, (coin_id, )).fetchone()

    def get_banknote(self, banknote_id):
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
                bd.width,
                bd.height,
                banknote_deal.banknote_deal_id
            FROM
                     banknote
                INNER JOIN token_details td ON td.token_details_id = banknote.token_details_id
                INNER JOIN banknote_details  bd ON bd.banknote_details_id = banknote.banknote_details_id
                INNER JOIN currency ON td.currency_id = currency.currency_id
                INNER JOIN token_type ON td.type_id = token_type.token_type_id
                INNER JOIN material ON td.material_id = material.material_id
                LEFT JOIN banknote_deal ON banknote_deal.banknote_id = banknote.banknote_id
            WHERE
                banknote.banknote_id = :banknote_id
        """, (banknote_id, )).fetchone()

    def update_coin(self, coin_id, value, currency_name, currency_country, year, token_type, material, image_obverse,
                    image_reverse, description, subject, diameter, weight, edge, collection_name, collection_id):
        self.cursor.execute('''
            DECLARE
                var_previous_collection_id  NUMBER := :var_previous_collection_id;
                var_coin_id          NUMBER := :coin_id;
                var_token_type_id    NUMBER;
                var_material_id      NUMBER;
                var_currency_id      NUMBER;
                var_token_details_id NUMBER;
                var_edge_id          NUMBER;
                var_coin_details_id  NUMBER;
                var_collection_id    NUMBER;
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
                    
                SELECT
                    coll.collection_id
                INTO var_collection_id
                FROM
                    collection coll
                    inner join collection coll2 on coll2.consumer_id = coll.consumer_id
                WHERE
                    coll.name = :collection_name
                    and coll2.collection_id = var_previous_collection_id;
                    
                UPDATE collection_coin 
                SET
                    collection_id = var_collection_id
                WHERE
                    coin_id = var_coin_id;
            
                COMMIT;
            END;
            ''', (collection_id, coin_id, token_type, material, currency_name, currency_country, value, year,
                  image_obverse, image_reverse, description, subject, edge, diameter, weight, collection_name)
        )

    def update_banknote(self, banknote_id, value, currency_name, currency_country, year, token_type, material,
                        image_obverse, image_reverse, description, subject, width, height, collection_name,
                        collection_id):
        self.cursor.execute('''
            DECLARE
                var_previous_collection_id  NUMBER := :var_previous_collection_id;
                var_banknote_id         NUMBER := :banknote_id;
                var_token_type_id       NUMBER;
                var_material_id         NUMBER;
                var_currency_id         NUMBER;
                var_token_details_id    NUMBER;
                var_banknote_details_id NUMBER;
                var_collection_id       NUMBER;
            BEGIN
                SELECT
                    token_details_id,
                    banknote_details_id
                INTO
                    var_token_details_id,
                    var_banknote_details_id
                FROM
                    banknote
                WHERE
                    banknote_id = var_banknote_id;

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

                UPDATE banknote_details
                SET
                    width = :width,
                    height = :height
                WHERE
                    banknote_details_id = var_banknote_details_id;

                SELECT
                    coll.collection_id
                INTO var_collection_id
                FROM
                    collection coll
                    inner join collection coll2 on coll2.consumer_id = coll.consumer_id
                WHERE
                    coll.name = :collection_name
                    and coll2.collection_id = var_previous_collection_id;

                UPDATE collection_banknote 
                SET
                    collection_id = var_collection_id
                WHERE
                    banknote_id = var_banknote_id;

                COMMIT;
            END;
            ''', (collection_id, banknote_id, token_type, material, currency_name, currency_country, value, year, image_obverse,
                  image_reverse, description, subject, width, height, collection_name)
        )

    def delete_coin(self, coin_id):
        self.cursor.execute('''
            DECLARE
                var_coin_id          NUMBER := :coin_id;
                var_token_details_id NUMBER;
                var_coin_details_id  NUMBER;
                var_tokens           NUMBER;
                var_consumer_id      NUMBER;
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
                    
                SELECT cs.tokens, cs.consumer_id INTO var_tokens, var_consumer_id FROM consumer_statistics cs
                inner join consumer c on c.consumer_id = cs.consumer_id
                inner join collection coll on coll.consumer_id = c.consumer_id
                inner join collection_coin cc on cc.collection_id = coll.collection_id
                where cc.coin_id = var_coin_id;
                
                var_tokens := var_tokens - 1;
                
                UPDATE consumer_statistics
                SET tokens = var_tokens
                WHERE consumer_id = var_consumer_id;
            
                DELETE FROM collection_coin
                WHERE
                    coin_id = var_coin_id;
            
                UPDATE coin_deal_archive
                SET coin_id = NULL
                where coin_id = var_coin_id;
                
                DELETE FROM coin_statistics
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

    def delete_banknote(self, banknote_id):
        self.cursor.execute('''
            DECLARE
                var_banknote_id          NUMBER := :banknote_id;
                var_token_details_id     NUMBER;
                var_banknote_details_id  NUMBER;
                var_tokens               NUMBER;
                var_consumer_id          NUMBER;
            BEGIN
                SELECT
                    token_details_id,
                    banknote_details_id
                INTO
                    var_token_details_id,
                    var_banknote_details_id
                FROM
                    banknote
                WHERE
                    banknote_id = var_banknote_id;
                    
                SELECT cs.tokens, cs.consumer_id INTO var_tokens, var_consumer_id FROM consumer_statistics cs
                inner join consumer c on c.consumer_id = cs.consumer_id
                inner join collection coll on coll.consumer_id = c.consumer_id
                inner join collection_banknote cb on cb.collection_id = coll.collection_id
                where cb.banknote_id = var_banknote_id;
                
                var_tokens := var_tokens - 1;
                
                UPDATE consumer_statistics
                SET tokens = var_tokens
                WHERE consumer_id = var_consumer_id;

                DELETE FROM collection_banknote
                WHERE
                    banknote_id = var_banknote_id;
                    
                UPDATE banknote_deal_archive
                SET banknote_id = NULL
                where banknote_id = var_banknote_id;
                
                DELETE FROM banknote_statistics
                WHERE
                    banknote_id = var_banknote_id;

                DELETE FROM banknote
                WHERE
                    banknote_id = var_banknote_id;

                DELETE FROM token_details
                WHERE
                    token_details_id = var_token_details_id;

                DELETE FROM banknote_details
                WHERE
                    banknote_details_id = var_banknote_details_id;

                COMMIT;
            END;
            ''', (banknote_id,)
        )

    def create_collection(self, username, collection_name, description, image):
        self.cursor.execute('''
            DECLARE
                var_collections             NUMBER;
                var_consumer_id             NUMBER;
            BEGIN
                select c.consumer_id into var_consumer_id from consumer c where c.name = :username;
                
                select collections into var_collections
                from consumer_statistics
                where consumer_id = var_consumer_id;
                
                var_collections := var_collections + 1;
                
                UPDATE consumer_statistics
                SET collections = var_collections
                WHERE consumer_id = var_consumer_id;
                
                insert into collection (name, consumer_id, description, image) 
                values (
                    :collection_name, var_consumer_id, :description, :image
                );
            END;
            ''', (username, collection_name, description, image)
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

    def get_collection_name(self, collection_id):
        return  self.cursor.execute(
            "select name from collection where collection_id = :collection_id", (collection_id, )
        ).fetchone()[0]

    def delete_collection(self, collection_id):
        name = self.get_collection_name(collection_id)
        if name == GENERAL_COLLECTION_NAME:
            return False
        self.cursor.execute('''
            DECLARE
                var_tokens NUMBER;
                var_consumer_id NUMBER;
                var_collection_id NUMBER := :collection_id;
                var_collections NUMBER;
            
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
                    coll.collection_id = var_collection_id;
                    
                CURSOR banknotes IS
                SELECT
                    b.banknote_id,
                    b.token_details_id,
                    b.banknote_details_id
                FROM
                         banknote b
                    INNER JOIN collection_banknote cb ON cb.banknote_id = b.banknote_id
                    INNER JOIN collection      coll ON coll.collection_id = cb.collection_id
                WHERE
                    coll.collection_id = var_collection_id;    
            
            BEGIN
                SELECT consumer_id into var_consumer_id from collection where collection_id = var_collection_id;
            
                FOR record IN coins LOOP
                
                    SELECT cs.tokens INTO var_tokens FROM consumer_statistics cs
                    inner join consumer c on c.consumer_id = cs.consumer_id
                    inner join collection coll on coll.consumer_id = c.consumer_id
                    inner join collection_coin cc on cc.collection_id = coll.collection_id
                    where cc.coin_id = record.coin_id;
                    
                    var_tokens := var_tokens - 1;
                    
                    UPDATE consumer_statistics
                    SET tokens = var_tokens
                    WHERE consumer_id = var_consumer_id;
                
                    UPDATE coin_deal_archive
                    SET coin_id = NULL
                    where coin_id = record.coin_id;
                    
                    DELETE FROM collection_coin
                    WHERE
                        coin_id = record.coin_id;
            
                    DELETE FROM coin_statistics
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
                
                FOR record IN banknotes LOOP
                
                    SELECT cs.tokens INTO var_tokens FROM consumer_statistics cs
                    inner join consumer c on c.consumer_id = cs.consumer_id
                    inner join collection coll on coll.consumer_id = c.consumer_id
                    inner join collection_banknote cb on cb.collection_id = coll.collection_id
                    where cb.banknote_id = record.banknote_id;
                    
                    var_tokens := var_tokens - 1;
                    
                    UPDATE consumer_statistics
                    SET tokens = var_tokens
                    WHERE consumer_id = var_consumer_id;
                
                    UPDATE banknote_deal_archive
                    SET banknote_id = NULL
                    where banknote_id = record.banknote_id;
                    
                    DELETE FROM collection_banknote
                    WHERE
                        banknote_id = record.banknote_id;
                        
                    DELETE FROM banknote_statistics
                    WHERE
                        banknote_id = record.banknote_id;
            
                    DELETE FROM banknote
                    WHERE
                        banknote_id = record.banknote_id;
            
                    DELETE FROM token_details
                    WHERE
                        token_details_id = record.token_details_id;
            
                    DELETE FROM banknote_details
                    WHERE
                        banknote_details_id = record.banknote_details_id;
            
                END LOOP;
                
                select collections into var_collections
                from consumer_statistics
                where consumer_id = var_consumer_id;
                
                var_collections := var_collections - 1;
                
                UPDATE consumer_statistics
                SET collections = var_collections
                WHERE consumer_id = var_consumer_id;
            
                DELETE FROM collection
                WHERE
                    collection_id = :collection_id;
            
                COMMIT;
            END;
            ''', (collection_id, )
        )
        return True

    def create_coin_deal(self, coin_id, price, deal_type):
        self.cursor.execute('''
            DECLARE
                var_seller_id       NUMBER;
                var_coin_id         NUMBER := :coin_id;
                var_deal_type_id    NUMBER;
            BEGIN
                SELECT
                    c.consumer_id
                INTO var_seller_id
                FROM
                         consumer c
                    INNER JOIN collection      coll ON c.consumer_id = coll.consumer_id
                    INNER JOIN collection_coin cc ON cc.collection_id = coll.collection_id
                WHERE
                    cc.coin_id = var_coin_id;
                    
                SELECT 
                    deal_type_id
                INTO var_deal_type_id
                FROM 
                    deal_type
                WHERE 
                    type = :deal_type;
            
                INSERT INTO coin_deal (
                    coin_id,
                    seller_id,
                    price,
                    deal_type_id
                ) VALUES (
                    var_coin_id,
                    var_seller_id,
                    :price,
                    var_deal_type_id
                );
            
                COMMIT;
            END;
            ''', (coin_id, deal_type, price)
        )

    def create_banknote_deal(self, banknote_id, price, deal_type):
        self.cursor.execute('''
            DECLARE
                var_seller_id       NUMBER;
                var_banknote_id     NUMBER := :banknote_id;
                var_deal_type_id    NUMBER;
            BEGIN
                SELECT
                    c.consumer_id
                INTO var_seller_id
                FROM
                         consumer c
                    INNER JOIN collection      coll ON c.consumer_id = coll.consumer_id
                    INNER JOIN collection_banknote cb ON cb.collection_id = coll.collection_id
                WHERE
                    cb.banknote_id = var_banknote_id;

                SELECT 
                    deal_type_id
                INTO var_deal_type_id
                FROM 
                    deal_type
                WHERE 
                    type = :deal_type;

                INSERT INTO banknote_deal (
                    banknote_id,
                    seller_id,
                    price,
                    deal_type_id
                ) VALUES (
                    var_banknote_id,
                    var_seller_id,
                    :price,
                    var_deal_type_id
                );

                COMMIT;
            END;
            ''', (banknote_id, deal_type, price)
        )

    def cancel_coin_deal(self, coin_id):
        self.cursor.execute('''
            DECLARE 
                var_coin_id NUMBER := :coin_id;
            BEGIN
                DELETE(
                    SELECT * FROM COIN_LOT cl
                    inner join COIN_DEAL cd ON cd.COIN_DEAL_ID = cl.COIN_DEAL_ID
                    where cd.coin_id = var_coin_id
                );
                DELETE FROM COIN_DEAL cd
                WHERE cd.coin_id = var_coin_id;
                COMMIT;
            END;
            ''', (coin_id, )
        )

    def cancel_banknote_deal(self, banknote_id):
        self.cursor.execute('''
            DECLARE 
                var_banknote_id NUMBER := :banknote_id;
            BEGIN
                DELETE(
                    SELECT * FROM banknote_lot bl
                    inner join banknote_deal bd ON bd.banknote_deal_id = bl.banknote_deal_id
                    where bd.banknote_id = var_banknote_id
                );
                DELETE FROM banknote_deal bd
                WHERE bd.banknote_id = var_banknote_id;
                COMMIT;
            END;
            ''', (banknote_id, )
        )

    def get_deal_coin_details(self, coin_id):
        deal_type = self.cursor.execute("""
            select type from deal_type dt
            inner join coin_deal cd on cd.deal_type_id = dt.deal_type_id
            where cd.coin_id = :coin_id
        """, (coin_id,)).fetchone()[0]
        if deal_type == 'Sale':
            return self.cursor.execute("""
                select c.image, c.name, cd.price
                FROM coin_lot cl
                inner join consumer c
                on c.consumer_id = cl.buyer_id
                inner join coin_deal cd on cd.coin_deal_id = cl.coin_deal_id
                where cd.coin_id = :coin_id
            """, (coin_id,)).fetchone()
        else:
            return self.cursor.execute("""
                SELECT
                    *
                FROM
                    (
                        SELECT
                            c.image,
                            c.name,
                            cl.price
                        FROM
                                 coin_deal cd
                            INNER JOIN coin_lot cl ON cl.coin_deal_id = cd.coin_deal_id
                            INNER JOIN consumer c ON c.consumer_id = cl.buyer_id
                        WHERE
                            cd.coin_id = :coin_id
                        ORDER BY
                            cl.price DESC
                    )
                WHERE
                    ROWNUM = 1
            """, (coin_id,)).fetchone()

    def get_deal_banknote_details(self, banknote_id):
        deal_type = self.cursor.execute("""
            select type from deal_type dt
            inner join banknote_deal bd on bd.deal_type_id = dt.deal_type_id
            where bd.banknote_id = :banknote_id
        """, (banknote_id,)).fetchone()[0]
        if deal_type == 'Sale':
            return self.cursor.execute("""
                select c.image, c.name, bd.price
                FROM banknote_lot bl
                inner join consumer c
                on c.consumer_id = bl.buyer_id
                inner join banknote_deal bd on bd.banknote_deal_id = bl.banknote_deal_id
                where bd.banknote_id = :banknote_id
            """, (banknote_id,)).fetchone()
        else:
            return self.cursor.execute("""
                SELECT
                    *
                FROM
                    (
                        SELECT
                            c.image,
                            c.name,
                            bl.price
                        FROM
                                 banknote_deal bd
                            INNER JOIN banknote_lot bl ON bl.banknote_deal_id = bd.banknote_deal_id
                            INNER JOIN consumer c ON c.consumer_id = bl.buyer_id
                        WHERE
                            bd.banknote_id = :banknote_id
                        ORDER BY
                            bl.price DESC
                    )
                WHERE
                    ROWNUM = 1
            """, (banknote_id,)).fetchone()

    def refresh_deal_coin_value(self, coin_id):
        deal_type = self.cursor.execute("""
                        select type from deal_type dt
                        inner join coin_deal cd on cd.deal_type_id = dt.deal_type_id
                        where cd.coin_id = :coin_id
                    """, (coin_id,)
                                        ).fetchone()[0]
        if deal_type == 'Auction':
            max_lot = self.cursor.execute("""
                SELECT
                    *
                FROM
                    (
                        SELECT
                            cl.price
                        FROM
                                 coin_deal cd
                            INNER JOIN coin_lot cl ON cl.coin_deal_id = cd.coin_deal_id
                        WHERE
                            cd.coin_id = :coin_id
                        ORDER BY
                            cl.price DESC
                    )
                WHERE
                    ROWNUM = 1

                    """, (coin_id,)).fetchone()
            if max_lot is not None:
                return max_lot[0] + 1
        return self.cursor.execute("""   
                    select price from coin_deal where coin_id = :coin_id
                """, (coin_id,)).fetchone()[0]

    def refresh_deal_banknote_value(self, banknote_id):
        deal_type = self.cursor.execute("""
                        select type from deal_type dt
                        inner join banknote_deal bd on bd.deal_type_id = dt.deal_type_id
                        where bd.banknote_id = :banknote_id
                    """, (banknote_id,)
                                        ).fetchone()[0]
        if deal_type == 'Auction':
            max_lot = self.cursor.execute("""
                SELECT
                    *
                FROM
                    (
                        SELECT
                            bl.price
                        FROM
                                 banknote_deal bd
                            INNER JOIN banknote_lot bl ON bl.banknote_deal_id = bd.banknote_deal_id
                        WHERE
                            bd.banknote_id = :banknote_id
                        ORDER BY
                            bl.price DESC
                    )
                WHERE
                    ROWNUM = 1

                    """, (banknote_id,)).fetchone()
            if max_lot is not None:
                return max_lot[0] + 1
        return self.cursor.execute("""   
                    select price from banknote_deal where banknote_id = :banknote_id
                """, (banknote_id,)).fetchone()[0]

    def approve_coin_deal(self, coin_id):
        self.cursor.execute("""
            DECLARE
                var_coin_id         NUMBER := :coin_id;
                var_price           NUMBER;
                var_buyer_id        NUMBER;
                var_seller_id       NUMBER;
                var_deal_type_id    NUMBER;
                var_coin_deal_id    NUMBER;
                var_collection_id   NUMBER;
                var_income          NUMBER;
                var_spending        NUMBER;
                var_deals           NUMBER;
                var_tokens          NUMBER;
                var_total_spending  NUMBER;
                var_owners          NUMBER;
            BEGIN
                SELECT
                    *
                INTO var_buyer_id, var_price, var_seller_id, var_deal_type_id
                FROM
                (
                    SELECT
                        c.consumer_id,
                        cl.price,
                        cd.seller_id,
                        cd.deal_type_id
                    FROM
                             coin
                        INNER JOIN coin_deal cd ON cd.coin_id = coin.coin_id
                        INNER JOIN coin_lot  cl ON cl.coin_deal_id = cd.coin_deal_id
                        INNER JOIN consumer  c ON c.consumer_id = cl.buyer_id
                    WHERE
                        coin.coin_id = var_coin_id
                    ORDER BY
                        cl.price DESC
                )
                WHERE
                    ROWNUM = 1;
                
                INSERT INTO coin_deal_archive(coin_id, seller_id, buyer_id, price, deal_type_id)
                VALUES (var_coin_id, var_seller_id, var_buyer_id, var_price, var_deal_type_id);
                
                SELECT coin_deal_id INTO var_coin_deal_id FROM coin_deal where coin_id = var_coin_id;
                DELETE FROM coin_lot WHERE coin_deal_id = var_coin_deal_id;
                DELETE FROM coin_deal WHERE coin_deal_id = var_coin_deal_id;
                
                SELECT coll.collection_id INTO var_collection_id FROM collection coll
                INNER JOIN consumer c on c.consumer_id = coll.consumer_id
                WHERE c.consumer_id = var_buyer_id
                AND coll.name = :general;
                
                UPDATE collection_coin
                SET collection_id = var_collection_id
                WHERE coin_id = var_coin_id;
                
                SELECT income, deals, tokens INTO var_income, var_deals, var_tokens
                FROM consumer_statistics
                WHERE consumer_id = var_seller_id;
                
                var_income := var_income + var_price;
                var_deals := var_deals + 1;
                var_tokens := var_tokens - 1;
                
                UPDATE consumer_statistics SET
                income = var_income,
                deals = var_deals,
                tokens = var_tokens
                WHERE consumer_id = var_seller_id;
                
                SELECT spending, deals, tokens INTO var_spending, var_deals, var_tokens
                FROM consumer_statistics
                WHERE consumer_id = var_buyer_id;
                
                var_spending := var_spending + var_price;
                var_deals := var_deals + 1;
                var_tokens := var_tokens + 1;
                
                UPDATE consumer_statistics SET
                spending = var_spending,
                deals = var_deals,
                tokens = var_tokens
                WHERE consumer_id = var_buyer_id;
                
                SELECT total_spending, owners INTO var_total_spending, var_owners
                FROM coin_statistics
                WHERE coin_id = var_coin_id;
                
                var_total_spending := var_total_spending + var_price;
                var_owners := var_owners + 1;
                
                UPDATE coin_statistics SET
                total_spending = var_total_spending,
                owners = var_owners
                WHERE coin_id = var_coin_id;
                    
                commit;
            END;
                
        """, (coin_id, GENERAL_COLLECTION_NAME))

    def approve_banknote_deal(self, banknote_id):
        self.cursor.execute("""
            DECLARE
                var_banknote_id         NUMBER := :banknote_id;
                var_price               NUMBER;
                var_buyer_id            NUMBER;
                var_seller_id           NUMBER;
                var_deal_type_id        NUMBER;
                var_banknote_deal_id    NUMBER;
                var_collection_id       NUMBER;
                var_income              NUMBER;
                var_spending            NUMBER;
                var_deals               NUMBER;
                var_tokens              NUMBER;
                var_total_spending      NUMBER;
                var_owners              NUMBER;
            BEGIN
                SELECT
                    *
                INTO var_buyer_id, var_price, var_seller_id, var_deal_type_id
                FROM
                (
                    SELECT
                        c.consumer_id,
                        bl.price,
                        bd.seller_id,
                        bd.deal_type_id
                    FROM
                             banknote
                        INNER JOIN banknote_deal bd ON bd.banknote_id = banknote.banknote_id
                        INNER JOIN banknote_lot  bl ON bl.banknote_deal_id = bd.banknote_deal_id
                        INNER JOIN consumer  c ON c.consumer_id = bl.buyer_id
                    WHERE
                        banknote.banknote_id = var_banknote_id
                    ORDER BY
                        bl.price DESC
                )
                WHERE
                    ROWNUM = 1;

                INSERT INTO banknote_deal_archive(banknote_id, seller_id, buyer_id, price, deal_type_id)
                VALUES (var_banknote_id, var_seller_id, var_buyer_id, var_price, var_deal_type_id);

                SELECT banknote_deal_id INTO var_banknote_deal_id 
                FROM banknote_deal where banknote_id = var_banknote_id;
                
                DELETE FROM banknote_lot WHERE banknote_deal_id = var_banknote_deal_id;
                DELETE FROM banknote_deal WHERE banknote_deal_id = var_banknote_deal_id;

                SELECT coll.collection_id INTO var_collection_id FROM collection coll
                INNER JOIN consumer c on c.consumer_id = coll.consumer_id
                WHERE c.consumer_id = var_buyer_id
                AND coll.name = :general;

                UPDATE collection_banknote
                SET collection_id = var_collection_id
                WHERE banknote_id = var_banknote_id;
                
                                SELECT income, deals, tokens INTO var_income, var_deals, var_tokens
                FROM consumer_statistics
                WHERE consumer_id = var_seller_id;
                
                var_income := var_income + var_price;
                var_deals := var_deals + 1;
                var_tokens := var_tokens - 1;
                
                UPDATE consumer_statistics SET
                income = var_income,
                deals = var_deals,
                tokens = var_tokens
                WHERE consumer_id = var_seller_id;
                
                SELECT spending, deals, tokens INTO var_spending, var_deals, var_tokens
                FROM consumer_statistics
                WHERE consumer_id = var_buyer_id;
                
                var_spending := var_spending + var_price;
                var_deals := var_deals + 1;
                var_tokens := var_tokens + 1;
                
                UPDATE consumer_statistics SET
                spending = var_spending,
                deals = var_deals,
                tokens = var_tokens
                WHERE consumer_id = var_buyer_id;
                
                SELECT total_spending, owners INTO var_total_spending, var_owners
                FROM banknote_statistics
                WHERE banknote_id = var_banknote_id;
                
                var_total_spending := var_total_spending + var_price;
                var_owners := var_owners + 1;
                
                UPDATE banknote_statistics SET
                total_spending = var_total_spending,
                owners = var_owners
                WHERE banknote_id = var_banknote_id;

                commit;
            END;

        """, (banknote_id, GENERAL_COLLECTION_NAME))

    def search_users(self, name):
        return self.cursor.execute("""
            SELECT
                c.consumer_id,
                c.name,
                c.image
            FROM consumer c
            WHERE
                c.name like '%' || :name || '%'
            ORDER BY
                c.name
        """, (name, )).fetchall()

    def search_collections(self, name):
        return self.cursor.execute("""
            SELECT
                coll.collection_id,
                coll.name,
                cons.name,
                coll.image
            FROM
                     collection coll
                INNER JOIN consumer cons ON cons.consumer_id = coll.consumer_id
            WHERE
                coll.name LIKE '%' || :name || '%' 
                    OR coll.description LIKE '%' || :name || '%' 
            ORDER BY
                coll.name
        """, (name, name)).fetchall()

    def search_user_collections(self, user_id):
        return self.cursor.execute("""
            SELECT
                coll.collection_id,
                coll.name,
                cons.name,
                coll.image
            FROM
                     collection coll
                INNER JOIN consumer cons ON cons.consumer_id = coll.consumer_id
            WHERE
                cons.consumer_id = :user_id
            ORDER BY
                coll.name
        """, (user_id, )).fetchall()

    def search_collection_coins(self, collection_id):
        return self.cursor.execute("""
            SELECT coin.coin_id, td.value, currency.name, td.year, td.subject, cons.name, td.image_obverse,
                    coin_deal.coin_deal_id
            from coin
            inner join collection_coin cc
                on cc.coin_id = coin.coin_id
            inner join collection c
                on c.collection_id = cc.collection_id
            inner join token_details td
                on coin.token_details_id = td.token_details_id
            inner join currency
                on currency.currency_id = td.currency_id
            inner join consumer cons
                on cons.consumer_id = c.consumer_id
            left outer join coin_deal
                on coin_deal.coin_id = coin.coin_id
            where c.collection_id = :collection_id
        """, (collection_id,)).fetchall()

    def search_collection_banknotes(self, collection_id):
        return self.cursor.execute("""
            SELECT banknote.banknote_id, td.value, currency.name, td.year, td.subject, cons.name, td.image_obverse,
                    banknote_deal.banknote_deal_id
            from banknote
            inner join collection_banknote cb
                on cb.banknote_id = banknote.banknote_id
            inner join collection c
                on c.collection_id = cb.collection_id
            inner join token_details td
                on banknote.token_details_id = td.token_details_id
            inner join currency
                on currency.currency_id = td.currency_id
            inner join consumer cons
                on cons.consumer_id = c.consumer_id
            left outer join banknote_deal
                on banknote_deal.banknote_id = banknote.banknote_id
            where c.collection_id = :collection_id
        """, (collection_id,)).fetchall()

    def search_coins_by_details(self, value, currency_name, currency_country, year, token_type, material, description,
                                subject, diameter, weight, edge):
        statement = """
            SELECT coin.coin_id, td.value, currency.name, td.year, td.subject, cons.name, td.image_obverse, 
                        coin_deal.coin_deal_id
            from coin
            inner join collection_coin cc
                on cc.coin_id = coin.coin_id
            inner join collection c
                on c.collection_id = cc.collection_id
            inner join token_details td
                on coin.token_details_id = td.token_details_id
            inner join coin_details cd
                on coin.coin_details_id = cd.coin_details_id
            inner join currency
                on currency.currency_id = td.currency_id
            inner join consumer cons
                on cons.consumer_id = c.consumer_id
            inner join token_type
                on token_type.token_type_id = td.type_id
            inner join material
                on material.material_id = td.material_id
            inner join edge
                on edge.edge_id = cd.edge_id
            left outer join coin_deal
                on coin_deal.coin_id = coin.coin_id
            where 1 = 1
        """
        if value is not None:
            statement += " and td.value = " + str(value)
        if currency_name is not None:
            statement += " and currency.name = '" + currency_name + "'"
        if currency_country is not None:
            statement += " and currency.country = '" + currency_country + "'"
        if year is not None:
            statement += " and td.year = " + str(year)
        if token_type is not None:
            statement += " and token_type.type = '" + token_type + "'"
        if material is not None:
            statement += " and material.name = '" + material + "'"
        if description is not None and description != "":
            statement += " and td.description like  '%" + description + "%'"
        if subject is not None and subject != "":
            statement += " and td.subject like  '%" + subject + "%'"
        if diameter is not None:
            statement += " and cd.diameter = " + str(diameter)
        if weight is not None:
            statement += " and cd.weight = " + str(weight)
        if edge is not None:
            statement += " and edge.name = '" + edge + "'"
        return self.cursor.execute(statement).fetchall()

    def search_banknotes_by_details(self, value, currency_name, currency_country, year, token_type, material,
                                    description, subject, width, height):
        statement = """
            SELECT banknote.banknote_id, td.value, currency.name, td.year, td.subject, cons.name, td.image_obverse,
                    banknote_deal.banknote_deal_id
            from banknote
            inner join collection_banknote cb
                on cb.banknote_id = banknote.banknote_id
            inner join collection c
                on c.collection_id = cb.collection_id
            inner join token_details td
                on banknote.token_details_id = td.token_details_id
            inner join banknote_details bd
                on banknote.banknote_details_id = bd.banknote_details_id
            inner join currency
                on currency.currency_id = td.currency_id
            inner join consumer cons
                on cons.consumer_id = c.consumer_id
            inner join token_type
                on token_type.token_type_id = td.type_id
            inner join material
                on material.material_id = td.material_id
            left outer join banknote_deal
                on banknote_deal.banknote_id = banknote.banknote_id
            where 1 = 1
        """
        if value is not None:
            statement += " and td.value = " + str(value)
        if currency_name is not None:
            statement += " and currency.name = '" + currency_name + "'"
        if currency_country is not None:
            statement += " and currency.country = '" + currency_country + "'"
        if year is not None:
            statement += " and td.year = " + str(year)
        if token_type is not None:
            statement += " and token_type.type = '" + token_type + "'"
        if material is not None:
            statement += " and material.name = '" + material + "'"
        if description is not None and description != "":
            statement += " and td.description like  '%" + description + "%'"
        if subject is not None and subject != "":
            statement += " and td.subject like  '%" + subject + "%'"
        if width is not None:
            statement += " and bd.width = " + str(width)
        if height is not None:
            statement += " and bd.height = " + str(height)
        return self.cursor.execute(statement).fetchall()

    def make_coin_offer(self, coin_id, price, buyer_username):
        name = self.cursor.execute("""
            SELECT c.name
            FROM consumer c
            inner join coin_deal cd on cd.seller_id = c.consumer_id
            where cd.coin_id = :coin_id
        """, (coin_id,)).fetchone()[0]
        if name == buyer_username:
            return MakeOfferCode.SAME_CONSUMER
        start_price = self.cursor.execute("""
                    SELECT price FROM coin_deal WHERE coin_id = :coin_id
                """, (coin_id,)).fetchone()[0]
        if start_price > price:
            return MakeOfferCode.SMALL_PRICE
        self.cursor.execute("""
            DECLARE
                var_coin_deal_id NUMBER;
                var_consumer_id  NUMBER;
            BEGIN
                SELECT coin_deal_id INTO var_coin_deal_id
                FROM coin_deal WHERE coin_id = :coin_id;
                
                SELECT consumer_id INTO var_consumer_id
                FROM consumer WHERE name = :name;
                
                INSERT INTO coin_lot (coin_deal_id, price, buyer_id)
                VALUES (var_coin_deal_id, :price, var_consumer_id);
                
                COMMIT;
            END;
        """, (coin_id, buyer_username, price))
        return MakeOfferCode.SUCCESS

    def make_banknote_offer(self, banknote_id, price, buyer_username):
        name = self.cursor.execute("""
            SELECT c.name
            FROM consumer c
            inner join banknote_deal bd on bd.seller_id = c.consumer_id
            where bd.banknote_id = :banknote_id
        """, (banknote_id,)).fetchone()[0]
        if name == buyer_username:
            return MakeOfferCode.SAME_CONSUMER
        start_price = self.cursor.execute("""
                    SELECT price FROM banknote_deal WHERE banknote_id = :banknote_id
                """, (banknote_id,)).fetchone()[0]
        if start_price > price:
            return MakeOfferCode.SMALL_PRICE
        self.cursor.execute("""
            DECLARE
                var_banknote_deal_id NUMBER;
                var_consumer_id      NUMBER;
            BEGIN
                SELECT banknote_deal_id INTO var_banknote_deal_id
                FROM banknote_deal WHERE banknote_id = :banknote_id;

                SELECT consumer_id INTO var_consumer_id
                FROM consumer WHERE name = :name;

                INSERT INTO banknote_lot (banknote_deal_id, price, buyer_id)
                VALUES (var_banknote_deal_id, :price, var_consumer_id);

                COMMIT;
            END;
        """, (banknote_id, buyer_username, price))
        return MakeOfferCode.SUCCESS

    def get_deal_coin_type(self, coin_id):
        return self.cursor.execute('''
            select dt.type
            from deal_type dt
            inner join coin_deal cd on cd.deal_type_id = dt.deal_type_id
            where cd.coin_id = :coin_id
        ''', (coin_id, )).fetchone()[0]

    def get_deal_banknote_type(self, banknote_id):
        return self.cursor.execute('''
            select dt.type
            from deal_type dt
            inner join banknote_deal bd on bd.deal_type_id = dt.deal_type_id
            where bd.banknote_id = :banknote_id
        ''', (banknote_id, )).fetchone()[0]

    def is_admin(self, username):
        return self.cursor.execute('''
            select is_admin
            from consumer
            where name = :username
        ''', (username, )).fetchone()[0]

    def get_user_statistics(self, username):
        return self.cursor.execute('''
            select cs.income, cs.spending, cs.deals, cs.tokens, cs.collections
            from consumer_statistics cs
            inner join consumer c on c.consumer_id = cs.consumer_id
            where c.name = :username
        ''', (username,)).fetchone()

    def get_coin_statistics(self, coin_id):
        return self.cursor.execute('''
            select total_spending, owners
            from coin_statistics
            where coin_id = :coin_id
        ''', (coin_id,)).fetchone()

    def get_banknote_statistics(self, banknote_id):
        return self.cursor.execute('''
            select total_spending, owners
            from banknote_statistics
            where banknote_id = :banknote_id
        ''', (banknote_id,)).fetchone()

    def get_user_statistics_top(self, field, num):
        return self.cursor.execute('''
            select c.image, c.name, cs.income, cs.spending, cs.deals, cs.tokens
            from consumer_statistics cs
            inner join consumer c on c.consumer_id = cs.consumer_id
            order by 
        ''' + field + ' desc').fetchmany(num)

    def get_coin_statistics_top(self, field, num):
        return self.cursor.execute('''
            select td.image_obverse, c.coin_id, cs.total_spending, cs.owners
            from coin_statistics cs
            inner join coin c on c.coin_id = cs.coin_id
            inner join token_details td on td.token_details_id = c.token_details_id
            order by 
        ''' + field + ' desc').fetchmany(num)

    def get_banknote_statistics_top(self, field, num):
        return self.cursor.execute('''
            select td.image_obverse, b.banknote_id, bs.total_spending, bs.owners
            from banknote_statistics bs
            inner join banknote b on b.banknote_id = bs.banknote_id
            inner join token_details td on td.token_details_id = b.token_details_id
            order by 
        ''' + field + ' desc').fetchmany(num)


connection = Connection()
