var rowData = [
  {currency: 'BRL', implied_ticker: 'BCNI3M Curncy', spot_ticker: 'BRLUSD Curncy', carry_ticker: 'BRLUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'PEN', implied_ticker: 'PSNI3M Curncy', spot_ticker: 'PENUSD Curncy', carry_ticker: 'PENUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'MXN', implied_ticker: 'MXNI3M Curncy', spot_ticker: 'MXNUSD Curncy', carry_ticker: 'MXNUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'COP', implied_ticker: 'CLNI3M Curncy', spot_ticker: 'COPUSD Curncy', carry_ticker: 'COPUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'CLP', implied_ticker: 'CHNI3M Curncy', spot_ticker: 'CLPUSD Curncy', carry_ticker: 'CLPUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'TRY', implied_ticker: 'TRYI3M Curncy', spot_ticker: 'TRYUSD Curncy', carry_ticker: 'TRYUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'RUB', implied_ticker: 'RUBI3M Curncy', spot_ticker: 'RUBUSD Curncy', carry_ticker: 'RUBUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'CZK', implied_ticker: 'CZKI3M Curncy', spot_ticker: 'CZKEUR Curncy', carry_ticker: 'CZKEURCR Curncy', weight_on_usd: 0, eur_usd_base: 'EUR'},
  {currency: 'HUF', implied_ticker: 'HUFI3M Curncy', spot_ticker: 'HUFEUR Curncy', carry_ticker: 'HUFEURCR Curncy', weight_on_usd: 0, eur_usd_base: 'EUR'},
  {currency: 'PLN', implied_ticker: 'PLNI3M Curncy', spot_ticker: 'PLNEUR Curncy', carry_ticker: 'PLNEURCR Curncy', weight_on_usd: 0, eur_usd_base: 'EUR'},
  {currency: 'ZAR', implied_ticker: 'ZARI3M Curncy', spot_ticker: 'ZARUSD Curncy', carry_ticker: 'ZARUSDCR Curncy', weight_on_usd: 50, eur_usd_base: 'USD'},
  {currency: 'CNY', implied_ticker: 'CCNI3M Curncy', spot_ticker: 'CNYUSD Curncy', carry_ticker: 'CNYUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'KRW', implied_ticker: 'KWNI3M Curncy', spot_ticker: 'KRWUSD Curncy', carry_ticker: 'KRWUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'IDR', implied_ticker: 'IHNI3M Curncy', spot_ticker: 'IDRUSD Curncy', carry_ticker: 'IDRUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'INR', implied_ticker: 'IRNI3M Curncy', spot_ticker: 'INRUSD Curncy', carry_ticker: 'INRUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'PHP', implied_ticker: 'PPNI3M Curncy', spot_ticker: 'PHPUSD Curncy', carry_ticker: 'PHPUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'},
  {currency: 'THB', implied_ticker: 'THBI3M Curncy', spot_ticker: 'THBUSD Curncy', carry_ticker: 'THBUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD'}
];

var gridOptions = {
  columnDefs: [
    { headerName: 'Currency', field: 'currency' },
    { headerName: '3M Implied Ticker', field: 'implied_ticker' },
    { headerName: 'Spot Ticker', field: 'spot_ticker' },
    { headerName: 'Carry Ticker', field: 'carry_ticker' },
    { headerName: 'Weight on USD (%)', field: 'weight_on_usd' },
    { headerName: 'EUR/USD base', field: 'eur_usd_base' },
  ],
  defaultColDef: {flex: 1, editable: true},
  rowData: rowData,
  rowSelection: 'multiple',
  animateRows: true,
};

// Create a row to add in the table
function createNewRowData() {
  var newData = {
    currency: 'currency',
    implied_ticker: 'implied ticker ',
    spot_ticker: 'spot ticker',
    carry_ticker: 'carry ticker',
    weight_on_usd: 'weight on usd',
    eur_usd_base: 'eur/usd base',
  };
  return newData;
}

// Clear the data from the table (clear all)
function clearData() {
  gridOptions.api.setRowData([]);
}

// Add a new line in the table => let the user to enter new asset
function onAddRow() {
    var newItem = createNewRowData();
    var res = gridOptions.api.updateRowData({add: [newItem]});
    printResult(res);
}

// Remove a row from the table
function onRemoveSelected() {
  var selectedData = gridOptions.api.getSelectedRows();
  var res = gridOptions.api.applyTransaction({ remove: selectedData });
  printResult(res);
}



// wait for the document to be loaded, otherwise
// ag-Grid will not find the div in the document.
document.addEventListener('DOMContentLoaded', function () {
  var eGridDiv = document.querySelector('#myGrid');
  new agGrid.Grid(eGridDiv, gridOptions);
});