
var rowData = [
  {asset: 'DM FX', category: 'FX', signal_ticker: 'SPXT Index',future_ticker: 'CD1 A:00_0_R Curncy', costs:  0.0002, s_leverage: 1},
  {asset: 'DM Equity', category: 'Equities', signal_ticker: 'TPXDDVD Index', future_ticker: 'SPXT Index', costs:  0.0002, s_leverage: 1},
  {asset: 'Nominal Bond', category: 'Fixed Income', signal_ticker: 'G 1 A:00_0_R Comdty', future_ticker: 'CN1 A:00_0_R Comdty', costs:  0.0002, s_leverage: 1},

//  {asset: 'EU Equities', category: 'Equities', signal_ticker: 'SX5T Index', future_ticker: 'AD1 A:00_0_R Curncy', costs:  0.0002, s_leverage: 1},
//
//  {asset: 'HK Equities', category: 'Equities', signal_ticker: 'HSI 1 A:00_0_R Index', future_ticker: 'B1 A:00_0_R Curncy', costs:  0.0002, s_leverage: 1},
//  {asset: 'US 10y Bonds', category: 'Bonds', signal_ticker: 'MLT1US10 Index', future_ticker: 'SPXT Index', costs:  0.0002, s_leverage: 1},
//
//  {asset: 'EU 10y Bonds', category: 'Bonds', signal_ticker: 'SRX1 A:00_0_R Comdty', future_ticker: 'SPXT Index', costs:  0.0002, s_leverage: 1},
//  {asset: 'JPY', category: 'FX', signal_ticker: 'JPYUSD Curncy', future_ticker: 'SPXT Index', costs:  0.0002, s_leverage: 1},
//  {asset: 'EUR', category: 'FX', signal_ticker: 'EURUSD Curncy', future_ticker: 'SPXT Index', costs:  0.0002, s_leverage: 1},
//  {asset: 'AUD', category: 'FX', signal_ticker: 'AUDUSD Curncy', future_ticker: 'AUDUSD Curncy', costs:  0.0002, s_leverage: 1},
//  {asset: 'CAD', category: 'FX', signal_ticker: 'CADUSD Curncy', future_ticker: 'SPXT Index', costs:  0.0002, s_leverage: 1},
//  {asset: 'GBP', category: 'FX', signal_ticker: 'EURGBP Curncy', future_ticker: 'SPXT Index', costs:  0.0002, s_leverage: 1}
];

var gridOptions = {
  columnDefs: [
    { headerName: 'Asset', field: 'asset' },
    { headerName: 'Category', field: 'category' },
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

// Get the data from assets table
//function getDataFromTable(){
////    var asset = $("#input_asset_from_times").val();
////    var category = $("#input_category_from_times").val();
////    var signalTicker = $("#input_signal_ticker_from_times").val();
////    var futureTicker = $("#input_future_ticker_from_times").val();
////    var costs = parseFloat($("#input_costs_from_times").val());
////    var leverage = parseFloat($("#input_leverage_from_times").val());
////    var versionName = $("#input_version_name_strategy").val();
////
////    var json_data = JSON.stringify({"input_asset": asset,
////                                    "input_category": category,
////                                    "input_signal_ticker": signalTicker,
////                                    "input_future_ticker": futureTicker,
////                                    "input_costs": costs,
////                                    "input_leverage": leverage,
////                                    "input_version_name_strategy": versionName});
//
//
//
//
//
//
//
//
//
//
//
//
//
////    return json_data;
//}





$(function()
{
   $("#contact-form-button-times").click(function()
   {
      $("#faqs").find('tr').each(function(){

         var asset_title = $(this).find("th:eq(0)").val();


         var asset = $(this).find("td:eq(0) input[type='text']").val();
         var category = $(this).find("td:eq(1) input[type='text']").val();
         var signalTicker = $(this).find("td:eq(2) input[type='text']").val();
         var futureTicker = $(this).find("td:eq(3) input[type='text']").val();
         var costs = $(this).find("td:eq(4) input[type='text']").val();
         var leverage = $(this).find("td:eq(5) input[type='text']").val();

        console.log(asset_title);
         console.log(asset);
         console.log(category);
        console.log(signalTicker);
        console.log(futureTicker);
        console.log(costs);
        console.log(leverage);
   });
 });
});
















// Checking if the values of the signals are in the ascending order, otherwise the signals are wrong
function checkArray(array) {
    var aa = array.slice(1);
    if (aa.every((a, i) => array[i] <= a)) {
        // No error
        return false;
    }
    return true;

}

// Checking the values of the form before running the model CHANGE TO JQUERY
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

function selectDateToCalendar() {
    var date_to = document.getElementById("input_date_to_new_version_times").value;

    var gsDayNames = ['Sunday',
                      'Monday',
                      'Tuesday',
                      'Wednesday',
                      'Thursday',
                      'Friday',
                      'Saturday'
                    ];

    var fields = date_to.split('/');

    var day = fields[0];
    var month = fields[1];
    var year = fields[2];

    date_from_new = year + "/" + month + "/" + day

    var d = new Date(date_from_new);
    var dayName = gsDayNames[d.getDay()];

    document.getElementById("input_weekday_times").value = dayName.substring(0,3).toUpperCase();
}



//$(function(){
//	$('#contact-form-button-times').click(function(){
//
//	    var json_data = getDataFromTable();
//        var form_data = $('form').serialize();
//        var check = checkReceivedDataTimes();
//
//        if (check != 'error'){
//            $.ajax({
//                url: "received_data_times_form",
//                data: {form_data: form_data, json_data:json_data},
//                type: 'POST',
//                success: function(response){
//                    console.log(response);
//                    alert('The strategy has been run successfully!');
//                    window.location.href = "times_dashboard";
//                },
//                error: function(error){
//                    console.log(error);
//                }
//            });
//
//		}
//	});
//});


// wait for the document to be loaded, otherwise
// ag-Grid will not find the div in the document.
//document.addEventListener('DOMContentLoaded', function () {
//  var eGridDiv = document.querySelector('#myGrid');
//  new agGrid.Grid(eGridDiv, gridOptions);
//});