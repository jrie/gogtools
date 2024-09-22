#!/usr/bin/env python3
"""
    gogtools - game id retriever
"""
# Python stuff
from json import loads as jsonloads, dumps as jsondump
from os.path import (
    exists as osexists,
    isfile as osisfile,
)
from time import sleep
from requests import get as requestget

# Our main, nice!
if __name__ == "__main__":
    appName = "gogtools-game-id-retriever"
    appVersion = "v0.0.2"
    appGithub = "https://github.com/jrie/gogtools"

    currentPage = 1
    forwardOption = '+'
    backwardOption = '-'
    doSearch = True
    versionRetrieverFile = 'gt-gid.json'

    print(f"You are running {appName} {appVersion}\nFor details, visit Github @ {appGithub}")
    print(f'All added information are added to the file: "{versionRetrieverFile}"')

    while True:
        if doSearch:
            currentPage = 1
            print('')
            searchValue = input('[Exit by entering "x"] --- Search Gog.com ==> ')
            searchValue = searchValue.lower().replace('_', ' ').strip()

            if searchValue == "x":
                break

            if len(searchValue) < 3:
                print(f'{appName} [ ERROR ] : Search value must be at least 3 characters long.')
                continue

        searchURL = f'https://catalog.gog.com/v1/catalog?limit=20&locale=en-US&page={currentPage}&order=desc:score&productType=in:game,pack,dlc&query=like:{searchValue}'
        gogData = requestget(searchURL, timeout=30)

        if gogData.status_code == 200:
            jsonData = jsonloads(gogData.text)
            if jsonData['productCount'] == 0:
                print(f'{appName} [STATUS 200] : Nothing found for query.')
                continue
            else:
                print(f'{appName} [STATUS 200] : Found the following items..\n')

                gameItems = {}

                for index, item in enumerate(jsonData['products']):
                    index += 1

                    if item["productType"] == "game":
                        itemType = "[ GAME ]"
                    elif item["productType"] == "dlc":
                        itemType = "[ DLC  ]"
                    elif item["productType"] == "pack":
                        itemType = "[ PACK ]"
                    else:
                        print(f'{appName} [ ERROR ] : Type "{item["productType"]}" is not recognized, please report this at Github @ {appGithubUrl}.')

                    intIndex = int(index)
                    gameItems[intIndex] = {}
                    gameItems[intIndex]['gameId'] = item["id"]
                    gameItems[intIndex]['title'] = item["title"]
                    gameItems[intIndex]['slug'] = item["slug"]
                    gameItems[intIndex]['productType'] = item["productType"]
                    gameItems[intIndex]['url'] = item["storeLink"]

                    print(f'{index:<2}) {itemType:<9} "{item["title"]}"')

                if jsonData['pages'] != 1:
                    print(f'\nYou are on page: {currentPage} of {jsonData["pages"]}')
                    print(f'{appName} use "{forwardOption}" to go forward and "{
                          backwardOption}" to go backward')

                print('')
                inputSelection = input('[Continue search by entering "c" or exit using "x"] --- Gog.com selection: ')
                inputSelection = inputSelection.lower().replace('_', ' ').strip()

                if inputSelection == "c":
                    doSearch = True
                    continue

                if inputSelection == "x":
                    break

                if jsonData['pages'] != 1:
                    pageInfo = f'{currentPage} of {jsonData["pages"]} total pages.'

                    if inputSelection == forwardOption:
                        if currentPage < jsonData['pages']:
                            currentPage += 1
                            doSearch = False
                        else:
                            print(f'{appName} : Cannot go forward. {pageInfo}')
                        continue
                    elif inputSelection == backwardOption:
                        if currentPage > 1:
                            currentPage -= 1
                            doSearch = False
                        else:
                            print(f'{appName} : Cannot go backward. {pageInfo}')
                        continue

                inputSelection = int(inputSelection, 10)
                if inputSelection in gameItems.keys():
                    currentItem = gameItems[inputSelection]
                    print(f'{appName} : Entry information.\n[TITLE   ] {currentItem["title"]}\n[TYPE    ] {
                          currentItem["productType"]}\n[GAME ID ] {currentItem["gameId"]}\n[URL     ] {currentItem["url"]}\n[SLUG    ] {currentItem["slug"]}')

                    print('')
                    inputSelection = input('[Exit by entering "x"] --- Add selection information to "{versionRetrieverFile}" (y/n): ')
                    inputSelection = inputSelection.lower().replace('_', ' ').strip()

                    if inputSelection == "x":
                        break
                    elif inputSelection == "y":
                        print(f'{appName} : Dumping data to "{versionRetrieverFile}"')

                        entryExists = False
                        if osexists(versionRetrieverFile) and osisfile(versionRetrieverFile):
                            outputFile = open(versionRetrieverFile, 'r')
                            existingData = outputFile.readlines()
                            dumpData = jsondump(currentItem)
                            for line in existingData:
                                if line.startswith(dumpData):
                                    entryExists = True
                                    break

                            outputFile.close()

                        if entryExists:
                            print(f'{appName} : "{versionRetrieverFile}" already has: "{currentItem["title"]}" with game id "{currentItem["gameId"]}"\n')
                            sleep(3)
                        else:
                            outputFile = open(versionRetrieverFile, 'a')
                            outputFile.write(jsondump(currentItem) + '\n')
                            outputFile.close()
                            print(f'{appName} : "{versionRetrieverFile}" entry added.\n')
                            sleep(3)

                    elif inputSelection == "n":
                        print(f'{appName} : Not writing information!\n')

                    doSearch = False
                    continue
                else:
                    print(f'{appName} : Input selection not found {inputSelection}')
                    doSearch = False
                    continue

        elif gogData.status_code == 404:
            print(f'{appName} [STATUS 404] : Gog.com catalog search not reachable.')
            continue

    print(f'\n{appName}: Finished run. Enjoy your day!')