from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.object import Object

# classe DAO
class DAO:
    def __init__(self):
        pass


    @staticmethod
    def readObjects():
        # apro connessione e cursore, creo la lista del risultato
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        # query
        query = ''' SELECT * FROM objects '''
        cursor.execute(query)
        for row in cursor:
            result.append(Object(row['object_id'], row['title']))

            # UNPACKING DEL DIZIONARIO
            #result.append(Object(**row))    -> unpacking del dizionario tirando fuori tutte le chiavi del dizionario e
            #                                   associando un valore (nella classe non si devono mettere gli underscore
            #                                   sugli attributi se no non funziona)

        # chiudo tutto e restituisco la lista
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def readConnessioni(objects_dict):      # riceve l'ID-MAP degli Object
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        # query per leggere le connessioni
        query = ''' SELECT eo1.object_id AS o1, eo2.object_id AS o2, COUNT(*) AS peso
                    FROM exhibition_objects eo1, exhibition_objects eo2
                    WHERE eo1.exhibition_id = eo2.exhibition_id AND eo1.object_id < eo2.object_id 
                    GROUP BY eo1.object_id, eo2.object_id '''
        cursor.execute(query)

        for row in cursor:
            o1 = objects_dict[row['o1']]
            o2 = objects_dict[row['o2']]
            peso = row['peso']
            result.append(Connessione(o1, o2, peso))      # costruisce una connessione

        cursor.close()
        conn.close()
        return result       # lista di oggetti di tipo Connessione