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
    def get_sighting():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM sighting ORDER BY s_datetime ASC"""

        cursor.execute(query)

        for row in cursor:
            result.append(Sighting(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_state():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM state """

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_shapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT shape FROM sighting WHERE shape != " " """

        cursor.execute(query)

        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_weighted_neighbors(a, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT LEAST(n.state1, n.state2) as st1, 
                    GREATEST(n.state1, n.state2) as st2,
                    COUNT(*) as N
                    FROM sighting s, neighbor n
                    WHERE year(s.s_datetime) = %s AND s.shape = %s
                    AND (s.state = n.state1 OR s.state = n.state2)
                    GROUP BY st1, st2"""

        cursor.execute(query, (a, shape))

        for row in cursor:
            result.append((row['st1'], row['st2'], row['N']))

        cursor.close()
        conn.close()
        return result






