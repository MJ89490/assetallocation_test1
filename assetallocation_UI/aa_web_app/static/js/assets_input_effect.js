var rowData = [
  {currency: 'BRL', implied_ticker: 'Celica', spot_ticker: 35000, carry_ticker: 'Elly', weight_on_usd: 'Smooth', eur_usd_base: 'Jeans'},
  {currency: 'PEN', implied_ticker: 'Mondeo', spot_ticker: 32000, carry_ticker: 'Shane', weight_on_usd: 'Filthy', eur_usd_base: 'Shorts'},
  {currency: 'MXN', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'COP', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'CLP', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'TRY', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'RUB', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'CZK', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'HUF', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'PLN', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'ZAR', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'CNY', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'KRW', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'IDR', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'INR', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'PHP', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'},
  {currency: 'THB', implied_ticker: 'Boxter', spot_ticker: 72000, carry_ticker: 'Jack', weight_on_usd: 'Dirty', eur_usd_base: 'Padded'}
];

var gridOptions = {
  columnDefs: [
    { headerName: 'Currency', field: 'currency' },
    { headerName: '3M Implied Ticker', field: 'implied_ticker' },
    { headerName: 'Spot Ticker', field: 'spot_ticker' },
    { headerName: 'Carry Ticker', field: 'carry_ticker' },
    { headerName: 'Weight on USD', field: 'weight_on_usd' },
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

function getRowData() {
  var rowData = [];
  gridOptions.api.forEachNode(function (node) {
    rowData.push(node.data);
  });
  console.log('Row Data:');
  console.log(rowData);
}

// Clear the data from the table (clear all)
function clearData() {
  gridOptions.api.setRowData([]);
}

function addItems(addIndex) {
  var newItems = [createNewRowData(), createNewRowData(), createNewRowData()];
  var res = gridOptions.api.applyTransaction({
    add: newItems,
    addIndex: addIndex,
  });
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