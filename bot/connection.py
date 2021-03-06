import psycopg2

from player import Player

"""def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
"""


def insert_player(user_id, chat_id=0):
    conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost", dbname="expbot", user="postgres", password="HoZGnEAPL3xP6H")
        cur = conn.cursor()

        if user_id is not None:
            cur.execute("""insert into player (user_id, chat_id, level, experience, experience_next_level)
                           VALUES (%s, %s, 1, 0, (select experience_next_level from rank where level = 1))""",
                        (user_id, chat_id))

        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete_player(user_id, chat_id=0):
    conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost", dbname="expbot", user="postgres", password="HoZGnEAPL3xP6H")
        cur = conn.cursor()

        if user_id is not None:
            cur.execute("""delete from player where user_id = %s and chat_id = %s""", (user_id, chat_id))

        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_player(user_id, chat_id):
    conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost", dbname="expbot", user="postgres", password="HoZGnEAPL3xP6H")
        cur = conn.cursor()
        cur.execute("""select * from player where user_id = %s and chat_id = %s""", (user_id, chat_id))
        row = cur.fetchone()
        cur.close()
        if row is not None:
            return Player(row[0], row[1], row[2], row[3], row[4])
        else:
            return None
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def gain_exp(user_id, chat_id=0):
    conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost", dbname="expbot", user="postgres", password="HoZGnEAPL3xP6H")
        cur = conn.cursor()

        if user_id is not None:
            cur.execute("""update player set experience = experience + 1 where user_id = %s and chat_id = %s""",
                        (user_id, chat_id))

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def check_player_level_up(user_id, chat_id=0):
    conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost", dbname="expbot", user="postgres", password="HoZGnEAPL3xP6H")
        cur = conn.cursor()
        level_up = False
        player = get_player(user_id, chat_id)

        if player.experience_next_level != 0 and player.experience > player.experience_next_level:
            if user_id is not None:
                cur.execute("""update player set experience_next_level = (select experience_next_level from rank
                                                        where level = player.level + 1),
                                                 level = level + 1
                               where user_id = %s and chat_id = %s""",
                            (user_id, chat_id))
                level_up = True

        conn.commit()
        cur.close()
        return level_up
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_top_ten(chat_id=0):
    conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost", dbname="expbot", user="postgres", password="HoZGnEAPL3xP6H")
        cur = conn.cursor()
        cur.execute("select * from player where chat_id = " + str(chat_id) + " order by experience desc limit 10")
        row = cur.fetchone()
        leaderboard = []
        if row is not None:
            while row is not None:
                leaderboard.append(Player(row[0], row[1], row[2], row[3], row[4]))
                row = cur.fetchone()
        else:
            return None
        cur.close()
        return leaderboard
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_king(chat_id=0):
    conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost", dbname="expbot", user="postgres", password="HoZGnEAPL3xP6H")
        cur = conn.cursor()
        cur.execute("select * from player where chat_id = " + str(chat_id) + " order by experience desc limit 1")
        row = cur.fetchone()
        king = None
        if row is not None:
            king = Player(row[0], row[1], row[2], row[3], row[4])
        else:
            return None
        cur.close()
        return king
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def silence_chat(chat_id=0):
    conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost", dbname="expbot", user="postgres", password="HoZGnEAPL3xP6H")
        cur = conn.cursor()

        if chat_id is not None:
            cur.execute("select silence from chat where chat_id = " + str(chat_id))
            check = cur.fetchone()
            conn.commit()
            cur.execute("update chat set silence = not " + str(check[0]) + " where chat_id = " + str(chat_id))
            conn.commit()
            cur.close()
            return not check[0]

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def check_silence(chat_id=0):
    conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)
        conn = psycopg2.connect(host="localhost", dbname="expbot", user="postgres", password="HoZGnEAPL3xP6H")
        cur = conn.cursor()

        if chat_id is not None:
            cur.execute("select silence from chat where chat_id = " + str(chat_id))
            check = cur.fetchone()
            cur.close()
            return check[0]

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
