import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import pandas as pd
import re

LOCATION_URL_PREPEND = "https://www.serebii.net/pokedex-dp/location/"
MAIN_PAGE_URL_PREPEND = "https://www.serebii.net/pokedex-dp/"
SHTML_URL_APPEND = ".shtml"
GEN_4_NUMBER_OF_POKEMON = 493

def location_to_table_row(dex_number, pokemon_name, location_tr):
    """Retrieve the location name, rarity, method, minimum level and maximum
    level from table row and return the information in a list with dex number
    and pokemon name
    """
    
    data = location_tr.findAll('td')
    locationName = data[0].a.text
    rarity = data[1].text
    method = data[4].text
    minLevel = data[5].text
    maxLevel = data[6].text
    
    return [dex_number, pokemon_name, locationName,
            rarity, method, minLevel, maxLevel]

def ss_trade_to_table(df, dex_number, pokemon_name):
    """Add a line to the df dataframe with dex number, pokemon name and 'Trade
    from SoulSilver' as Location Name
    """
    
    df.loc[dex_number] = [dex_number, pokemon_name, 'Trade from SoulSilver',
                          '', '', '', '']

def get_best_location_in_hg_table(hg_table):
    """Go through the locations in heartgold where pokemon appears and return
    the one with the best chance of appearing
    """
    
    locations = hg_table.findAll("tr", recursive=False)[2:]

    best_location = locations[0]
    best_rarity = 0
    locRarity = (best_location.findAll("td")[1]
                              .text
                              .strip(' %'))
    if locRarity.isnumeric():
        best_rarity = int(locRarity)

    for loc in locations[1:]:
        locRarity = (loc.findAll("td")[1]
                        .text
                        .strip(" %"))
        
        if not locRarity.isnumeric():
            continue
        
        rarityNumber = int(locRarity)
        if rarityNumber > best_rarity:
            best_location = loc
            best_rarity = rarityNumber
    
    return best_location

def get_locations_soup(dex_number):
    """Access the pokemon locations page and return its html as a BeautifulSoup
    object
    """
    
    url = (LOCATION_URL_PREPEND
           + str(dex_number).zfill(3)
           + SHTML_URL_APPEND)

    text = (urllib.request
                  .urlopen(url)
                  .read())
    
    return BeautifulSoup(text, 'html.parser')

def get_pokemon_name(locations_soup, dex_number):
    """Return the pokemon name"""
    
    return (locations_soup.find("b", string=re.compile(str(dex_number)))
	                      .text[6:])

def get_best_hg_location(df, locations_soup, dex_number, pokemon_name):
    """Find the heartgold table, get the tr element for the best location and
    insert the data in the dataframe
    """
    
    hg_table = (locations_soup.find("a", string="HeartGold")
                              .findParent("table"))
    
    bestLocation = get_best_location_in_hg_table(hg_table)
    df.loc[dex_number] = location_to_table_row(dex_number, pokemon_name,
                                               bestLocation)

def get_hg_location_from_main_page(df, dex_number, pokemon_name):
    """Access the pokemon main page, find the heartgold location and insert the
    data in the dataframe
    """
    
    url = (MAIN_PAGE_URL_PREPEND
           + str(dex_number).zfill(3)
           + SHTML_URL_APPEND)

    text = (urllib.request
                  .urlopen(url)
                  .read())
    
    soup = BeautifulSoup(text, 'html.parser')
    
    hg_location = (soup.find("b", string="Location")
                       .findParent("table")
                       .find("td", class_="heartgold")
                       .find_next("td")
                       .text
                       .strip())
    
    df.loc[dex_number] = [dex_number, pokemon_name, hg_location, '', '', '', '']

def insert_pokemon_location(df, dex_number):
    """Insert the data of the best location to obtain pokemon in the dataframe
    """
    
    locations_soup = get_locations_soup(dex_number)
    pokemon_name = get_pokemon_name(locations_soup, dex_number)

    if locations_soup.find("a", string="HeartGold") is not None:
        get_best_hg_location(df, locations_soup, dex_number, pokemon_name)
    elif locations_soup.find("a", string="SoulSilver") is not None:
        ss_trade_to_table(df, dex_number, pokemon_name)
    else:
        get_hg_location_from_main_page(df, dex_number, pokemon_name)

def main():
    # setup dataframe
    df = pd.DataFrame(columns=['Dex No.', 'Pokémon', 'Location', 'Rarity',
                               'Method', 'MinLevel', 'MaxLevel'])

    # insert data for every pokemon in generation 4
    for dex_number in range(1, GEN_4_NUMBER_OF_POKEMON+1):
        try:
            insert_pokemon_location(df, dex_number)
        except urllib.error.URLError as error:
            print(f"Error at dex_number {dex_number} with type {error}")
            continue

    # save data into .csv file
    df.to_csv("hgDex.csv", index=False)

if __name__ == "__main__":
    main()