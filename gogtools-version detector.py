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
    appVersion = "v0.0.3"
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

    hasPrinted = False
    versionFiles = []

    cssStyle = 'body { background-color: #111; color: green; font-size: 1rem; } pre { background-color: #333; color: orange; font-size: 0.75rem; padding: 0.25rem 0.65rem; } a { text-decoration: none; color: green; font-size: inherit;} a:hover { cursor: pointer; color: lightgreen; }'
    appHtmlStart = f'<DOCTYPE html><html><head><title>{appName} {appVersion}</title><meta charset="utf-8" /><style type="text/css">{cssStyle}</style><body>'
    appHtmlEnd = '</body></html>'

    outputFile = stdout

    def printVersionAndSystem(forcePrint=False):
        global hasPrinted
        if hasPrinted and not forcePrint:
            return

        if useHtml:
            outputFile.write('<pre>')
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

        if useHtml:
            outputFile.write('</pre>')

        if useHtml:
            outputFile.write('<pre>')

        print(
            f'{appName} called with the following parameters: "{argv[1:]}"', file=outputFile
        )

        if useHtml:
            outputFile.write('</pre><pre>')

        if sysString == "":
            if useHtml:
                outputFile.write('<h2>')

            print(
                f"{appName}: Operating system is not detected in script.\nPlease report this at Github @ {
                    appGithub}", file=outputFile
            )

            if useHtml:
                outputFile.write('</h2>')
                outputFile.write(appHtmlEnd + '\n')
                outputFile.close()

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
        if useHtml:
            outputFile.write('<pre>')

        print(f"{appName}: Running in current folder.\n", file=outputFile)
    else:
        options, arguments = getopt(
            argv[1:], "i:o:rdw", ["gogDirectory", "operatingSystem", "makeRemoteCheck", "ignoreDLC", "writePrintToFile"]
        )

        for option, value in options:
            if option == "-w":
                printVersionAndSystem(forcePrint=True)
                useHtml = True
                outputFile = open(f'gt-gvd-output_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.html', "w")
                outputFile.write(appHtmlStart + '\n')

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

                    if useHtml:
                        outputFile.write(appHtmlEnd + '\n')
                        outputFile.close()

                    exit(6)

        if gogDirectory is None:
            printVersionAndSystem()
            if useHtml:
                outputFile.write('<pre>')

            print(
                f'{appName}: No input directory with "-i folder" specified, exiting.', file=outputFile)

            if useHtml:
                outputFile.write('</pre>')
                outputFile.close()

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

                if useHtml:
                    outputFile.write('</pre>')
                    outputFile.close()
                exit(3)
        else:
            printVersionAndSystem()
            print(f'{appName}: "{gogDirectory}" is not existing.', file=outputFile)

            if useHtml:
                outputFile.write('</pre>')
                outputFile.close()

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
        print(f"{appName}: HTML generation disabled.", file=outputFile)

    if makeRemoteCheck or ignoreDLC:
        if useHtml:
            outputFile.write('</pre>')

    if useHtml:
        outputFile.write('<pre>')

    if useHtml:
        print(
            f"\n{appName}: Starting detection.. this might take a moment.", file=outputFile)
    else:
        print(f"\n{appName}: Starting detection.. this might take a moment.\n", file=outputFile)

    if useHtml:
        outputFile.write('</pre><pre>')

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
                        f'{appName}: Error reading out "name" from file: "{
                            inputFile}".\nPlease report this at Github @ {appGithub}', file=outputFile
                    )

                    if useHtml:
                        outputFile.write('</pre>')
                        outputFile.write(appHtmlEnd)
                        outputFile.close()

                    exit(5)

                if "gameId" in jsonKeys:
                    gameId = jsonData["gameId"]
                else:
                    print(
                        f'{appName}: Error reading out "gameId" from file: "{
                            inputFile}".\nPlease report this at Github @ {appGithub}', file=outputFile
                    )

                    if useHtml:
                        outputFile.write('</pre>')
                        outputFile.write(appHtmlEnd)
                        outputFile.close()

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

                    print(f'{appName}: [Status: {gogData.status_code}] : "{
                          gameName}"', file=outputFile)

                    if gogData.status_code == 404:
                        gogErrorCode = gogData.status_code
                        break

                    if gogData.status_code != 200:
                        retries += 1
                        if retries == 4:
                            print(
                                f'{appName}: Error reading game info "{gameName}" from Gog.com.. error code: {
                                    gogData.status_code}\nCheck your internet connection.\nIf the error persists, please report this at Github @ {appGithub}', file=outputFile
                            )
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

    if useHtml:
        outputFile.write('</pre><pre>')

    print(164 * '-', file=outputFile)
    for game in sorted(detectedGames):
        gameId = gamesProcessed[game]
        status = gogStatus[gameId]['text']
        gameLink = gogStatus[gameId]['link']

        gameLinkUrl = ""
        if useHtml:
            gameLinkUrl = f'<a style="display: inline;" href="{gameLink}">{gogStatus[gameId]['name']}</a>'

        if gameLinkUrl != '':
            gogStatus[gameId]["text"] = gogStatus[gameId]["text"].replace(gogStatus[gameId]['name'], gameLinkUrl)

        print(gogStatus[gameId]["text"], file=outputFile)

        if gameId in detectedDLCs:
            for dlc in detectedDLCs[gameId]:
                print(gogStatus[dlc], file=outputFile)

    print(f"\n{appName}: Detected {countGames} game(s) and {
          countDLCs} DLC(s).", file=outputFile)

    if useHtml:
        print(f"{appName}: Finished run. Enjoy your day!", file=outputFile)

    print(f"{appName}: Finished run. Enjoy your day!")

    if useHtml:
        outputFile.write('</pre>' + appHtmlEnd + '\n')

    outputFile.close()
