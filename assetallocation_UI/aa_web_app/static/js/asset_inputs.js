// Items in the table (columns)
// TO AUTOMATE WITH THE DATABASE!!!
var columnDefs = [

    {headerName: "Asset", field: "asset"},
    {headerName: "Signal Ticker", field: "signal_ticker"},
    {headerName: "Future Ticker", field: "future_ticker"},
    {headerName: "Costs", field: "costs"},
    {headerName: "S Leverage", field: "s_leverage"},
];

// Items in the table (rows)
var rowData = [
    {asset: "US Equities", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "EU Equities", signal_ticker: "SX5T Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "JP Equities", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "HK Equities", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "US 10y Bonds", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "UK 10y Bonds", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "Eu 10y Bonds", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "JPY", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "EUR", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "AUD", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "CAD", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1},
    {asset: "GBP", signal_ticker: "SPXT Index", future_ticker: "SP1 R:00_0_R Index", costs: 0.0002, s_leverage: 1}
];

// Options of the table
var gridOptions = {
    defaultColDef: {
        editable: true,
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
        asset: "new line",
        signal_ticker: "new line",
        future_ticker: "line",
        costs: 0,
        s_leverage: 0,
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

// Get the number of rows of the table
function getNumberOfRows() {
    var count = gridOptions.api.getDisplayedRowCount();
    return count;
}

// Get the data from the table ==> TO CALL FROM PYTHON TO GET THE INPUTS
function getDataFromTable(){
    var tmpArr = [];
    var assetsArr = [];
    var rowNum = this.getNumberOfRows();

    for (var i = 0; i < rowNum ; i++){
        var rowNode = gridOptions.api.getDisplayedRowAtIndex(i);
        assetsArr.push(rowNode.data);
    }
    return assetsArr;
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