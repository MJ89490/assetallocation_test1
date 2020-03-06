var columnDefs = [
    {headerName: "Asset", field: "asset"},
    {headerName: "Signal Ticker", field: "signal_ticker"},
    {headerName: "Future Ticker", field: "future_ticker"},
    {headerName: "Costs", field: "costs"},
    {headerName: "S Leverage", field: "s_leverage"}
];

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

var gridOptions = {animateRows: true, columnDefs: columnDefs, rowData:rowData, rowSelection: 'multiple'};

var newCount = 1;

function createNewRowData(){
    var newData = {
        asset: "",
        signal_ticker: "",
        future_ticker: "",
        costs:"",
        s_leverage:""
    };
    newCount++;
    return newData;
}

function clearData() {
    gridOptions.api.setRowData([]);
}

function onAddRow(){
    var newItem = createNewRowData();
    var res = gridOptions.updateRowData({add: [newItem]});
    printResult(res);
}

function addItems() {
    var newItems = [createNewRowData(), createNewRowData(), createNewRowData()];
    var res = gridOptions.api.updateRowData({add: newItems});
    printResult(res);
}

function onRemoveSelected() {
    var selectedData = gridOptions.api.getSelectedRows();
    var res = gridOptions.api.updateRowData({remove: selectedData});
    printResult(res);
}

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