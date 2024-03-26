#!/usr/bin/env python3
"""
    gogtools - version detector and retriever
"""
# Python stuff
from getopt import getopt
from glob import glob
from json import load as jsonload, loads as jsonloads
from os import sep as pathSeparator, listdir as oslistdir
from os.path import (
    exists as osexists,
    isdir as osisdir,
    curdir as oscurdir,
    isfile as osisfile,
)
from platform import system as getSystemString
from re import search as research
from subprocess import run as runprocess
from sys import argv
from time import sleep as timesleep
from requests import get as requestget

# Our main, nice!
if __name__ == "__main__":
    appName = "gogtools-version detector"
    appVersion = "v0.0.1"
    appGithub = "https://github.com/jrie/gogtools"

    sysString = getSystemString()
    gogSystemString = "osx"  # Fallback

    if sysString == "Linux":
        gogSystemString = "linux"
    elif sysString == "Windows":
        gogSystemString = "windows"

    gogDirectory = oscurdir
    makeRemoteCheck = False

    versionFiles = []

    print(
        f"You are running {appName} {appVersion}\nFor details, visit Github @ {appGithub}\n"
    )

    if sysString == "":
        print(
            f"{appName}: Operating system is not detected in script.\nPlease report this at Github @ {appGithub}"
        )
        exit(1)
    else:
        print(f'{appName}: Your operating system is reported as "{sysString}"')

    if len(argv) == 1:
        print(f"{appName}: Running in current folder.\n")
    else:
        options, arguments = getopt(
            argv[1:], "i:o:r", ["gogDirectory", "operatingSystem", "makeRemoteCheck"]
        )

        for option, value in options:
            if option == "-i":
                gogDirectory = value.rstrip(pathSeparator).strip()
            elif option == "-r":
                makeRemoteCheck = True
            elif option == '-o':
                operatingSystemName = value.lower().strip()
                if operatingSystemName in ['windows', 'linux', 'osx']:
                    gogSystemString = operatingSystemName
                else:
                    print(f'{appName}: Unknown os string "-o osName" specified.\nUse "windows", "linux" or "osx" \nExiting.')
                    exit(6)

        if gogDirectory is None:
            print(f'{appName}: No input directory with "-i folder" specified, exiting.')
            exit(2)

        if osexists(gogDirectory):
            if osisdir(gogDirectory):
                print(f'{appName}: Running in folder: "{gogDirectory}"')
            else:
                print(f'{appName}: "{gogDirectory}" is not a directory.')
                exit(3)
        else:
            print(f'{appName}: "{gogDirectory}" is not existing.')
            exit(4)

    print(f"{appName}: Starting detection.. this might take a moment.\n")

    gameRootFolder = f"{gogDirectory}{pathSeparator}"
    detectedGameFolders = sorted(oslistdir(gameRootFolder))

    for entry in detectedGameFolders:
        gameInfoPath = f"{gameRootFolder}{entry}{pathSeparator}gameinfo"
        if osisfile(gameInfoPath):
            versionFiles.append(gameInfoPath)

    detectedGameFolders = sorted(oslistdir(gameRootFolder))

    for entry in detectedGameFolders:
        gameGogInfoPath = f"{entry}{pathSeparator}"
        versionFiles.extend(
            sorted(
                glob(f"{gameRootFolder}{gameGogInfoPath}**{pathSeparator}goggame*.info", recursive=True)
            )
        )

    gamesProcessed = {}
    detectedGames = []
    detectedDLCs = {}
    gameDLCs = {}
    gogStatus = {}

    countGames = 0
    countDLCs = 0
    internalId = 0

    for versionFile in versionFiles:
        isDLC = False
        hasInteralId = False
        hasOSsupport = False

        with open(versionFile, "r", encoding="utf-8") as inputFile:
            if versionFile.endswith("gameinfo"):
                fileData = inputFile.read().split("\n", 5)
                gameName = fileData[0]
                gameVersion = fileData[1]
                gameLanguage = fileData[2]
                if len(fileData) > 4:
                    gameId = fileData[4]
                else:
                    gameId = internalId
                    hasInteralId = True
                    internalId += 1

            elif versionFile.endswith(".info"):
                jsonData = jsonload(inputFile)
                jsonKeys = jsonData.keys()

                if "name" in jsonKeys:
                    gameName = jsonData["name"]
                else:
                    print(
                        f'{appName}: Error reading out "name" from file: "{inputFile}".\nPlease report this at Github @ {appGithub}'
                    )
                    exit(5)

                if "gameId" in jsonKeys:
                    gameId = jsonData["gameId"]
                else:
                    print(
                        f'{appName}: Error reading out "gameId" from file: "{inputFile}".\nPlease report this at Github @ {appGithub}'
                    )
                    exit(5)

                if "version" in jsonKeys:
                    gameVersion = jsonData["version"]

                if "rootGameId" in jsonKeys:
                    rootId = jsonData["rootGameId"]

                    if gameId != rootId:
                        if not rootId in gameDLCs:
                            gameDLCs[rootId] = [gameId]
                        else:
                            gameDLCs[rootId].append(gameId)

                        isDLC = True

            if sysString == "Windows":
                result = runprocess(
                    f"reg query HKLM\\SOFTWARE\\WOW6432Node\\GOG.com\\Games\\{gameId} /v ver",
                    capture_output=True,
                    check=False,
                )

                if result.returncode != 0:
                    print(f"{gameName:>60} ==> Not present in Windows registry")
                    continue

                gameVersionWindows = research(
                    r"REG_SZ[\ ]+([^\r\n]*)", result.stdout.decode()
                )
                if gameVersionWindows is not None:
                    gameVersion = gameVersionWindows.group(1).lstrip("vV")

            if gameName in gamesProcessed.keys():
                continue

            gogVersionOnline = None
            gogErrorCode = 0
            hasVersion = False
            hasOSsupport = True

            if makeRemoteCheck and gameId != 0 and not hasInteralId:
                retries = 0
                while True:
                    gogErrorCode = 0
                    gogData = requestget(
                        f"https://api.gog.com/products/{gameId}?locale=en_US&expand=downloads",
                        timeout=30,
                    )

                    print(f'{appName}: [Status: {gogData.status_code}] : "{gameName}"')

                    if gogData.status_code == 404:
                        gogErrorCode = gogData.status_code
                        break

                    if gogData.status_code != 200:
                        retries += 1
                        if retries == 4:
                            print(
                                f'{appName}: Error reading game info "{gameName}" from Gog.com.. error code: {gogData.status_code}\nCheck your internet connection.\nIf the error persists, please report this at Github @ {appGithub}'
                            )
                            exit(6)

                        timesleep(15)
                        continue

                    jsonData = jsonloads(gogData.text)

                    if (
                        "downloads" in jsonData.keys()
                        and "installers" in jsonData["downloads"].keys()
                    ):
                        for installer in jsonData["downloads"]["installers"]:
                            if installer["os"].lower() != gogSystemString:
                                continue

                            if installer["name"] != gameName:
                                pass

                            gogVersionOnline = installer["version"].lstrip("vV")
                            hasVersion = True
                            hasOSsupport = True
                            break

                        if hasVersion:
                            break

                        if gogSystemString in jsonData["content_system_compatibility"].keys() and jsonData["content_system_compatibility"][gogSystemString] != True:
                            gogVersionOnline = jsonData["downloads"]["installers"][0][
                                "version"
                            ]
                            hasOSsupport = False
                            break

                    timesleep(0.12)
                    break

            gamesProcessed[gameName] = gameId

            if not isDLC:
                detectedGames.append(gameName)
                countGames += 1
            else:
                if not rootId in detectedDLCs:
                    detectedDLCs[rootId] = [gameId]
                else:
                    detectedDLCs[rootId].append(gameId)
                countDLCs += 1


            gameNameString = f'{gameName:>60}'
            gameVersionString = f'{gameVersion:<32}'

            if not isDLC:
                typeString = ' [ GAME ]'
            else:
                typeString = ' [ DLC  ]'

            if gogErrorCode != 0 and gogErrorCode != 200:
                gogErrorCodeString = f' [Error code: {gogErrorCode}] '
            else:
                gogErrorCodeString = ''

            if gogVersionOnline is not None and gameVersion != gogVersionOnline:
                gogUpdateString = f' [Update available: {gogVersionOnline}]'
            else:
                gogUpdateString = ''

            if not hasOSsupport:
                compatibleString = f'No {gogSystemString}'
            else:
                compatibleString = ''

            if gogErrorCodeString == '':
                if gogUpdateString != '':
                    gogStatus[gameId] = f"{gameNameString}{typeString} ==> {gameVersionString}{gogUpdateString:<52}{compatibleString}"
                else:
                    gogStatus[gameId] = f"{gameNameString}{typeString} ==> {gameVersionString}{gogUpdateString:<52}{compatibleString}"
            else:
                gogStatus[gameId] = f"{gameNameString}{typeString} ==> {gameVersionString}{gogErrorCodeString:<52}"

    print(164 * '-')
    for game in sorted(detectedGames):
        gameId = gamesProcessed[game]
        status = gogStatus[gameId]
        print(gogStatus[gameId])
        if gameId in detectedDLCs:
            for dlc in detectedDLCs[gameId]:
                print(gogStatus[dlc])

    print(f"\n{appName}: Detected {countGames} game(s) and {countDLCs} DLC(s).")
    print(f"{appName}: Finished run. Enjoy your day!")
