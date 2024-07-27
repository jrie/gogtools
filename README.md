# gogtools
A collection of tools to work on and with Gog.com

## Tools of trade

### gogtools - version detector and retriever
A *windows*, *linux*, and *osx* Python script which attempts to identify and list the versions of installed Gog games and DLC, as well as an option to compare versions online at Gog.

#### Screenshot in Windows Powershell:
![version_detector_windows](https://github.com/jrie/gogtools/assets/5701785/0a18b287-5b09-464c-a3eb-01e3f96c3ac2)

#### Screenshot in Linux:
![version_detector_linux](https://github.com/user-attachments/assets/d79b928d-2f4a-4830-ad17-05f2c1a7ce75)


More information can be found [here](version-detector-retriever.md).

### gogtools - whatitsworth
A userscript for Greasemonkey, Tampermonkey and other userscript addons.

This script can read out the order page details inside the browser if the order history page is opened and you are logged in to Gog. It collects the details of each order item in a json store variable like id and price paid and discounted price and percent.

In addition a summary of total paid, average paid, average discount, and other stats are shown inside the developer console of the browser.
