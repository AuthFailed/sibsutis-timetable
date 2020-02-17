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
                dbname=environ.get("db_name"),
                user=environ.get("db_username"),
                host=environ.get("db_host"),
                password=environ.get("db_password"),
                port=5432,
            )

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)
            conn.commit()

            answer = None
            try:
                answer = cursor.fetchall()
                if len(answer):
                    print("SQL answer:", dict(answer[0]), file=stderr)
                else:
                    print("SQL answer:", answer, file=stderr)
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
        query = f"SELECT {column} FROM users WHERE user_id = {user_id}"
        return cls.__execute(query)

    @classmethod
    def user_exists(cls, user_id):
        """Проверяем существование пользователя."""
        query = f"SELECT EXISTS(SELECT user_id FROM users WHERE user_id = {user_id})"
        return cls.__execute(query)

    @classmethod
    def get_person(cls, user_id):
        """Получаем пользователя из базы."""
        query = f"SELECT * FROM users WHERE user_id={user_id}"
        result = cls.__execute(query)
        if not result:
            cls.__execute(f"INSERT INTO users (user_id) VALUES ({user_id})")
            cls.__execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        cls.__execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        return result

    @classmethod
    def change_faculty(cls, user_id, faculty):
        """Смена факультета пользователя."""
        query = f"UPDATE users SET faculty = '{faculty}' WHERE user_id = {user_id}"
        return cls.__execute(query)

    @classmethod
    def change_course(cls, user_id, course):
        """Смена курса пользователя."""
        query = f"UPDATE users SET course = {course} WHERE user_id = {user_id}"
        return cls.__execute(query)

    @classmethod
    def change_group(cls, user_id, group):
        """Смена группы пользователя."""
        query = f"UPDATE users SET \"group\" = '{group}' WHERE user_id = {user_id}"
        return cls.__execute(query)

    @classmethod
    def change_registration_date(cls, user_id):
        """Установка даты регистрации."""
        query = f"UPDATE users SET registration_date = NOW()::timestamp WHERE user_id = {user_id}"
        cls.__execute(query)

    @classmethod
    def get_user_count(cls):
        """Статистика людей по факультетам."""
        array = {
            "Count_All_Users": "",
            "MTS_Count": "",
            "MRM_Count": "",
            "IVT_Count": "",
            "AES_Count": "",
            "GF_Count": "",
        }
        array["Count_All_Users"] = cls.__execute(
            "SELECT COUNT(DISTINCT user_id) FROM users"
        )
        array["MTS_Count"] = cls.__execute(
            "SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = 'МТС'"
        )
        array["MRM_Count"] = cls.__execute(
            "SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = 'МРМ'"
        )
        array["IVT_Count"] = cls.__execute(
            "SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = 'ИВТ'"
        )
        array["AES_Count"] = cls.__execute(
            "SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = 'АЭС'"
        )
        array["GF_Count"] = cls.__execute(
            "SELECT COUNT(DISTINCT user_id) FROM users WHERE faculty = 'ГФ'"
        )
        return array

    @classmethod
    def get_files_versions(cls):
        """Статистика версий расписания"""
        array = {"Count_All_Groups": "", "Top_Groups": ""}
        array["Count_All_Groups"] = cls.__execute(
            "SELECT COUNT(DISTINCT file_name) FROM fs"
        )["count"]
        result = cls.__execute(
            "select * from fs order by version desc fetch first 10 rows only"
        )
        # i = 0
        # for group in result:
        #     print(group)
        #     i+=1
        #     array['Top_Groups'] += str(i) + ". " + group[0] + " | " + str(group[1]) + " \n"
        print(result)
        return array

    @classmethod
    def delete_person(cls, user_id):
        """Удаление пользователя из бд."""
        query = f"DELETE FROM users WHERE user_id={user_id}"
        cls.__execute(query)

    @classmethod
    def update_time(cls, file_name, update_time):
        """Дата последнего изменения файла."""
        if (
            len(cls.__execute(f"SELECT version FROM fs WHERE file_name='{file_name}'"))
            == 0
        ):
            query = f"INSERT INTO fs (file_name, update_time) VALUES ('{file_name}', '{update_time}')"
        else:
            query = f"UPDATE fs SET update_time='{update_time}', version={cls.get_version(file_name)['version'] + 1} WHERE file_name='{file_name}'"
        cls.__execute(query)

    @classmethod
    def get_version(cls, file_name):
        """Получение версии файла."""
        query = f"SELECT version FROM fs WHERE file_name='{file_name}'"
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
