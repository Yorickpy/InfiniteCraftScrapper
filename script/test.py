import datetime
from database.db_functions import DbTools
from database.Craft import Craft
craft = Craft(created_at=datetime.date.today(), emoji="😀", discovered=False, id=1, libelle="content")

arr = DbTools.get_craft_many()

for element in arr :
    print(element)

print("test 2")
arr2 = DbTools.get_craft("Water")

for element2 in arr2 :
    print(element2)