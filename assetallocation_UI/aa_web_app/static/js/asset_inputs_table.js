// Items in the table (columns)
var columnDefs = [
    {headerName: "Asset", field: "asset"},
    {headerName: "Signal Ticker", field: "signal_ticker"},
    {headerName: "Future Ticker", field: "future_ticker"},
    {headerName: "Costs", field: "costs"},
    {headerName: "S Leverage", field: "s_leverage"},
];

// Items in the table (rows)
var rowData = [
    {asset: "US Equities", signal_ticker: "F25915Y Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "EU Equities", signal_ticker: "F91001Y Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "JP Equities", signal_ticker: "LP01TREU Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "HK Equities", signal_ticker: "I05204Y Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "US 10y Bonds", signal_ticker: "F91003Y Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "UK 10y Bonds", signal_ticker: "F10120Y Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "EU 10y Bonds", signal_ticker: "F25904Y Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "JPY", signal_ticker: "NK1 A:00_0_R Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "EUR", signal_ticker: "I05110Y Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "AUD", signal_ticker: "F25606Y Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "CAD", signal_ticker: "SP1 A:00_0_R Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1},
    {asset: "GBP", signal_ticker: "I05110Y Index", future_ticker: "SPXT Index", costs: 0.0002, s_leverage: 1}
];

// Options of the table
var gridOptions = {
    defaultColDef: {
        editable: true, //the user has the possibility to change the value in the table
        sortable: true,
        filter: true
    },
    animateRows: true,
    columnDefs: columnDefs,
    rowData: rowData,
    rowSelection: 'multiple'
};


// Create a row to add in the table
function createNewRowData() {
    var newData = {
        asset: "US Equities (to automate)",
        signal_ticker: "SPXT Index",
        future_ticker: "SP1 R:00_0_R Index",
        costs: 0.0002,
        s_leverage: 1,
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
    var res = gridOptions.api.updateRowData({remove: selectedData});
    printResult(res);
}

//Print the rows in the console of the Browser (checking errors)
function printResult(res) {
    console.log('---------------------------------------')
    if (res.add) {
        res.add.forEach( function(rowNode) {
            console.log('Added Row Node', rowNode);
        });
    }
    if (res.remove) {
        res.remove.forEach( function(rowNode) {
            console.log('Removed Row Node', rowNode);
        });
    }
    if (res.update) {
        res.update.forEach( function(rowNode) {
            console.log('Updated Row Node', rowNode);
        });
    }
}

// wait for the document to be loaded, otherwise
// ag-Grid will not find the div in the document.
document.addEventListener("DOMContentLoaded", function() {
    var eGridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(eGridDiv, gridOptions);
});