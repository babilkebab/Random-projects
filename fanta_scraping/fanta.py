from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from prettyprinter import pprint
import pandas

def get_role(rl):
    if(rl == 'a'):
        return 'Attaccante'
    elif(rl == 'c'):
        return 'Centrocampista'
    elif(rl == 'd'):
        return 'Difensore'
    return 'Portiere'



def scrape_fanta(url):
    driver = webdriver.Chrome(options = chrome_options)
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "qc-cmp2-close-icon"))).click()


    #SKIPPO ALL'ultimo
    pager = driver.find_element(By.ID, "pager")
    buttons = pager.find_elements(By.TAG_NAME, "li")
    _ = buttons.pop()
    last = buttons.pop()
    driver.execute_script("arguments[0].click();", last)



    players = driver.find_element(By.ID, "stats")
    tbody = players.find_element(By.TAG_NAME, 'tbody')

    #IL CODICE SOTTO PER PIGLIARE LE RIGHE DI UNA TABELLA
    players_stats = []
    players_table = tbody.find_elements(By.TAG_NAME, "tr")
    for row in players_table:
        #if len(row.text) == 0:
        #   break
        name = (row.find_element(By.CLASS_NAME, "player-name")).find_element(By.TAG_NAME, "span").get_attribute("textContent")
        role = get_role((row.find_element(By.CLASS_NAME, "role")).get_attribute("data-value"))
        club = (row.find_element(By.CLASS_NAME, "player-team")).get_attribute("textContent").replace(" ", "").replace("\n", "")
        matches = int((row.find_element(By.CLASS_NAME, "player-match-playeds")).get_attribute("textContent").replace(" ", "").replace("\n", ""))
        if matches < 15:
            continue
        avg = float((row.find_element(By.CLASS_NAME, "player-grade-avg")).get_attribute("textContent").replace(" ", "").replace("\n", "").replace(",", "."))
        favg = float((row.find_element(By.CLASS_NAME, "player-fanta-grade-avg")).get_attribute("textContent").replace(" ", "").replace("\n", "").replace(",", "."))
        goals = int((row.find_element(By.CLASS_NAME, "player-scoreds")).get_attribute("textContent").replace(" ", "").replace("\n", ""))
        assists = int((row.find_element(By.CLASS_NAME, "player-assists")).get_attribute("textContent").replace(" ", "").replace("\n", ""))
        list_row = [name, club, role, matches, avg, favg, goals, assists]
        players_stats.append(list_row)
    #FINO A QUA
    dataframe = pandas.DataFrame(players_stats, columns=['Calciatore', 'Squadra', 'Ruolo', 'Partite con voto', 'Media voto', 'Fantamedia', 'Gol', 'Assist'])
    print("Finito")
    return dataframe


chrome_options = Options()
chrome_options.add_argument("--headless")
    
season_22_23 = scrape_fanta("https://www.fantacalcio.it/statistiche-serie-a/2022-23")
season_21_22 = scrape_fanta("https://www.fantacalcio.it/statistiche-serie-a/2021-22")
season_20_21 = scrape_fanta("https://www.fantacalcio.it/statistiche-serie-a/2020-21")
seasons_21_23 = pandas.merge(season_21_22, season_22_23, on = "Calciatore")
all_seasons = pandas.merge(season_20_21, seasons_21_23, on = "Calciatore")
pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)


players_means = pandas.DataFrame([], columns=['Calciatore', 'Ruolo', 'Voto medio', 'Fantamedia', 'Gol medi', 'Assist medi', 'Varianza gol', 'Varinv'])
players_means['Calciatore'] = all_seasons['Calciatore']
players_means['Ruolo'] = all_seasons['Ruolo']
players_means['Voto medio'] = round((all_seasons['Media voto'] + all_seasons["Media voto_x"] + all_seasons["Media voto_y"])/3,2)
players_means['Fantamedia'] = round((all_seasons['Fantamedia'] + all_seasons["Fantamedia_x"] + all_seasons["Fantamedia_y"])/3,2)
players_means['Gol medi'] = round((all_seasons['Gol'] + all_seasons["Gol_x"] + all_seasons["Gol_y"])/3)
players_means['Assist medi'] = round((all_seasons['Assist'] + all_seasons["Assist_x"] + all_seasons["Assist_y"])/3)
players_means['Varianza gol'] = round((all_seasons['Gol']**2 + all_seasons["Gol_x"]**2 + all_seasons["Gol_y"]**2)/3 - ((all_seasons['Gol'] + all_seasons["Gol_x"] + all_seasons["Gol_y"])/3)**2, 2)
players_means['Varinv'] = players_means['Varianza gol'].max() - players_means['Varianza gol']


final = pandas.DataFrame([], columns=['Calciatore', 'Ruolo', 'Punteggio'])
final['Calciatore'] = players_means['Calciatore']
final['Ruolo'] = players_means['Ruolo']
final_attcen = pandas.DataFrame([], columns=['Calciatore', 'Ruolo', 'Punteggio'])
final_dif = pandas.DataFrame([], columns=['Calciatore', 'Ruolo', 'Punteggio'])
final_por = pandas.DataFrame([], columns=['Calciatore', 'Ruolo', 'Punteggio'])
final_attcen = final[(final['Ruolo'] == 'Attaccante') | (final['Ruolo'] == 'Centrocampista')]
final_dif = final[final['Ruolo'] == 'Difensore']
final_por = final[final['Ruolo'] == 'Portiere']
final_attcen['Punteggio'] = ((players_means["Gol medi"] - players_means["Gol medi"].mean())/players_means["Gol medi"].var()) + ((players_means["Fantamedia"] - players_means["Fantamedia"].mean())/players_means["Fantamedia"].var()) + ((players_means["Varinv"] - players_means["Varinv"].mean())/players_means["Varinv"].var())
final_dif['Punteggio'] = ((players_means["Gol medi"] - players_means["Gol medi"].mean())/players_means["Gol medi"].var()) + ((players_means["Voto medio"] - players_means["Voto medio"].mean())/players_means["Voto medio"].var()) + ((players_means["Varinv"] - players_means["Varinv"].mean())/players_means["Varinv"].var())
final_por['Punteggio'] = 0
final = pandas.concat([final_attcen, final_dif, final_por])
final.to_excel("fanta_stats.xlsx")