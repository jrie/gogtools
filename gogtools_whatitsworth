// ==UserScript==
// @name         gogtools-whatItsWorth
// @namespace    https://github.com/jrie/gogtools
// @version      v0.0.1
// @description  What its worth? - Compare orders and see what has been payed on Gog.com
// @author       Jan Riechers
// @match        https://www.gog.com/account/settings/orders
// @match        https://www.gog.com/*/account/settings/orders
// @icon         https://www.google.com/s2/favicons?sz=64&domain=gog.com
// @grant        none
// ==/UserScript==

(function () {
  const settings = {
    currencySymbol: '€',
    currencyFormat: 'de-DE',
    minFractionDigits: 2,
    maxFractionDigits: 2,
    currencyStringFormat: '{value} {symbol}',
    showItemStats: false,
    showSummary: true,
    confirmCrawl: false,
    crawlTimeoutSeconds: 3,
    collectData: true
  };

  // Housekeeping
  let orderStats = {
    totalPaid: 0.0,
    totalDiscount: 0.0,
    totalSaved: 0.0,
    totalPrice: 0.0,
    totalItems: 0,
    orderPages: 0,
    totalPages: 0,
    freeItems: 0,
    giftedItems: 0,
    unclaimedItems: 0
  };

  let orderDataJson = {};

  const request = new window.XMLHttpRequest();
  request.addEventListener('readystatechange', evaluateOrderPageRequest);

  // Functions
  function createCurrencyString (value) {
    let format = settings.currencyStringFormat;
    format = format.replace('{value}', value);
    format = format.replace('{symbol}', settings.currencySymbol);
    return format;
  }

  function formatAmount (amount) {
    return (amount).toLocaleString(settings.currencyFormat, { minimumFractionDigits: settings.minFractionDigits, maximumFractionDigits: settings.maxFractionDigits });
  }

  function calculateSavedAmount (beforeDiscount, paid) {
    return beforeDiscount !== 0 && paid !== 0 ? beforeDiscount - paid : 0;
  }

  function calculateAverage (value, items) {
    return items !== 0 ? value / items : 0;
  }

  function calculateDiscount (beforeDiscount, paid, fromHundreds) {
    const discountPercent = beforeDiscount !== 0 && paid !== 0 ? paid / beforeDiscount : 0;
    if (discountPercent !== 0) {
      return fromHundreds ? getPercentFromHundred(discountPercent) : discountPercent;
    }

    return 0;
  }

  function getPercentFromHundred (percent) {
    return (1 - percent) * 100;
  }

  // Stats function
  function printOrderStats () {
    // Money money..
    const totalPrice = createCurrencyString(formatAmount(orderStats.totalPrice));
    const totalPaid = createCurrencyString(formatAmount(orderStats.totalPaid));
    const totalSaved = createCurrencyString(formatAmount(orderStats.totalSaved));

    // Items (Orders)
    const totalItems = orderStats.totalItems;
    const freeItems = orderStats.freeItems;

    // Averages
    const averagePrice = createCurrencyString(formatAmount(calculateAverage(orderStats.totalPaid, totalItems)));
    const averageDiscount = formatAmount(calculateDiscount(orderStats.totalPrice, orderStats.totalPaid, true));
    const averageSaved = formatAmount(calculateDiscount(orderStats.totalSaved, totalItems, true));

    // Output
    console.log('--- ORDER SUMMARY ---');
    console.log('You ordered ' + totalItems + ' item(s) and ' + freeItems + ' item(s) were free.');
    console.log('With a value of ' + totalPrice);
    console.log('You paid and saved ' + totalPaid + ' (' + totalSaved + ')');
    console.log('\n\n');
    console.log('--- AVERAGES ---');
    console.log('Average price: ' + averagePrice);
    console.log('Average discount: ' + averageDiscount + '%');
    console.log('Average saved: ' + averageSaved + '%');
    console.log('\n');
  }

  function evaluateOrderPageRequest (evt) {
    if (evt.target.readyState === 4) {
      if (evt.target.status === 200) {
        const pageOrderData = JSON.parse(evt.target.responseText);
        const orders = pageOrderData.orders;
        orderStats.totalPages = pageOrderData.totalPages;

        for (const order of orders) {
          for (const product of order.products) {
            const productTitle = product.title;
            const productId = product.id;
            const priceSymbol = product.price.symbol;
            const basePrice = parseFloat(product.price.baseAmount);
            const paidPrice = parseFloat(product.price.amount);

            const baseWithCurrency = createCurrencyString(formatAmount(basePrice));
            const paidWithCurrency = createCurrencyString(formatAmount(paidPrice));

            orderDataJson[productTitle] = [productId, priceSymbol, basePrice, paidPrice];

            if (settings.showItemStats) {
              if (paidPrice !== 0 && basePrice !== 0 && paidPrice !== basePrice) {
                console.log(productTitle + ' : ' + baseWithCurrency + ' / ' + paidWithCurrency + ' [ ' + Math.floor(calculateDiscount(basePrice, paidPrice, true)) + '% ]');
              } else if (paidPrice !== 0) {
                console.log(productTitle + ' : ' + baseWithCurrency + ' [ 0% ]');
              } else {
                console.log(productTitle + ' : FREE');
              }
            }

            // Stats
            if (basePrice !== paidPrice) {
              orderStats.totalPrice += basePrice;
            }

            if (paidPrice !== 0) {
              orderStats.totalPaid += paidPrice;

              if (basePrice !== paidPrice) {
                orderStats.totalSaved += calculateSavedAmount(basePrice, paidPrice);
              }
            } else {
              ++orderStats.freeItems;
            }

            ++orderStats.totalItems;
          }
        }

        ++orderStats.orderPages;

        if (orderStats.orderPages <= orderStats.totalPages) {
          if (settings.confirmCrawl) {
            if (window.confirm('gogtools-whatItsWorth: Process next order page? Currently ' + orderStats.orderPages + ' of ' + orderStats.totalPages + 'pages.\n\nYou can resume at any time by pressing "Shift + A"')) {
              generateRequest();
            }
          } else {
            console.log('gogtools-whatItsWorth: Process order page ' + orderStats.orderPages + ' of ' + orderStats.totalPages);
            window.setTimeout(generateRequest, settings.crawlTimeoutSeconds * 1000);
          }
        } else {
          if (settings.showSummary) {
            printOrderStats();
            window.alert('gogtools-whatItsWorth: Everything done.');
          }
        }
      } else {
        window.alert('gogtools-whatItsWorth: Encountered an error while retrieving the order data.\nStatus code: ' + evt.target.status.toString());
      }
    }
  }

  function generateRequest () {
    request.open('GET', 'https://www.gog.com/account/settings/orders/data?canceled=0&completed=1&in_progress=0&not_redeemed=0&page=' + orderStats.orderPages.toString() + '&pending=0&redeemed=1');
    request.send();
  }

  function handleKeyUp (evt) {
    if (evt.target.nodeName === 'BODY' && evt.shiftKey === true) {
      if (evt.code === 'KeyA') {
        if (orderStats.orderPages !== 0 && orderStats.orderPages < orderStats.totalPages) {
          if (window.confirm('gogtools-whatItsWorth: Read all order pages automated?')) {
            if (orderStats.orderPages !== 0) {
              if (window.confirm('gogtools-whatItsWorth: Continue from order page ' + orderStats.orderPages.toString() + '..')) {
                generateRequest();
              } else {
                return;
              }
            }

            generateRequest();
            return;
          }
        } else if (orderStats.totalPages === 0 && window.confirm('gogtools-whatItsWorth: Read all order pages automated?')) {
          generateRequest();
          return;
        }

        window.alert('gogtools-whatItsWorth: All pages already crawled.\n\nYou can reset by pressing "Shift + C" and confirm.');
      } else if (evt.code === 'KeyJ') {
        console.log(orderDataJson);
      } else if (evt.code === 'KeyS') {
        if (orderStats.orderPages === 0) {
          console.log('gogtools-whatItsWorth: No order pages evaluated.');
          return;
        }

        console.log('gogtools-whatItsWorth: summary for order of ' + orderStats.orderPages + ' page(s)');
        printOrderStats();
      } else if (evt.code === 'KeyC') {
        if (window.confirm('gogtools-whatItsWorth: Reset order statistics and data?')) {
          orderStats = {
            totalPaid: 0.0,
            totalDiscount: 0.0,
            totalSaved: 0.0,
            totalPrice: 0.0,
            totalItems: 0,
            totalPages: 0,
            orderPages: 0,
            freeItems: 0,
            giftedItems: 0,
            unclaimedItems: 0
          };

          orderDataJson = {};

          console.log('gogtools-whatItsWorth: Order data resetted.');
        }
      }
    }
  }

  document.addEventListener('keyup', handleKeyUp);

  console.log('gogtools-whatItsWorth: Ready.');
  console.log('gogtools-whatItsWorth:\nUsage:\n[Shift] key +\n[A]utomated order page requests\n[S]ummary display of gathered data\n[J]son data output to process further.\n[C]lear and reset order informations and statistics.');
})();
