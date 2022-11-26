import cx_Oracle
from enum import Enum
from verify_email import verify_email

from Utils import *


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
            
            END;
        ''', (username, password, email, GENERAL_COLLECTION_NAME, img)
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

    def get_user_deals_preview(self, username, active):
        if active:
            return self.cursor.execute("""
                SELECT coin.coin_id, td.value, currency.name, td.year, td.image_obverse, cd.price, cd.date_begin
                from  consumer c
                inner join coin_deal cd on cd.seller_id = c.consumer_id
                inner join coin on coin.coin_id = cd.coin_id
                inner join token_details td on td.token_details_id = coin.token_details_id
                inner join currency on currency.currency_id = td.currency_id
                where c.name = :username
                and cd.date_end is null
                order by cd.date_begin desc
            """, (username,))
        else:
            return self.cursor.execute("""
                SELECT coin.coin_id, td.value, currency.name, td.year, td.image_obverse, cd.price, cd.date_end
                from  consumer c
                inner join coin_deal cd on cd.seller_id = c.consumer_id
                inner join coin on coin.coin_id = cd.coin_id
                inner join token_details td on td.token_details_id = coin.token_details_id
                inner join currency on currency.currency_id = td.currency_id
                where c.name = :username
                and cd.date_end is not null
                order by cd.date_end desc
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
                    image_reverse, description, subject, diameter, weight, edge, collection_name):
        self.cursor.execute('''
            DECLARE
                var_token_type_id    NUMBER;
                var_material_id      NUMBER;
                var_currency_id      NUMBER;
                var_token_details_id NUMBER;
                var_edge_id          NUMBER;
                var_coin_details_id  NUMBER;
                var_coin_id          NUMBER;
                var_collection_id    NUMBER;
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
                
                SELECT
                    collection_id
                INTO var_collection_id
                FROM
                    collection
                WHERE
                    name = :collection_name;
            
                INSERT INTO collection_coin (
                    coin_id,
                    collection_id
                ) VALUES (
                    var_coin_id,
                    var_collection_id
                );
                
                COMMIT;
            END;
            ''', (token_type, material, currency_name, currency_country, value, year, image_obverse, image_reverse,
                  description, subject, edge, diameter, weight, collection_name)
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

    def update_coin(self, coin_id, value, currency_name, currency_country, year, token_type, material, image_obverse,
                    image_reverse, description, subject, diameter, weight, edge, collection_name):
        self.cursor.execute('''
            DECLARE
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
                    collection_id
                INTO var_collection_id
                FROM
                    collection
                WHERE
                    name = :collection_name;
                    
                UPDATE collection_coin 
                SET
                    collection_id = var_collection_id
                WHERE
                    coin_id = var_coin_id;
            
                COMMIT;
            END;
            ''', (coin_id, token_type, material, currency_name, currency_country, value, year, image_obverse,
                  image_reverse, description, subject, edge, diameter, weight, collection_name)
        )

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
        return True

    def create_deal(self, coin_id, price, deal_type):
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

    def cancel_deal(self, coin_id):
        self.cursor.execute('''
            DECLARE 
                var_coin_id NUMBER := :coin_id;
            BEGIN
                DELETE(
                    SELECT * FROM COIN_AUCTION_LOT cal
                    inner join COIN_DEAL cd ON cd.COIN_DEAL_ID = cal.COIN_DEAL_ID
                    where cd.coin_id = var_coin_id
                );
                DELETE FROM COIN_DEAL cd
                WHERE cd.coin_id = var_coin_id;
                COMMIT;
            END;
            ''', (coin_id, )
        )

    def get_deal_details(self, coin_id):
        deal_type = self.cursor.execute("""
            select type from deal_type dt
            inner join coin_deal cd on cd.deal_type_id = dt.deal_type_id
            where cd.coin_id = :coin_id
        """, (coin_id,)).fetchone()[0]
        if deal_type == 'Sale':
            return self.cursor.execute("""
                select c.image, c.name, cd.price
                FROM coin_deal cd
                inner join consumer c
                on c.consumer_id = cd.buyer_id
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
                            cal.price
                        FROM
                                 coin_deal cd
                            INNER JOIN coin_auction_lot cal ON cal.coin_deal_id = cd.coin_deal_id
                            INNER JOIN consumer         c ON c.consumer_id = cal.buyer_id
                        WHERE
                            cd.coin_id = :coin_id
                        ORDER BY
                            cal.price DESC
                    )
                WHERE
                    ROWNUM = 1
            """, (coin_id,)).fetchone()

    def refresh_deal_value(self, coin_id):
        deal_type = self.cursor.execute("""
                        select type from deal_type dt
                        inner join coin_deal cd on cd.deal_type_id = dt.deal_type_id
                        where cd.coin_id = :coin_id
                    """, (coin_id,)
                                        ).fetchone()[0]
        if deal_type == 'Sale':
            return self.cursor.execute("""   
                        select price from coin_deal where coin_id = :coin_id
                    """, (coin_id,)).fetchone()[0]
        else:
            return self.cursor.execute("""
                SELECT
                    *
                FROM
                    (
                        SELECT
                            cal.price
                        FROM
                                 coin_deal cd
                            INNER JOIN coin_auction_lot cal ON cal.coin_deal_id = cd.coin_deal_id
                        WHERE
                            cd.coin_id = :coin_id
                        ORDER BY
                            cal.price DESC
                    )
                WHERE
                    ROWNUM = 1

                    """, (coin_id,)).fetchone()[0]

    def approve_deal(self, coin_id):
        deal_type = self.cursor.execute("""
                select type from deal_type dt
                inner join coin_deal cd on cd.deal_type_id = dt.deal_type_id
                where cd.coin_id = :coin_id
            """, (coin_id,)
        ).fetchone()[0]
        if deal_type == 'Sale':
            self.cursor.execute("""   
                UPDATE coin_deal 
                SET date_end = SYSDATE
                WHERE coin_id = :coin_id
            """, (coin_id,)).fetchone()
            self.connection.commit()
        else:
            self.cursor.execute("""
                DECLARE
                    var_price       NUMBER;
                    var_buyer_id    NUMBER;
                BEGIN
                    SELECT
                        *
                    INTO var_buyer_id, var_price
                    FROM
                    (
                        SELECT
                            c.consumer_id,
                            cal.price
                        FROM
                                 coin
                            INNER JOIN coin_deal        cd ON cd.coin_id = coin.coin_id
                            INNER JOIN coin_auction_lot cal ON cal.coin_deal_id = cd.coin_deal_id
                            INNER JOIN consumer         c ON c.consumer_id = cal.buyer_id
                        WHERE
                            coin.coin_id = :coin_id
                        ORDER BY
                            cal.price DESC
                    )
                    WHERE
                        ROWNUM = 1;
                    
                    UPDATE coin_deal
                    SET buyer_id = var_buyer_id
                        price = var_price
                        end_date = SYSDATE;
                        
                    commit;
                    
            """, (coin_id,)).fetchone()

    def search_users(self, name):
        return self.cursor.execute("""
            SELECT
                t1.col_id,
                t1.col_name,
                t1.col_count,
                t2.image
            FROM
                     (
                    SELECT
                        c.consumer_id       AS col_id,
                        c.name              AS col_name,
                        COUNT(coin.coin_id) col_count
                    FROM
                             consumer c
                        INNER JOIN collection      coll ON coll.consumer_id = c.consumer_id
                        INNER JOIN collection_coin cc ON cc.collection_id = coll.collection_id
                        INNER JOIN coin ON coin.coin_id = cc.coin_id
                    WHERE
                        c.name like '%' || :name || '%'
                    GROUP BY
                        c.consumer_id,
                        c.name
                ) t1
                INNER JOIN consumer t2 ON t2.consumer_id = t1.col_id
        """, (name, )).fetchall()

    def search_collections(self, name):
        return self.cursor.execute("""
            SELECT
                t1.col_id,
                t1.col_name,
                t2.name,
                t1.col_count,
                t3.image
            FROM
                     (
                    SELECT
                        coll.collection_id  AS col_id,
                        coll.name           AS col_name,
                        coll.consumer_id    AS cons_id,
                        COUNT(coin.coin_id) AS col_count
                    FROM
                             collection coll
                        INNER JOIN collection_coin cc ON cc.collection_id = coll.collection_id
                        INNER JOIN coin ON coin.coin_id = cc.coin_id
                    WHERE
                        coll.name LIKE '%' || :name || '%' 
                            OR coll.description LIKE '%' || :name || '%' 
                    GROUP BY
                        coll.collection_id,
                        coll.name,
                        coll.consumer_id
                ) t1
                INNER JOIN consumer   t2 ON t2.consumer_id = t1.cons_id
                INNER JOIN collection t3 ON t3.collection_id = t1.col_id
        """, (name, name)).fetchall()

    def search_user_collections(self, user_id):
        return self.cursor.execute("""
            SELECT
                t1.col_id,
                t1.col_name,
                t2.name,
                t1.col_count,
                t3.image
            FROM
                     (
                    SELECT
                        coll.collection_id  AS col_id,
                        coll.name           AS col_name,
                        coll.consumer_id    AS cons_id,
                        COUNT(coin.coin_id) AS col_count
                    FROM
                             collection coll
                        INNER JOIN collection_coin cc ON cc.collection_id = coll.collection_id
                        INNER JOIN coin ON coin.coin_id = cc.coin_id
                    WHERE
                        coll.consumer_id = :user_id
                    GROUP BY
                        coll.collection_id,
                        coll.name,
                        coll.consumer_id
                ) t1
                INNER JOIN consumer   t2 ON t2.consumer_id = t1.cons_id
                INNER JOIN collection t3 ON t3.collection_id = t1.col_id
        """, (user_id, )).fetchall()

    def search_collection_coins(self, collection_id):
        return self.cursor.execute("""
            SELECT coin.coin_id, td.value, currency.name, td.year, td.subject, cons.name, td.image_obverse
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
            where c.collection_id = :collection_id
        """, (collection_id,)).fetchall()

    def search_coins_by_details(self, value, currency_name, currency_country, year, token_type, material, description,
                                subject, diameter, weight, edge):
        statement = """
            SELECT coin.coin_id, td.value, currency.name, td.year, td.subject, cons.name, td.image_obverse
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


connection = Connection()
