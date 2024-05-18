
from database.connectionSingleton import DatabaseConnection #appelle depuis main
from database.Craft import Craft #appelle depuis main
from typing import List
from psycopg2.errors import UniqueViolation


class DbTools():

    @staticmethod
    def get_craft_all(): 
        craftArr: List[Craft] = []

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
    @staticmethod
    def get_craft(libelle: str):
        try:
            db = DatabaseConnection()
            conn = db.get_connection()
            cur = conn.cursor()

            # Define the prepared statement using psycopg2.sql
            query = """
                SELECT id, libelle, emoji, discovered, created_at
                FROM public.craft
                WHERE libelle ILIKE %s
            """

            # Execute the prepared statement with parameters
            try:
                cur.execute(query, (libelle,))
                row = cur.fetchone()
                return Craft(id=row[0], libelle=row[1], emoji=row[2], discovered=row[3], created_at=row[4])
            except TypeError as e:
                print("Erreur de type, surement aucun resultat trouve")
                return None;
            except Exception as e:
                print("Erreur non  prevu de type : ", e.__class__)
                print("message d erreur: ", e)
                return None;
            finally:
                cur.close()
        except Exception as e:
            print(f"impossible de se connectre a la base de donnees: {str(e)}")
            raise Exception(f"impossible de se connectre a la base de donnees:: {str(e)}")
    @staticmethod
    def create_craft(craft: Craft):
        try:
            db = DatabaseConnection()
            conn = db.get_connection()
            cur = conn.cursor()

            query = """
                INSERT INTO craft (libelle, emoji, discovered) VALUES 
                (%s, %s, %s)
            """

            try:
                cur.execute(query, (craft.libelle, craft.emoji, craft.discovered))
            except UniqueViolation as e:
                print(f"impossible de lancer la requete le le champ existe deja")
                print(e)

            conn.commit()
            cur.close()
        except Exception as e:
            print(f"impossible de se connecter a la base de donnees: {str(e)}")
            raise Exception(f"impossible de se connecter a la base de donnees: {str(e)}")
    @staticmethod
    def create_recette(parent: Craft, recipe1: Craft, recipe2: Craft):
        try:
            db = DatabaseConnection()
            conn = db.get_connection()
            cur = conn.cursor()

            query = """
                INSERT INTO public.recette (id_enfant1, id_enfant2, id_parent)
                VALUES (%s, %s, %s) ; 
            """
            if (parent.isId and recipe1.isId and recipe2.isId):
                try:
                    cur.execute(query, (recipe1.id, recipe2.id, parent.id))
                except UniqueViolation as e:
                    print(f"impossible de lancer la requete le le champ existe deja")
                    print(e)
                except Exception as e:
                    print(f"Erreur non prevu de type : {e.__class__}")
                    print("message d erreur", e)

                conn.commit()
                cur.close()
            else:
                print(f"""
                parent: {"✅" if parent.isId() else "❌"}
                recipe1: {"✅" if recipe1.isId() else "❌"}
                recipe2: {"✅" if recipe2.isId() else "❌"}
                """)
        except Exception as e:
            print(f"impossible de se connecter a la base de donnees: {str(e)}")
            raise Exception(f"impossible de se connecter a la base de donnees: {str(e)}")
