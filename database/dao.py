from database.DB_connect import DBConnect
from model.sighting import Sighting
from model.state import State

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_anni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT year(s_datetime) as anno
                    FROM sighting 
                    ORDER BY anno ASC """

        cursor.execute(query)

        for row in cursor:
            result.append(row['anno'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_shapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT shape  
                    FROM sighting 
                    WHERE shape != " " 
                    ORDER BY shape ASC"""

        cursor.execute(query)

        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from state"""

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi(shape, year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.state1 as stato1, n.state2  as stato2, COUNT(*) as N
                    FROM sighting s, neighbor n
                    WHERE (s.state = n.state1 OR s.state = n.state2)
                    AND s.shape = %s and year(s.s_datetime ) = %s
                    AND n.state1 < n.state2
                    GROUP BY stato1, stato2"""

        cursor.execute(query, (shape, year))
        for row in cursor:
            result.append((row['stato1'], row['stato2'], row['N']))

        cursor.close()
        conn.close()
        return result




