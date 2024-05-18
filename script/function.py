from discord_webhook import DiscordWebhook, DiscordEmbed
import json


# Cette classe permet de gérer le LocalStorage d'une page Internet, donc de récupérer les informations, voire même de les retirer ou d'en ajouter
class LocalStorage:

    def __init__(self, driver) :
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()
    

# Cette fonction permet de reccuperer les emojis des élément qui on était fusionné

def get_element_emoji(element_name, json_data):
    elements = json_data["element_data"]["elements"]
    for element in elements:
        if element["text"] == element_name:
            return element["emoji"]
    return None

def get_element_discovered(element_name, json_data):
    elements = json_data["element_data"]["elements"]
    for element in elements:
        if element["text"] == element_name:
            return element["discovered"]
    return None

# Les quatre fontions suivantes permettent de journaliser toutes les actions effectuées par le script dans un webhook sur Discord.
def simple_log_embed(element1:list, element2:list, result:list):
    with open('webhook_data.json', encoding="utf-8") as f:
        data = json.load(f)
    
    webhookurl = data["simplelogwebhookurl"]
    webhook = DiscordWebhook(url=webhookurl, username="Simple log", avatar_url="https://png.pngtree.com/png-clipart/20190516/original/pngtree-log-file-format-icon-design-png-image_4307740.jpg")
    embed = DiscordEmbed(title="Simple log", color="03b2f8")
    embed.set_thumbnail("https://wordlenyt.io/upload/imgs/screenshot_411.png")
    with open('data.json', encoding="utf-8") as f:
        data = json.load(f)
    element1_emoji = get_element_emoji(element1, data)
    element2_emoji = get_element_emoji(element2, data)
    description = ""
    for i in range(len(element1)):
        description += f"{get_element_emoji(element1[i], data)} {element1[i]} ➡️ {get_element_emoji(element2[i], data)} {element2[i]} = {result[i][0]} {result[i][1]}\n"
    embed.set_description(description=description)
    webhook.add_embed(embed)
    response = webhook.execute()


def element_found_log_embed(element1:str, element2:str, result:list):
        with open('webhook_data.json', encoding="utf-8") as f:
            data = json.load(f)
    
        webhookurl = data["elementfoundwebhookurl"]
        webhook = DiscordWebhook(url=webhookurl, username="Simple log", avatar_url="https://png.pngtree.com/png-clipart/20190516/original/pngtree-log-file-format-icon-design-png-image_4307740.jpg")
        embed = DiscordEmbed(title="Découverte d'un élément.", color="03b2f8")
        embed.set_thumbnail("https://i.giphy.com/0GsNMsRwDKKMjiwIe5.gif")
        with open('data.json', encoding="utf-8") as f:
            data = json.load(f)
        element1_emoji = get_element_emoji(element1, data)
        element2_emoji = get_element_emoji(element2, data)
        embed.set_description(description=f"**J'ai découvert un nouvel élément ! Je suis tellement content !**\n```{element1_emoji} {element1} ➡️ {element2_emoji} {element2} = {result[0]} {result[1]}```")
        webhook.add_embed(embed)
        response = webhook.execute()


def element_never_founded_log_embed(element1, element2, result):
        with open('webhook_data.json', encoding="utf-8") as f:
            data = json.load(f)
    
        webhookurl = data["elementneverfoundwebhookurl"]
        webhook = DiscordWebhook(url=webhookurl, username="Simple log", avatar_url="https://png.pngtree.com/png-clipart/20190516/original/pngtree-log-file-format-icon-design-png-image_4307740.jpg")
        embed = DiscordEmbed(title="⭐ Découverte d'un élément que personne a jamais trouvé ! ⭐", color="03b2f8")
        embed.set_thumbnail("https://cdn.dribbble.com/users/2422127/screenshots/17320891/dancers.gif")
        with open('data.json', encoding="utf-8") as f:
            data = json.load(f)
        element1_emoji = get_element_emoji(element1, data)
        element2_emoji = get_element_emoji(element2, data)
        embed.set_description(description=f"**J'ai découvert un nouvel élément que personne n'avait jamais trouvé ! Je suis vraiment doué !**\n```{element1_emoji} {element1} ➡️ {element2_emoji} {element2} = {result[0]} {result[1]}```")
        webhook.add_embed(embed)
        response = webhook.execute()


def error_log_embed(element1:str, element2:str, result:list):
    with open('webhook_data.json', encoding="utf-8") as f:
        data = json.load(f)
    
    webhookurl = data["simplelogwebhookurl"]
    webhook = DiscordWebhook(url=webhookurl, username="Simple log erreur", avatar_url="https://png.pngtree.com/png-clipart/20190516/original/pngtree-log-file-format-icon-design-png-image_4307740.jpg")
    embed = DiscordEmbed(title="Simple log", color="03b2f8")
    embed.set_thumbnail("https://wordlenyt.io/upload/imgs/screenshot_411.png")
    with open('data.json', encoding="utf-8") as f:
        data = json.load(f)
    embed.set_description(description=f"{element1} ➡️ {element2} = ❌")
    webhook.add_embed(embed)
    response = webhook.execute()



# Cette fonction permet de sauvegarder les recettes des éléments grâce a un petit algorithme

def sauvegarder_recettes(element, recipe, data):
    existing_recipes = data['recettes'].get(element, [])

    for existing_recipe in existing_recipes:
        if (existing_recipe["recipe1"]["text"] == recipe["recipe1"]["text"] and
            existing_recipe["recipe2"]["text"] == recipe["recipe2"]["text"]) or \
           (existing_recipe["recipe1"]["text"] == recipe["recipe2"]["text"] and
            existing_recipe["recipe2"]["text"] == recipe["recipe1"]["text"]):
            return  # La recette existe déjà, donc on ne l'ajoute pas

    data['recettes'].setdefault(element, []).append(recipe)