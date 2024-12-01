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
from sys import argv, stdout
from time import sleep as timesleep
from datetime import datetime
from requests import get as requestget

# Our main, nice!
if __name__ == "__main__":
    appName = "gogtools-version detector"
    appVersion = "v0.0.6.1"
    appGithub = "https://github.com/jrie/gogtools"

    sysString = getSystemString()
    gogSystemString = "osx"  # Fallback

    if sysString == "Linux":
        gogSystemString = "linux"
    elif sysString == "Windows":
        gogSystemString = "windows"

    gogDirectory = oscurdir
    makeRemoteCheck = False
    ignoreDLC = False
    useHtml = False
    printUrls = False

    gameIdFile = "gt-gid.json"
    useGameIdFile = False

    cssStyle = 'body { background-color: #111; color: green; font-size: 1rem; } pre { background-color: #333; color: orange; font-size: 0.75rem; padding: 0.25rem 0.65rem; } a { text-decoration: none; color: green; font-size: inherit;} a:hover { cursor: pointer; color: lightgreen; }'
    appHtmlStart = f'<DOCTYPE html><html><head><title>{appName} {appVersion}</title><meta charset="utf-8" /><style type="text/css">{cssStyle}</style><body>'
    appHtmlEnd = '</body></html>'

    outputFile = stdout

    hasPrinted = False
    versionFiles = []

    def closeHTML():
        if useHtml:
            outputFile.write('</pre>')
            outputFile.write(appHtmlEnd)
            outputFile.close()

    def addHTML(string):
        if useHtml:
            outputFile.write(string)

    def printVersionAndSystem(forcePrint=False):
        global hasPrinted
        if hasPrinted and not forcePrint:
            return

        if useHtml:
            addHTML('<pre>')
            appGithubUrl = f'<a href="{appGithub}">{appGithub}</a>'
            print(
                f"You are running {appName} {appVersion}\n<br>For details, visit Github @ {appGithubUrl}",
                file=outputFile
            )
        else:
            print(
                f"You are running {appName} {appVersion}\nFor details, visit Github @ {appGithub}\n",
                file=outputFile
            )

        addHTML('</pre><pre>')

        print(
            f'{appName} called with the following parameters: "{argv[1:]}"', file=outputFile
        )

        addHTML('</pre><pre>')

        if sysString == "":
            print(
                f"{appName}: Operating system is not detected in script.\nPlease report this at Github @ {
                    appGithub}", file=outputFile
            )

            closeHTML()
            exit(1)
        else:
            print(f'{appName}: Your operating system is reported as "{
                  sysString}"', file=outputFile)

        print(f'Time of run: {datetime.now().strftime(
            "%d %B %Y on %H:%M:%S")}', file=outputFile)

        if not forcePrint:
            hasPrinted = True

    if len(argv) == 1:
        printVersionAndSystem()
        addHTML('<pre>')
        print(f"{appName}: Running in current folder.\n", file=outputFile)
    else:
        options, arguments = getopt(
            argv[1:], "i:o:rdwuc", ["gogDirectory", "operatingSystem", "makeRemoteCheck", "ignoreDLC", "writePrintToFile", "printUrls", "catchGameId"]
        )

        for option, value in options:
            if option == "-w":
                printVersionAndSystem(forcePrint=True)
                useHtml = True
                outputFile = open(f'gt-gvd-output_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.html', "w")
                addHTML(appHtmlStart + '\n')

        for option, value in options:
            if option == "-i":
                gogDirectory = value.rstrip(pathSeparator).strip()
            elif option == "-r":
                makeRemoteCheck = True
            elif option == "-d":
                ignoreDLC = True
            elif option == '-o':
                operatingSystemName = value.lower().strip()
                if operatingSystemName in ['windows', 'linux', 'osx']:
                    gogSystemString = operatingSystemName
                else:
                    printVersionAndSystem()
                    print(
                        f'{appName}: Unknown os string "-o osName" specified.\nUse "windows", "linux" or "osx" \nExiting.', file=outputFile)

                    closeHTML()
                    exit(6)
            elif option == '-u':
                printUrls = True
            elif option == '-c':
                useGameIdFile = True
                if not osexists(gameIdFile):
                    printVersionAndSystem()
                    print(f"\n{appName}: Game ID file '{gameIdFile}' does not exist.", file=outputFile)
                    closeHTML()
                    exit(7)

                if not osisfile(gameIdFile):
                    printVersionAndSystem()
                    print(f"\n{appName}: Game ID file '{gameIdFile}' is not a file.", file=outputFile)
                    closeHTML()
                    exit(8)

        if gogDirectory is None:
            printVersionAndSystem()

            print(
                f'{appName}: No input directory with "-i folder" specified, exiting.', file=outputFile)

            closeHTML()
            exit(2)

        if osexists(gogDirectory):
            if osisdir(gogDirectory):
                printVersionAndSystem()

                print(f'{appName}: Running in folder: "{
                      gogDirectory}"', file=outputFile)
            else:
                printVersionAndSystem()

                print(f'{appName}: "{
                      gogDirectory}" is not a directory.', file=outputFile)

                closeHTML()
                exit(3)
        else:
            printVersionAndSystem()
            print(f'{appName}: "{gogDirectory}" is not existing.', file=outputFile)

            closeHTML()
            exit(4)

    printVersionAndSystem()

    if makeRemoteCheck:
        print(f"{appName}: Remote check enabled.", file=outputFile)

    else:
        print(
            f"{appName}: Remote check is disabled. Enable using '-r' parameter.", file=outputFile)

    if ignoreDLC:
        print(f"{appName}: DLC detection is disabled.", file=outputFile)
    else:
        print(
            f"{appName}: DLC detection is enabled. Disable using '-d' parameter.", file=outputFile)

    if useHtml:
        print(f'{appName}: HTML generation enabled.', file=outputFile)
    else:
        print(
            f"{appName}: HTML generation disabled. Enable using '-w' parameter.", file=outputFile)

    if printUrls:
        print(f"{appName}: URL console output is enabled.", file=outputFile)
    else:
        print(
            f"{appName}: URL console output disabled. Enable using '-u' parameter.", file=outputFile)

    if useGameIdFile:
        print(f"{appName}: Read game id file '{gameIdFile}' is enabled.", file=outputFile)
    else:
        print(
            f"{appName}: Read game id file '{gameIdFile}' is disabled. Enable using '-c' parameter.", file=outputFile)


    if makeRemoteCheck or ignoreDLC:
        addHTML('</pre>')

    addHTML('<pre>')

    if useHtml:
        print(
            f"\n{appName}: Starting detection.. this might take a moment.", file=outputFile)
    else:
        print(f"\n{appName}: Starting detection.. this might take a moment.\n", file=outputFile)

    addHTML('</pre><pre>')

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

    noURLstring = 'No URL available'
    missingGameId = " [GAME ID MISSING] "
    missingGameUrl = " [URL ERROR] "

    gameIdData = {}

    if useGameIdFile:
        with open(gameIdFile, "r") as inputFile:
            for line in inputFile:
                jsonLine = jsonloads(line)
                gameId = jsonLine['gameId']
                gameTitle = jsonLine['title']
                gameSlug = jsonLine['slug']
                gameType = jsonLine['productType']
                gameUrl = jsonLine['url']

                gameIdData[gameTitle.lower()] = {
                    'gameId': int(gameId),
                    'title': gameTitle,
                    'slug': gameSlug,
                    'type': gameType,
                    'url': gameUrl
                }

    for versionFile in versionFiles:
        isDLC = False
        hasInteralId = False
        hasOSsupport = False
        hasGameIdMatch = False
        with open(versionFile, "r", encoding="utf-8") as inputFile:
            if versionFile.endswith("gameinfo"):
                fileData = inputFile.read().split("\n", 5)
                gameName = fileData[0]
                gameVersion = fileData[1]
                gameLanguage = fileData[2]
                if len(fileData) > 4:
                    gameId = fileData[4]
                else:
                    if useGameIdFile:
                        gameNameLower = gameName.lower()
                        for gameNameKey in gameIdData.keys():
                            if gameNameKey.find(gameNameLower) != -1:
                                gameId = gameIdData[gameNameKey]['gameId']
                                hasGameIdMatch = True
                                break

                    if not hasGameIdMatch:
                        gameId = internalId
                        hasInteralId = True

                        print(f'{appName}: [Status: ---] : "{gameName}" {missingGameId}', file=outputFile)
                        internalId += 1
                        gogItemLink = ""
                        gog = 0

            elif versionFile.endswith(".info"):
                jsonData = jsonload(inputFile)
                jsonKeys = jsonData.keys()

                if "name" in jsonKeys:
                    gameName = jsonData["name"]
                else:
                    print(
                        f'{appName}: Error reading out "name" from file: "{
                            inputFile}".\nPlease report this at Github @ {appGithub}', file=outputFile
                    )

                    closeHTML()
                    exit(5)

                if "gameId" in jsonKeys:
                    gameId = jsonData["gameId"]
                else:
                    print(
                        f'{appName}: Error reading out "gameId" from file: "{
                            inputFile}".\nPlease report this at Github @ {appGithub}', file=outputFile
                    )

                    closeHTML()
                    exit(5)

                if "version" in jsonKeys:
                    gameVersion = jsonData["version"]

                if "rootGameId" in jsonKeys:
                    rootId = jsonData["rootGameId"]

                    if gameId != rootId:
                        if ignoreDLC:
                            continue

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
                    print(
                        f"{gameName:>60} ==> Not present in Windows registry", file=outputFile)
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
                    gameIdMatchString = ""
                    if hasGameIdMatch:
                        gameIdMatchString = f'  [MATCHED GAME ID]'
                    print(f'{appName}: [Status: {gogData.status_code}] : "{
                          gameName}"{gameIdMatchString}', file=outputFile)

                    if gogData.status_code == 404:
                        gogErrorCode = gogData.status_code
                        gogItemLink = ""
                        break

                    if gogData.status_code != 200:
                        retries += 1
                        if retries == 4:
                            print(
                                f'{appName}: Error reading game info "{gameName}" from Gog.com.. error code: {
                                    gogData.status_code}\nCheck your internet connection.\nIf the error persists, please report this at Github @ {appGithub}', file=outputFile
                            )

                            closeHTML()
                            exit(6)

                        timesleep(15)
                        continue

                    jsonData = jsonloads(gogData.text)
                    gogItemLink = jsonData["links"]["product_card"]

                    if (
                        "downloads" in jsonData.keys()
                        and "installers" in jsonData["downloads"].keys()
                    ):
                        for installer in jsonData["downloads"]["installers"]:
                            if installer["os"].lower() != gogSystemString:
                                continue

                            if installer["name"] != gameName:
                                pass

                            if installer["version"] != None:
                                gogVersionOnline = installer["version"]
                            else:
                                gogVersionOnline = "No version reported by Gog"

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

            gogStatus[gameId] = {}

            if gogErrorCodeString == '':
                if gogUpdateString != '':
                    gogStatus[gameId]['text'] = f"{gameNameString}{typeString} ==> {gameVersionString}{gogUpdateString:<48}{compatibleString}"
                else:
                    gogStatus[gameId]['text'] = f"{gameNameString}{typeString} ==> {gameVersionString}{gogUpdateString:<48}{compatibleString}"
            else:
                gogStatus[gameId]['text'] = f"{gameNameString}{typeString} ==> {gameVersionString}{gogErrorCodeString:<48}"

            gogStatus[gameId]['name'] = gameNameString
            gogStatus[gameId]['link'] = gogItemLink
            gogStatus[gameId]['urlstatus'] = gogErrorCode

    addHTML('</pre><pre>')

    if not useHtml:
        print(164 * '-', file=outputFile)

    urlTypeString = ' [ URL  ]'

    for game in sorted(detectedGames):
        gameId = gamesProcessed[game]
        status = gogStatus[gameId]['text']
        gameLink = gogStatus[gameId]['link']

        if gogStatus[gameId]['urlstatus'] == 404:
            gameLinkUrl = f'{noURLstring} {missingGameUrl}'
        elif gogStatus[gameId]['urlstatus'] == 0:
            gameLinkUrl = f'{noURLstring} {missingGameId}'

        if gameLink != "":
            if useHtml:
                gameLinkUrl = f'<a href="{gameLink}">{gogStatus[gameId]["name"]}</a>'
                gogStatus[gameId]["text"] = gogStatus[gameId]["text"].replace(gogStatus[gameId]["name"], gameLinkUrl)
            else:
                gameLinkUrl = gameLink

        print(gogStatus[gameId]["text"], file=outputFile)

        if printUrls:
            if useHtml and gameLink != "":
                gameLinkUrl = f'<a href="{gameLink}">{gameLink}</a>'
                print(f'{" ":>60}{urlTypeString}{" ":>5}{gameLinkUrl}', file=outputFile)
            else:
                print(f'{" ":>60}{urlTypeString}{" ":>5}{gameLinkUrl}', file=outputFile)


        if gameId in detectedDLCs:
            for dlc in detectedDLCs[gameId]:
                dlcStatus = gogStatus[dlc]["text"]
                dlcLink = gogStatus[dlc]["link"]
                detectedGameFoldersLinkUrl = ""
                dlcLinkUrl = f'{noURLstring}'

                if gogStatus[dlc]['urlstatus'] == 404:
                    dlcLinkUrl = f'{noURLstring} {missingGameUrl}'
                elif gogStatus[dlc]['urlstatus'] == 0:
                    dlcLinkUrl = f'{noURLstring} {missingGameId}'

                if dlcLink != "":
                    if useHtml:
                        dlcLinkUrl = f'<a href="{dlcLink}">{gogStatus[dlc]["name"]}</a>'
                        gogStatus[dlc]["text"] = gogStatus[dlc]["text"].replace(
                            gogStatus[dlc]["name"], dlcLinkUrl)
                    else:
                        dlcLinkUrl = dlcLink

                print(gogStatus[dlc]["text"], file=outputFile)

                if printUrls:
                    if useHtml and dlcLink != "":
                        dlcLinkUrl = f'<a href="{dlcLink}">{dlcLink}</a>'
                        print(f'{" ":>60}{urlTypeString}{" ":>5}{dlcLinkUrl}', file=outputFile)
                    else:
                        print(f'{" ":>60}{urlTypeString}{" ":>5}{dlcLinkUrl}', file=outputFile)

        print('', file=outputFile)

    print(f"\n{appName}: Detected {countGames} game(s) ({internalId} without game id) and {
          countDLCs} DLC(s).", file=outputFile)

    addHTML(f"{appName}: Finished run. Enjoy your day!")
    print(f"{appName}: Finished run. Enjoy your day!")

    closeHTML()
