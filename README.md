# gogtools
A collection of tools to work on and with Gog.com

## Tools of trade

### gogtools - version detector and retriever
A *windows*, *linux*, and *osx* Python script which attempts to identify and list the versions of installed Gog games and DLCs.

![image](https://github.com/jrie/gogtools/assets/5701785/0a18b287-5b09-464c-a3eb-01e3f96c3ac2)


In addition, the version number can be directly retrieved from Gog and updated version, if any, are displayed.
Lastly, it is possible to check for installers and versions for a particular operating system - if a game or DLC is not available, this is shown too.
By default, with no option set, the current operating system detected is used for querying for versions.

#### Requirements for this tool:
- A Python3 version of 3.xx or later
- "requests" package, either installed using "pip" or as linux package, something like `python3-requests` on Debian.


#### Example usages

Windows
- `python '.\gogtools-version detector.py'` (no `-i` provided, uses the current folder of the script as root to scan for contents)
- `python '.\gogtools-version detector.py' -i "c:\GOG Games"` (analyze folder starting from "c:\GOG Games")
- `python '.\gogtools-version detector.py' -r -i "c:\GOG Games"` (`-r` check Gog for current versions)
- `python '.\gogtools-version detector.py' -r -i "c:\GOG Games" -o osx` (`-o`, check if `osx`, meaning OSX, installers are available)

Linux (perhaps also OSX)
- `python ./gogtools-version detector.py' -i /home/user/gogGames -r`


Option/Switches:
- `-i value`: The input folder where all games and DLCs are installed/located to start analyze from, if not specified, uses the directory where the script is located.
- `-r`: No value, request the online Gog API for the current versions
- `-o value`: Use with `-r` to check for game/dlcs installers for the operating systems, possible values are `windows`, `linux`, and `osx`.



