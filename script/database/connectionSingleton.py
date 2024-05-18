import psycopg2
from psycopg2.extensions import connection
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Informations de connexion
            hostname = '93.127.202.168'
            database = 'infinitcraft'
            username = 'infinitcraft'
            password = 'LucasYorick'
            port = 5432

            # Connexion à la base de données
            cls._instance.conn = psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=password,
                port=port
            )
        return cls._instance

    def get_connection(self) -> connection:
        return self.conn

# Exemple d'utilisation
if __name__ == "__main__":
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
        print(row)

    cur.close()
