from psycopg2.extras import RealDictCursor
from os import environ
from sys import stderr
import psycopg2
import traceback


class Database:
    """Класс для работы с базами данных."""

    @staticmethod
    def __execute(query):
        """Метод для выполнения SQL запросов."""

        try:
            conn = psycopg2.connect(
                dbname=environ.get('db_name'),
                user=environ.get('db_username'),
                host=environ.get('db_host'),
                password=environ.get('db_password'),
                port=5432
            )

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)
            conn.commit()

            answer = None
            try:
                answer = cursor.fetchall()
                if len(answer):
                    print('SQL answ:', dict(answer[0]), file=stderr)
                else:
                    print('SQL answ:', answer, file=stderr)
            except psycopg2.Error as err:
                print(err, file=stderr)
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
                if answer:
                    return dict(answer[0])
                else:
                    return answer
        except psycopg2.OperationalError:
            traceback.print_exc()
            return dict(error=dict(message="Database connection refused"))

    @classmethod
    def get_info(cls, user_id, column):
        """Получаем информацию об определенном пользователе."""
        query = 'SELECT %s FROM Users WHERE user_id=%s' % (column, user_id)
        return cls.__execute(query)

    @classmethod
    def user_exists(cls, user_id):
        """Проверяем существование пользователя."""
        query = 'SELECT * FROM Users WHERE user_id = %s' % user_id
        if not query:
            return False
        else:
            return True

    @classmethod
    def get_person(cls, user_id):
        """Получаем пользователя из базы."""
        query = 'SELECT * FROM Users WHERE user_id=%s' % user_id
        result = cls.__execute(query)
        if not result:
            cls.__execute('INSERT INTO Users (user_id) VALUES (%s)' % user_id)
            cls.__execute('SELECT * FROM Users WHERE user_id=%s' % user_id)
        cls.__execute('SELECT * FROM Users WHERE user_id=%s' % user_id)
        return result

    @classmethod
    def change_faculty(cls, user_id, faculty):
        """Смена факультета пользователя."""
        query = 'UPDATE Users SET user_faculty = \'%s\' WHERE user_id = %s' % (faculty, user_id)
        return cls.__execute(query)

    @classmethod
    def change_course(cls, user_id, course):
        """Смена курса пользователя."""
        query = 'UPDATE Users SET user_course = \'%s\' WHERE user_id = %s' % (course, user_id)
        return cls.__execute(query)

    @classmethod
    def change_group(cls, user_id, group):
        """Смена группы пользователя."""
        query = 'UPDATE Users SET user_group = \'%s\' WHERE user_id = %s' % (group, user_id)
        return cls.__execute(query)

    @classmethod
    def change_reg_date(cls, user_id, reg_date):
        """Установка даты регистрации."""
        query = 'UPDATE Users SET reg_date = (to_date(\'%s\', \'YYYY-MM-DD\')) WHERE user_id = %s' % (reg_date, user_id)
        cls.__execute(query)

    @classmethod
    def get_user_count(cls):
        """Статистика людей по факультетам."""
        array = []
        result = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM Users")
        print(result)
        # array.append(str(result[0])
        # result = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'МТС\'")
        # array.append(str(result[0]))
        # result = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'МРМ\'")
        # array.append(str(result[0]))
        # result = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'ИВТ\'")
        # array.append(str(result[0]))
        # result = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'АЭС\'")
        # array.append(str(result[0]))
        # result = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM Users where user_faculty=\'ГФ\'")
        # array.append(str(result[0]))
        return array

    @classmethod
    def change_show_audience_status(cls, user_id, status):
        """Смена форматирования - показ аудитории."""
        query = 'UPDATE Users SET show_audience = {} WHERE user_id = {}'.format(status, user_id)
        return cls.__execute(query)

    @classmethod
    def change_show_teacher_status(cls, user_id, status):
        """Смена форматирования - показ преподавателя."""
        query = 'UPDATE Users SET show_teacher = {} WHERE user_id = {}'.format(status, user_id)
        return cls.__execute(query)

    @classmethod
    def delete_person(cls, user_id):
        """Удаление пользователя из бд."""
        query = f"DELETE FROM Users WHERE user_id={user_id}"
        return cls.__execute(query)

    @classmethod
    def update_time(cls, file_name, update_time):
        """Дата последнего изменения файла."""
        query = f"""INSERT INTO fs (file_name, update_time)
                                 VALUES (\'%s\', \'%s\')
                                 ON CONFLICT (file_name) DO UPDATE
                                    SET update_time=\'%s\', version=\'%i\'""" % (file_name, update_time, update_time, int(cls.get_version(file_name)[0][0])+1)
        return cls.__execute(query)

    @classmethod
    def get_version(cls, file_name):
        """Получение версии файла."""
        query = f"SELECT version FROM fs WHERE file_name=\'{file_name}\'"
        return cls.__execute()

    @classmethod
    def truncate_table(cls):
        """Очистка базы."""
        query = "TRUNCATE TABLE users"
        cls.__execute(query)
