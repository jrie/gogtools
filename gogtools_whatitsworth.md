# gogtools - whatItsWorth (Userscript)
This is an userscript which can be used with userscript browser addons like Tampermonkey or Greasemonkey or alike.

The script retrieves all orders which have been made on Gog.com order pages.

## Requirements for this tool:
- Greasemonkey / Tampermonkey or alike browser userscript addons

#### Example usages

Copy the contents of the js file ![gogtools_whatitsworth.js](https://github.com/jrie/gogtools/blob/main/gogtools_whatitsworth.js) in a new userscript.
Some userscript extensions might already detect the userscript headers and ask to paste/create a userscript.

In order to then use the addon, login to Gog and navigate to the order page after the script is installed and active:
- https://www.gog.com/account/settings/orders
- For example in German: https://www.gog.com/de/account/settings/orders (other languages should work too.)

In the console of the developer tools of the browser, usually the function key "F12)" - you will see the following message in case everything is setup fine and you are on der order page:
Log info message: `gogtools-whatItsWorth: Ready.` and the usage as follows is displayed to.


The script has currently the following controls:
- `Shift + A`: [A]utomated order page requests - or continue if not finished.
- `Shift + S`: [S]ummary display of gathered data
- `Shift + J`: [J]son data output to process further
- `Shift + C`: [C]lear and reset order informations and statistics.

### Further settings and configuration

There are some settings in the userscript, from line 14 to 24 - which you can alter if you are keen to do so:

```const settings = {
    currencySymbol: '€',                       # Currency to display
    currencyFormat: 'de-DE',                   # Currency format
    minFractionDigits: 2,                      # Minimum digits after zero
    maxFractionDigits: 2,                      # Maximum digits after zero
    currencyStringFormat: '{value} {symbol}',  # {value} is replaced by value, {symbol} by currency symbol
    showItemStats: false,                      # If "true" show stats for each item
    showSummary: true,                         # If "true", shows summary after scraping
    confirmCrawl: false,                       # If "true", confirm each order page crawl
    crawlTimeoutSeconds: 3,                    # Pause in between crawls
    collectData: true                          # Should the json data be populated for further processing, for each order item
  };
```
