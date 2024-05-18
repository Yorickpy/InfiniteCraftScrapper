import datetime
from database.db_functions import DbTools
from database.Craft import Craft

def main():
    all = DbTools.get_craft_all()

    recipe1 = all[500]
    recipe2 = all[600]
    parent = all[700]

    print(recipe1)
    print(recipe2)
    print(parent)
    DbTools.create_recette(parent=parent, recipe1=recipe1, recipe2=recipe2)


main()
