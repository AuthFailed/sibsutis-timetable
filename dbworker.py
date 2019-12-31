import psycopg2


class Database:
    """Класс для работы с базами данных."""

    def __init__(self, dbname, username, password, host):
        self.dbname = dbname
        self.username = username
        self.password = password
        self.host = host

        self._db_connection = psycopg2.connect(
            "dbname={0} user={1} password={2} host={3}".format(dbname, username, password, host))
        self._db_connection.autocommit = True
        self._db_cur = self._db_connection.cursor()

    def get_info(self, user_id, column):
        """Получаем информацию об определенном пользователе."""
        self._db_cur.execute('SELECT %s FROM Users WHERE user_id=%s' % (column, user_id))
        result = self._db_cur.fetchall()
        return result

    def user_exists(self, user_id):
        """Проверяем существование пользователя."""
        self._db_cur.execute('SELECT user_id FROM Users WHERE user_id = %s' % user_id)
        result = self._db_cur.fetchall()
        if not result:
            return False
        else:
            return True

    def get_person(self, user_id):
        """Получаем пользователя из базы."""
        self._db_cur.execute('SELECT * FROM Users WHERE user_id=%s' % user_id)
        if not self._db_cur.fetchall():
            self._db_cur.execute('INSERT INTO Users (user_id) VALUES (%s)' % user_id)
            self._db_cur.execute('SELECT * FROM Users WHERE user_id=%s' % user_id)
        self._db_cur.execute('SELECT * FROM Users WHERE user_id=%s' % user_id)
        return self._db_cur.fetchall()

    def change_faculty(self, user_id, faculty):
        """Смена факультета пользователя."""
        self._db_cur.execute('UPDATE Users SET user_faculty = \'%s\' WHERE user_id = %s' % (
            faculty, user_id))

    def change_course(self, user_id, course):
        """Смена курса пользователя."""
        self._db_cur.execute('UPDATE Users SET user_course = \'%s\' WHERE user_id = %s' %
                             (course, user_id))

    def change_group(self, user_id, group):
        """Смена группы пользователя."""
        self._db_cur.execute('UPDATE Users SET user_group = \'%s\' WHERE user_id = %s' %
                             (group, user_id))

    def change_reg_date(self, user_id, reg_date):
        """Установка даты регистрации."""
        self._db_cur.execute('UPDATE Users SET reg_date = (to_date(\'%s\', \'YYYY-MM-DD\')) WHERE user_id = %s' %
                             (reg_date, user_id))

    def execute(self, query):
        """Кастомный запрос к базе."""
        self._db_cur.execute(query)
        if not self._db_cur.fetchall():
            return str(self._db_cur.fetchall())

    def get_user_count(self):
        """Статистика людей по факультетам."""
        array = []
        self._db_cur.execute("SELECT COUNT(DISTINCT user_id) FROM Users")
        array.append(str(self._db_cur.fetchall()[0][0]))
        self._db_cur.execute(
            "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'МТС\'")
        array.append(str(self._db_cur.fetchall()[0][0]))
        self._db_cur.execute(
            "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'МРМ\'")
        array.append(str(self._db_cur.fetchall()[0][0]))
        self._db_cur.execute(
            "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'ИВТ\'")
        array.append(str(self._db_cur.fetchall()[0][0]))
        self._db_cur.execute(
            "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'АЭС\'")
        array.append(str(self._db_cur.fetchall()[0][0]))
        self._db_cur.execute(
            "SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'ГФ\'")
        array.append(str(self._db_cur.fetchall()[0][0]))
        return array

    def change_show_audience_status(self, user_id, status):
        """Смена форматирования - показ аудитории."""
        self._db_cur.execute('UPDATE Users SET show_audience = {} WHERE user_id = {}'.format(status, user_id))

    def change_show_teacher_status(self, user_id, status):
        """Смена форматирования - показ преподавателя."""
        self._db_cur.execute('UPDATE Users SET show_teacher = {} WHERE user_id = {}'.format(status, user_id))

    def delete_person(self, user_id):
        """Удаление пользователя из бд."""
        self._db_cur.execute("DELETE FROM Users WHERE user_id=%s" % user_id)

    def update_time(self, file_name, update_time):
        """Дата последнего изменения файла."""
        self._db_cur.execute(f"""INSERT INTO fs (file_name, update_time, version)
                                 VALUES ({file_name}, {update_time})
                                 ON CONFLICT (file_name) DO UPDATE
                                    SET update_time={update_time}, version={self.get_version({file_name})+1}""")

    def get_version(self, file_name):
        """Получение версии файла."""
        return self._db_cur.execute("SELECT version FROM fs WHERE file_name=%s" % file_name)

    def truncate_table(self):
        """Очистка базы."""
        self._db_cur.execute("TRUNCATE TABLE users")
