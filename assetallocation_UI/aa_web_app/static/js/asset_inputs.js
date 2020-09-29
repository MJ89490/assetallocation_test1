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

function onBtForEachNode() {
  console.log('### api.forEachNode() ###');
  gridOptions.api.forEachNode(this.printNode)
}

function printNode(node, index) {
    console.log(index + ' -> data: ' + node.data.asset + ', ' + node.data.signal_ticker);
}


// Get the data from the table ==> TO CALL FROM PYTHON TO GET THE INPUTS
function getDataFromTable(){

    var assetsNames = []
    var assetsTicker = [];
    var assetsFutureTicker = [];
    var assetsCosts = [];
    var assetsLeverage = [];

    gridOptions.api.forEachNode(function(rowNode, index) {
        assetsNames.push(rowNode.data.asset);
        assetsTicker.push(rowNode.data.signal_ticker);
        assetsFutureTicker.push(rowNode.data.future_ticker);
        assetsCosts.push(rowNode.data.costs);
        assetsLeverage.push(rowNode.data.s_leverage);
    });

    return {assetsNames: assetsNames, assetsTicker: assetsTicker, assetsFutureTicker: assetsFutureTicker,
            assetsCosts: assetsCosts, assetsLeverage: assetsLeverage};
}


$(function (){
	$('#contact-form-button').click(function(){
		var fund = $('#inputFundname').val();
		var date = $('#inputdatefrom').val();
		var lag = $('#inputtimelag').val()
		var weight = $('#inputstrategyweight').val()
		var leverage = $('#inputleverage').val();
		var volwindow = $('#inputvolwindow').val();

		var frequency = $('#inputfrequency').val();
		var weekday = $('#inputweekday').val();

		var signaloneshort = $('#inputsignaloneshort').val();
		var signalonelong = $('#inputsignalonelong').val();

        var signaltwoshort = $('#inputsignaltwoshort').val();
		var signaltwolong = $('#inputsignaltwolong').val();

		var signalthreeshort = $('#inputsignalthreeshort').val();
		var signalthreelong = $('#inputsignalthreelong').val();

		var res =  sendJsonDataFromTable(fund, date, weight, lag, leverage, volwindow, frequency, weekday,
		           signaloneshort, signalonelong, signaltwoshort, signaltwolong, signalthreeshort, signalthreelong);
	});
});


// create a new fct which calls getDataFromTable
// send the return value (assetsArr) in json as a post request to python to the route times
function sendJsonDataFromTable(fund, date, weight, lag, leverage, volwindow, frequency, weekday, signaloneshort,
                               signalonelong, signaltwoshort, signaltwolong, signalthreeshort, signalthreelong){

    var results = this.getDataFromTable();

    var jsonData = JSON.stringify({"assetsNames": results.assetsNames, "assetsTicker": results.assetsTicker,
                                   "assetsFutureTicker": results.assetsFutureTicker, "assetsCosts": results.assetsCosts,
                                   "assetsLeverage": results.assetsLeverage, "fund": fund, "date": date,
                                   "weight": weight, "lag": lag, "leverage": leverage, "volwindow": volwindow,
                                   "frequency": frequency, "weekday": weekday, "signaloneshort": signaloneshort,
                                   "signalonelong": signalonelong, "signaltwoshort": signaltwoshort,
                                   "signaltwolong":signaltwolong,"signalthreeshort": signalthreeshort,
                                   "signalthreelong": signalthreelong });
    console.log(jsonData);
    $.ajax({
      type : 'POST',
      url : "http://127.0.0.1:5000/received_data_run_model",
      data : jsonData,
      contentType : 'application/json',
      dataType: 'json'
    });

    return jsonData

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


//Failed attempt at adding Asset input data to request from submit button
//
// $("#btn btn-lg btn-primary").click(function() {
//     console.log('hit form submit button');
//     var results = this.getDataFromTable();
//
//     var jsonData = JSON.stringify({"assetsNames": results.assetsNames, "assetsTicker": results.assetsTicker,
//                                    "assetsFutureTicker": results.assetsFutureTicker, "assetsCosts": results.assetsCosts,
//                                    "assetsLeverage": results.assetsLeverage});
//
//      $(this).append(jsonData);
//      return true;
// });
//
// $("form-group").submit(function () {
//     console.log('hit form submit button');
//     var results = this.getDataFromTable();
//
//     var jsonData = JSON.stringify({"assetsNames": results.assetsNames, "assetsTicker": results.assetsTicker,
//                                    "assetsFutureTicker": results.assetsFutureTicker, "assetsCosts": results.assetsCosts,
//                                    "assetsLeverage": results.assetsLeverage});
//
//      $(this).append(jsonData);
//      return true;
// });