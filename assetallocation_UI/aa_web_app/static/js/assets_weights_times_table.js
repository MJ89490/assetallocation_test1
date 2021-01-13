var colDefs = [];
var rowsDefs = [];

function createRowsTable(col, rowsValues){
    var rows = {};
//    var rowsValues = ['US Equities', 'Equities', 'SPXT Index']

//    for (var i = 0; i < rowsValues.length; i++) {
//        rows[col[i]] = rowsValues[i];
//    }
//    console.log(rows);
//
//    rowDefs.push(rows);
//
//    console.log(rowDefs);

//    var rowsValues = [[1, 2, 10], [4, 5, 40], [7, 8, 45]];
//    var rowsDefs = [];

    l = 0;
    if (rowsValues[0].length != col.length){l = 1};

    for (var val = 0; val < rowsValues.length - l; val++){
      rows = {};
      let counter = 0;

      for (var name = 0; name < col.length; name++){
        rows[col[name]] = rowsValues[counter][val];
        counter++;

      }
      rowsDefs.push(rows);
    }

    console.log(rowsDefs);

}


function createColumnsTable(val){
    for (var i = 0; i < val.length; i++) {
      var dict = {headerName: val[i], field: val[i]};
      colDefs.push(dict);
    }
}

var columnDefs = colDefs;
var rowData = rowsDefs;

var gridOptions = {
  columnDefs: columnDefs ,
  defaultColDef: {flex: 1, editable: true},
  rowData: rowData,
  rowSelection: 'multiple',
  animateRows: true,
};

// Create a row to add in the table
function createNewRowData() {
  var newData = {
    asset: 'asset',
    category: 'category',
    signal_ticker: 'signal ticker ',
    future_ticker: 'future ticker',
    costs: 'costs',
    leverage: 'leverage'
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

// Get the data from AG grid table
function getDataFromTable(){

    var input_asset = [];
    var input_category = [];
    var input_signal_ticker = [];
    var input_future_ticker = [];
    var input_costs = [];
    var input_leverage = [];

    gridOptions.api.forEachNode(function(rowNode, index) {
        input_asset.push(rowNode.data.asset);
        input_category.push(rowNode.data.category);
        input_signal_ticker.push(rowNode.data.signal_ticker);
        input_future_ticker.push(rowNode.data.future_ticker);
        input_costs.push(rowNode.data.costs);
        input_leverage.push(rowNode.data.s_leverage);
    });

    var json_data = JSON.stringify({"input_asset": input_asset,
                                    "input_category": input_category,
                                    "input_signal_ticker": input_signal_ticker,
                                    "input_future_ticker": input_future_ticker,
                                    "input_costs": input_costs,
                                    "input_leverage": input_leverage});
    return json_data;
}

// Checking if the values of the signals are in the ascending order, otherwise the signals are wrong
function checkArray(array) {
    var aa = array.slice(1);
    if (aa.every((a, i) => array[i] <= a)) {
        // No error
        return false;
    }
    return true;

}

// Checking the values of the form before running the model
function checkReceivedDataTimes(){
    var lag = parseInt(document.getElementById('input_time_lag_times').value);
    var vol = parseInt(document.getElementById('input_vol_window_times').value);

    var signalOneShort = parseInt(document.getElementById('input_signal_one_short_times').value);
    var signalOneLong = parseInt(document.getElementById('input_signal_one_long_times').value);
    var signalTwoShort = parseInt(document.getElementById('input_signal_two_short_times').value);
    var signalTwoLong = parseInt(document.getElementById('input_signal_two_long_times').value);
    var signalThreeShort = parseInt(document.getElementById('input_signal_three_short_times').value);
    var signalThreeLong = parseInt(document.getElementById('input_signal_three_long_times').value);

    var signals = [signalOneShort, signalOneLong, signalTwoShort, signalTwoLong, signalThreeShort, signalThreeLong]

    flagError = checkArray(signals);

    if (flagError == true){
        alert('Error: signals are wrong\nThe signals must be as follow\nsig1 short < sig1 long < sig2 short < sig2 long < sig3 short < sig3 long');
        return 'error'
    }

    if (lag < 1){
        alert('Error: time lag is lower than 1');
        return 'error';
    }
    else if (vol < 10){
        alert('Error: volatility is lower than 10');
         return 'error';
    }
    return 'okay';

}

$(function(){
	$('#contact-form-button-times').click(function(){

	    var json_data = getDataFromTable();
        var form_data = $('form').serialize();

        var check = checkReceivedDataTimes();
        console.log(check);

        if (check != 'error'){
            $.ajax({
                url: "received_data_times_form",
                data: {form_data: form_data, json_data: json_data},
                type: 'POST',
                success: function(response){
                    console.log(response);
                    alert('The strategy has been run successfully!');
                    window.location.href = "times_dashboard";
                },
                error: function(error){
                    console.log(error);
                }
            });

		}
	});
});


// wait for the document to be loaded, otherwise
// ag-Grid will not find the div in the document.
document.addEventListener('DOMContentLoaded', function () {
  var eGridDiv = document.querySelector('#myGrid');



  new agGrid.Grid(eGridDiv, gridOptions);
});