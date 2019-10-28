import psycopg2

import config

conn = psycopg2.connect(
    "dbname={} user={} password={} host={}".format(config.db_name, config.db_username, config.db_password,
                                                   config.db_url))
conn.autocommit = True
db = conn.cursor()

db.execute("CREATE TABLE IF NOT EXISTS Users (user_id serial PRIMARY KEY,\n"
           "            user_faculty VARCHAR DEFAULT Null,\n"
           "             user_course INTEGER DEFAULT 1,\n"
           "              user_group VARCHAR DEFAULT Null,\n"
           "               user_subscription BOOLEAN DEFAULT False,\n"
           "                user_mail VARCHAR DEFAULT Null,\n"
           "                 user_admin BOOLEAN DEFAULT False,\n"
           "                 reg_date DATE Default Null);")


def user_exists(user_id: object) -> object:
    db.execute('SELECT user_id FROM Users WHERE user_id = %s' % user_id)
    result = db.fetchall()
    if not result:
        return False
    else:
        return True


def get_person(user_id):
    # Существует ли юзер
    db.execute('SELECT * FROM Users WHERE user_id=%s' % user_id)
    if not db.fetchall():
        db.execute('INSERT INTO Users (user_id) VALUES (%s)' % user_id)
        db.execute('SELECT * FROM Users WHERE user_id=%s' % user_id)
    db.execute('SELECT * FROM Users WHERE user_id=%s' % user_id)
    return db.fetchall()


def get_info(user_id, column):
    db.execute('SELECT %s FROM Users WHERE user_id=%s' % (column, user_id))
    result = db.fetchall()
    return result


def change_group(user_id, group):
    db.execute('UPDATE Users SET user_group = \'%s\' WHERE user_id = %s' %
               (group, user_id))


def change_faculty(user_id, faculty):
    db.execute('UPDATE Users SET user_faculty = \'%s\' WHERE user_id = %s' % (
        faculty, user_id))


def change_course(user_id, course):
    db.execute('UPDATE Users SET user_course = \'%s\' WHERE user_id = %s' %
               (course, user_id))


def notification_status(user_id, status):
    db.execute('UPDATE Users SET user_subscription = \'%s\' WHERE user_id = %s' % (
        status, user_id))


def change_mail(user_id, mail):
    db.execute('UPDATE Users SET user_mail = \'%s\' WHERE user_id = %s' %
               (mail, user_id))


def change_reg_date(user_id, reg_date):
    db.execute('UPDATE Users SET reg_date = (to_date(\'%s\', \'YYYY-MM-DD\')) WHERE user_id = %s' %
               (reg_date, user_id))


def execute(query: object) -> object:
    db.execute(query)
    return str(db.fetchall())


def get_user_count():
    array = []
    db.execute("SELECT COUNT(DISTINCT user_id) FROM Users")
    array.append(str(db.fetchall()[0][0]))
    db.execute(
        "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'МТС\'")
    array.append(str(db.fetchall()[0][0]))
    db.execute(
        "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'МРМ\'")
    array.append(str(db.fetchall()[0][0]))
    db.execute(
        "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'ИВТ\'")
    array.append(str(db.fetchall()[0][0]))
    db.execute(
        "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'АЭС\'")
    array.append(str(db.fetchall()[0][0]))
    db.execute(
        "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'ГФ\'")
    array.append(str(db.fetchall()[0][0]))
    return array


def delete_person(user_id):
    db.execute("DELETE FROM Users WHERE user_id=%s" % user_id)


def delete_db():
    db.execute("DROP DATABASE Users")
