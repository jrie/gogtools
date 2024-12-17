# gogtools
A collection of tools to work on and with Gog.com

## Tools of trade

The Python scripts:
- gogtools - game-id-retriever
- gogtools - version-detector-and-retriever

.. work on *windows*, *linux*, and *osx* and require only Python3 and `python-requests` no other magic involved.


The Javascript:
- whatitsworth.js

.. works on every browser as a Greasemonkey, ViolentMonkey, or Tampermonkey userscript.

## Overview of the tools

### gogtools - game-id-retriever
A python script which has a console interface to search Gog.com for *games*, *dlc* and *packs*. This tools was made in reason that some of the version file, used by *gogtools-version detector.py* do not always provide a *game id* which is used to distinguish games and other contents of Gog.com


The script provides a search interface and allows to store game information in a file, currently `gt-gid.json` - as of time of writing, the *version detector.py* is able to use this file to supplement game information for online retrieval of the version.

#### Screenshot of usage:
![gogtools-game-id-retriever_v0 0 1](https://github.com/user-attachments/assets/9f64255e-f64b-4fde-9ab6-23b0ab859c8d)

### gogtools - version detector and retriever
A *windows*, *linux*, and *osx* Python script which attempts to identify and list the versions of installed Gog games and DLC, as well as an option to compare versions online at Gog.com

Also now supports HTML output using "-w" parameter. And display of optional URLS for console and HTML output.

More information can be found [in the readme of gogtools - version-detector-and-retriever](version-detector-retriever.md).

#### Screenshot in Windows Powershell:
![version_detector_windows](https://github.com/jrie/gogtools/assets/5701785/0a18b287-5b09-464c-a3eb-01e3f96c3ac2)

#### Screenshot in Linux:
![version_detector_linux](https://github.com/user-attachments/assets/d79b928d-2f4a-4830-ad17-05f2c1a7ce75)

#### Screenshot HTML output with links
![gogtools-version detector v0 0 5 0-html](https://github.com/user-attachments/assets/3d41b79b-3c4c-47d6-b574-d7bf8db0c56b)


### gogtools - whatitsworth
A userscript for Greasemonkey, Tampermonkey and other userscript addons.

This script can read out the order page details inside the browser if the order history page is opened and you are logged in to Gog. It collects the details of each order item in a json store variable like id and price paid and discounted price and percent.

In addition a summary of total paid, average paid, average discount, and other stats are shown inside the developer console of the browser.

More information can be found [here](gogtools_whatitsworth.md).
