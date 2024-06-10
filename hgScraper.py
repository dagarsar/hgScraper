import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=['Dex No.', 'Pokémon', 'Location', 'Rarity', 'Method', 'MinLevel', 'MaxLevel', 'Caught'])


for i in range(1, 494):
    url = "https://www.serebii.net/pokedex-dp/location/" + str(i).zfill(3) + ".shtml"

    text = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(text, 'html.parser')
    
    pokemon = soup.find("table", class_="dextable").findAll("tr")[1].findAll("td")[2].text.strip()
    
    # print(f'{i} {pokemon}')

    if soup.find("a", string="HeartGold") != None:
        hgTable = soup.find("a", string="HeartGold").findParent("table")

        hgLocations = hgTable.findAll("tr", recursive=False)

        bestLocation = hgLocations[2]
        bestRarity = 0
        locRarity = bestLocation.findAll("td")[1].text.strip(' %')
        if locRarity.isnumeric():
            bestRarity = int(locRarity)

        for loc in hgLocations[3:]:
            locRarity = loc.findAll("td")[1].text.strip(" %")
            if not locRarity.isnumeric():
                continue
            rarityNumber = int(locRarity)
            if rarityNumber > bestRarity:
                bestLocation = loc
                bestRarity = rarityNumber

        data = bestLocation.findAll("td")
        locationName = data[0].a.text
        rarity = data[1].text
        method = data[4].text
        minLevel = data[5].text
        maxLevel = data[6].text
        
        df.loc[i] = [i, pokemon, locationName, rarity, method, minLevel, maxLevel, '']

        # print(f'location: {locationName}; rarity: {rarity}; method: {method}; level: {minLevel} to {maxLevel}')
    elif soup.find("a", string="SoulSilver") != None:
        df.loc[i] = [i, pokemon, 'Trade from SoulSilver', '', '', '', '', '']
    else:
        url = "https://www.serebii.net/pokedex-dp/" + str(i).zfill(3) + ".shtml"

        text = urllib.request.urlopen(url).read()

        soup = BeautifulSoup(text, 'html.parser')
        
        dexTables = soup.findAll("table", class_="dextable")
        hgLocation = ""
        
        for dexTable in dexTables:
            if dexTable.findAll("td")[0].b != None and dexTable.findAll("td")[0].b.text == "Location":
                # print(dexTable.prettify())
                hgLocation = dexTable.find("td", class_="heartgold").findParent("tr").findAll("td")[1].text.strip()
                break
        
        df.loc[i] = [i, pokemon, hgLocation, '', '', '', '', '']
        
        # print(hgLocation)

df.to_csv("hgDex.csv", index=False)
            