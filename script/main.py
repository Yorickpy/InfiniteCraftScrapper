from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from function import LocalStorage
import json, time, emoji, sys
from itertools import combinations
from function import simple_log_embed, element_found_log_embed, element_never_founded_log_embed, error_log_embed, sauvegarder_recettes, get_element_emoji, get_element_discovered
from discord_webhook import DiscordWebhook
import undetected_chromedriver as uc

chrome_options = uc.ChromeOptions()


#init driver
driver = uc.Chrome(options=chrome_options)
driver.get("https://neal.fun/infinite-craft/")
driver.maximize_window()
time.sleep(5)
element = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]" )
element.click()


# input("Press enter to start auto crafting")


def check_if_element_already_get(general_data, request_data):
    result_exists = False
    for element in general_data['element_data']['elements']:
        if element['text'] == request_data['result'] and element['emoji'] == request_data['emoji'] and element['discovered'] == request_data['isNew']:
            result_exists = True
            break
    return result_exists



fusion_element1_log_list = []
fusion_element2_log_list = []
fusion_result_log_list = []

def fusion_element(element1, element2):
    global fusion_element1_log_list, fusion_element2_log_list, fusion_result_log_list
    api_url = f"https://neal.fun/api/infinite-craft/pair?first={element1}&second={element2}"



    script = f"""
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "{api_url}", false);  // false indique une requête synchrone
    xhr.send(null);
    return xhr.responseText;;
    """

    fusion_info = driver.execute_script(script)
    
    try:
        fusion_info = json.loads(fusion_info)
    except Exception as e:
        print(e)
        print(fusion_info)
    

    if fusion_info["emoji"] == "":
        print(f"{element1} > {element2} Ne Fontionne pas")
        result_list = ["❌", "❌"]
        error_log_embed(element1, element2, result_list)
        return



    if fusion_info["emoji"]!="":
        result_emoji = fusion_info["emoji"]
        result_element = fusion_info["result"]
        print(f"{element1} > {element2} = {result_emoji} {result_element}")

    with open('data.json', encoding="utf-8") as f:
        data = json.load(f)

    result_exists = check_if_element_already_get(data, fusion_info)

    if result_exists == False:
        with open('data.json', encoding="utf-8") as f:
            data = json.load(f)
        data["element_data"]["elements"].append({"text":fusion_info["result"], "emoji":fusion_info["emoji"], "discovered":fusion_info["isNew"]})
        with open('data.json', 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"{element1} > {element2} = {result_emoji} {result_element} ELEMENT AJOUTER AU DONNEE")
        result_list = [result_emoji, result_element]
        
        if fusion_info["isNew"] == True:
            result_list = [result_emoji, result_element]

            element_never_founded_log_embed(element1, element2, result_element)
        else:
            element_found_log_embed(element1, element2, result_list)
    else:
        print(f"{element1} > {element2} = {result_emoji} {result_element} ELEMENT DEJA DECOUVERT")
    result_list = [fusion_info["emoji"],fusion_info["result"]]
    
    
    if len(fusion_element1_log_list) >=10:
        print(fusion_element1_log_list)
        print(fusion_element2_log_list)
        print(fusion_result_log_list)
        simple_log_embed(fusion_element1_log_list, fusion_element2_log_list, fusion_result_log_list)
        fusion_element1_log_list = []
        fusion_element2_log_list = []
        fusion_result_log_list = []
        fusion_element1_log_list.append(element1)
        fusion_element2_log_list.append(element2)
        fusion_result_log_list.append((fusion_info["emoji"], fusion_info["result"]))
    else:
        fusion_element1_log_list.append(element1)
        fusion_element2_log_list.append(element2)
        fusion_result_log_list.append((fusion_info["emoji"], fusion_info["result"]))
    
    with open('data.json', encoding="utf-8") as f:
        data = json.load(f)

    if element1 == result_element or element2 == result_element:
        return

    recipe1_text = element1
    recipe1_emoji = get_element_emoji(element1, data)
    recipe1_discovered = get_element_discovered(element1, data)

    recipe2_text = element2
    recipe2_emoji = get_element_emoji(element2, data)
    recipe2_discovered = get_element_discovered(element2, data)

    

    new_recipe = {
    "recipe1": {
        "text": recipe1_text,
        "emoji": recipe1_emoji,
        "discovered": recipe1_discovered
    },
    "recipe2": {
        "text": recipe2_text,
        "emoji": recipe2_emoji,
        "discovered": recipe2_discovered
        }
    }

    with open('recettes_data.json', encoding="utf-8") as f:
        data = json.load(f)

    sauvegarder_recettes(result_element, new_recipe, data)

    with open('recettes_data.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



try:
    while True:
        with open('data.json', encoding="utf-8") as f:
            data = json.load(f)


        element_list = []
        for i in data["element_data"]["elements"]:
            element_list.append(i["text"])


        def charger_donnees():
            try:
                with open('combinaisons.json', 'r') as fichier:
                    return set(map(tuple, json.load(fichier)))
            except FileNotFoundError:
                return set()


        def sauvegarder_donnees(combinaisons):
            with open('combinaisons.json', 'w') as fichier:
                json.dump(list(combinaisons), fichier)

        combinaisons_deja_faites = charger_donnees()


        liste_des_combinaisons = []
        for combinaison in combinations(element_list, 2):
            # Vérifier si la combinaison a déjà été réalisée (dans les deux sens)
            if combinaison[::-1] not in combinaisons_deja_faites:
                # Ajouter la combinaison à la liste
                liste_des_combinaisons.append(combinaison)
                # Ajouter la combinaison et sa permutation à l'ensemble des combinaisons déjà réalisées
                combinaisons_deja_faites.add(combinaison)
                combinaisons_deja_faites.add(combinaison[::-1])
                # Mettre à jour le fichier JSON
                sauvegarder_donnees(combinaisons_deja_faites)

                # Ton code pour la fusion des éléments ici
            
                fusion_info = fusion_element(combinaison[0], combinaison[1])
                time.sleep(0.25)

except KeyboardInterrupt:
        sys.exit()