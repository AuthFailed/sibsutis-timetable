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
                    print('SQL answer:', dict(answer[0]), file=stderr)
                else:
                    print('SQL answer:', answer, file=stderr)
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
    def execute(cls, query):
        return cls.__execute(query)

    @classmethod
    def get_info(cls, user_id, column):
        """Получаем информацию об определенном пользователе."""
        query = f'SELECT {column} FROM users WHERE user_id = {user_id}'
        return cls.__execute(query)

    @classmethod
    def user_exists(cls, user_id):
        """Проверяем существование пользователя."""
        query = cls.__execute(f'SELECT * FROM users WHERE user_id = {user_id}')
        if not query:
            return False
        else:
            return True

    @classmethod
    def get_person(cls, user_id):
        """Получаем пользователя из базы."""
        query = f'SELECT * FROM users WHERE user_id={user_id}'
        result = cls.__execute(query)
        if not result:
            cls.__execute(f'INSERT INTO users (user_id) VALUES ({user_id})')
            cls.__execute(f'SELECT * FROM users WHERE user_id = {user_id}')
        cls.__execute(f'SELECT * FROM users WHERE user_id = {user_id}')
        return result

    @classmethod
    def change_faculty(cls, user_id, faculty):
        """Смена факультета пользователя."""
        query = f'UPDATE users SET faculty = \'{faculty}\' WHERE user_id = {user_id}'
        return cls.__execute(query)

    @classmethod
    def change_course(cls, user_id, course):
        """Смена курса пользователя."""
        query = f'UPDATE users SET course = {course} WHERE user_id = {user_id}'
        return cls.__execute(query)

    @classmethod
    def change_group(cls, user_id, group):
        """Смена группы пользователя."""
        query = f'UPDATE users SET \"group\" = \'{group}\' WHERE user_id = {user_id}'
        return cls.__execute(query)

    @classmethod
    def change_registration_date(cls, user_id):
        """Установка даты регистрации."""
        query = f'UPDATE users SET registration_date = NOW()::timestamp WHERE user_id = {user_id}'
        cls.__execute(query)

    @classmethod
    def get_user_count(cls):
        """Статистика людей по факультетам."""
        array = []
        result = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM users")
        array.append(result['count'])
        mst_count = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = \'МТС\'")
        array.append(mst_count['count'])
        mrm_count = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = \'МРМ\'")
        array.append(mrm_count['count'])
        ivt_count = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = \'ИВТ\'")
        array.append(ivt_count['count'])
        aes_count = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = \'АЭС\'")
        array.append(aes_count['count'])
        gf_count = cls.__execute("SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = \'ГФ\'")
        array.append(gf_count['count'])
        return array

    @classmethod
    def change_show_audience_status(cls, user_id, status):
        """Смена форматирования - показ аудитории."""
        query = f'UPDATE users SET show_audience = {status} WHERE user_id = {user_id}'
        return cls.__execute(query)

    @classmethod
    def change_show_teacher_status(cls, user_id, status):
        """Смена форматирования - показ преподавателя."""
        query = f'UPDATE users SET show_teacher = {status} WHERE user_id = {user_id}'
        return cls.__execute(query)

    @classmethod
    def delete_person(cls, user_id):
        """Удаление пользователя из бд."""
        query = f"DELETE FROM users WHERE user_id={user_id}"
        cls.__execute(query)

    @classmethod
    def update_time(cls, file_name, update_time):
        """Дата последнего изменения файла."""
        if len(cls.__execute(f"SELECT version FROM fs WHERE file_name=\'{file_name}\'")) == 0:
            query = f"INSERT INTO fs (file_name, update_time) VALUES (\'{file_name}\', \'{update_time}\')"
        else:
            query = f"UPDATE fs SET update_time=\'{update_time}\', version=\'{cls.get_version(file_name)['version'] + 1}\'"
        cls.__execute(query)

    @classmethod
    def get_version(cls, file_name):
        """Получение версии файла."""
        query = f"SELECT version FROM fs WHERE file_name=\'{file_name}\'"
        result = cls.__execute(query)
        return result

    @classmethod
    def get_files_stats(cls):
        """Получение статистики по обновлению расписания."""
        query = f"select * from fs"
        return cls.__execute(query)

    @classmethod
    def truncate_table(cls):
        """Очистка базы."""
        query = "TRUNCATE TABLE users"
        cls.__execute(query)
