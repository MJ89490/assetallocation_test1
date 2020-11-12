var rowData = [
  {asset: 'US Equities', signal_ticker: 'SPXT Index',future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'EU Equities', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'JP Equities', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'HK Equities', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'US 10y Bonds', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'UK 10y Bonds', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'Eu 10y Bonds', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'JPY', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'EUR', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'AUD', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'CAD', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1},
  {asset: 'GBP', signal_ticker: 'SPXT Index', future_ticker: 'SP1 R:00_0_R Index', costs:  0.0002, s_leverage: 1}
];

var gridOptions = {
  columnDefs: [
    { headerName: 'Asset', field: 'asset' },
    { headerName: 'Signal Ticker', field: 'signal_ticker' },
    { headerName: 'Future Ticker', field: 'future_ticker' },
    { headerName: 'Costs', field: 'costs' },
    { headerName: 'Leverage', field: 's_leverage' }
  ],
  defaultColDef: {flex: 1, editable: true},
  rowData: rowData,
  rowSelection: 'multiple',
  animateRows: true,
};

// Create a row to add in the table
function createNewRowData() {
  var newData = {
    asset: 'asset',
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
    var input_signal_ticker = [];
    var input_future_ticker = [];
    var input_costs = [];
    var input_leverage = [];

    gridOptions.api.forEachNode(function(rowNode, index) {
        input_asset.push(rowNode.data.asset);
        input_signal_ticker.push(rowNode.data.signal_ticker);
        input_future_ticker.push(rowNode.data.future_ticker);
        input_costs.push(rowNode.data.costs);
        input_leverage.push(rowNode.data.s_leverage);
    });

    var json_data = JSON.stringify({"input_asset": input_asset,
                                    "input_signal_ticker": input_signal_ticker,
                                    "input_future_ticker": input_future_ticker,
                                    "input_costs": input_costs,
                                    "input_leverage": input_leverage});
    return json_data
}

$(function(){
	$('#contact-form-button-times').click(function(){

	    var json_data = getDataFromTable();
        var form_data = $('form').serialize();

		$.ajax({
			url: '/received_data_times_form',
			data: {form_data: form_data, json_data: json_data},
			type: 'POST',
			success: function(response){
				console.log(response);
				alert('The strategy has been run successfully!');
				window.location.href = "https://elle.com/uk/";
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});


// wait for the document to be loaded, otherwise
// ag-Grid will not find the div in the document.
document.addEventListener('DOMContentLoaded', function () {
  var eGridDiv = document.querySelector('#myGrid');
  new agGrid.Grid(eGridDiv, gridOptions);
});