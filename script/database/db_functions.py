
from database.connectionSingleton import DatabaseConnection #appelle depuis main
from database.Craft import Craft #appelle depuis main

class DbTools():
    @staticmethod
    def get_craft_many(): 
        craftArr = []

        db = DatabaseConnection()
        conn = db.get_connection()
        cur = conn.cursor()
        query = """
        SELECT id, libelle, emoji, discovered, created_at
        FROM craft
        """

        cur.execute(query)
        rows = cur.fetchall()

        for row in rows:
            id = row[0]
            libelle = row[1]
            emoji = row[2]
            discovered = row[3]
            created_at = row[4]
            craft = Craft(id=id, libelle=libelle, emoji=emoji, discovered=discovered, created_at=created_at)
            craftArr.append(craft)
            

        cur.close()
        return craftArr
    def get_craft(libelle_query: str):
        craftArr = []

        db = DatabaseConnection()
        conn = db.get_connection()
        cur = conn.cursor()

        # Define the prepared statement using psycopg2.sql
        query = """
            SELECT id, created_at, discovered, emoji, libelle
            FROM public.craft
            WHERE libelle ILIKE %s
        """

        # Execute the prepared statement with parameters
        cur.execute(query, (libelle_query,))

        rows = cur.fetchall()

        for row in rows:
            id, created_at, discovered, emoji, libelle = row
            craft = Craft(id=id, libelle=libelle, emoji=emoji, discovered=discovered, created_at=created_at)
            craftArr.append(craft)

        cur.close()
        return craftArr