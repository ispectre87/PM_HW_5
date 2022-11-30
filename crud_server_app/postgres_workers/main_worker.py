from psycopg.rows import dict_row

from handlers.events_handlers import pool

class MainDatabaseWorker:
    def __init__(self, pool=pool):
        self._pool = pool

    def _execute_query(self, query: str, values: tuple = None):
        """Executes queries to database, returns Cursor object"""
        with self._pool.connection() as conn:
            conn.row_factory = dict_row
            return conn.execute(query, values)

    def _create_record(self, query: str, values: tuple) -> dict:
        print('00----', query, values)
        try:
            self._execute_query(query, values)
        except Exception:
            return {"Error": "Record not created"}
        return {"Success": "Record created"}

    def _read_record(self, query: str) -> list:
        try:
            result = self._execute_query(query)
        except Exception as e:
            print("exx", e)
            return [{"Error": "Wrong identificator"}]
        else:
            return result.fetchall()

    def _update_record(self, query: str) -> dict:
        try:
            self._execute_query(query)
        except Exception as e:
            print("eexx", e)
            return {"Error": "Update failed"}
        else:
            return {"Success": "Record updated"}

    def _delete_record(self, query: str) -> dict:
        try:
            self._execute_query(query)
        except Exception:
            return {"Error": "Record not deleted"}
        return {"Success": "Record deleted"}