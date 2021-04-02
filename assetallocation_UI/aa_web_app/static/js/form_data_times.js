function getDataFromTable()
{
      var assets = [];
      var categories = [];
      var signalTickers = [];
//      var futureTickers = [];
      var costs = [];
      var leverages = [];

      $("#faqs").find('tr').each(function(){

         var asset = $(this).find("td:eq(0) input[type='text']").val();
         var category = $(this).find("td:eq(1) input[type='text']").val();
         var signalTicker = $(this).find("td:eq(2) input[type='text']").val();
//         var futureTicker = $(this).find("td:eq(3) input[type='text']").val();
         var cost = $(this).find("td:eq(4) input[type='text']").val();
         var leverage = $(this).find("td:eq(5) input[type='text']").val();

        assets.push(asset);
        categories.push(category);
        signalTickers.push(signalTicker);
//        futureTickers.push(futureTicker);
        costs.push(parseFloat(cost));
        leverages.push(parseFloat(leverage));
   });

    assets.shift();
    categories.shift();
    signalTickers.shift();
//    futureTickers.shift();
    costs.shift();
    leverages.shift();

    var versionName = $("#input_version_name_strategy").val();

    var jsonData = JSON.stringify({"input_asset": assets,
                                   "input_category": categories,
                                   "input_signal_ticker": signalTickers,
//                                   "input_future_ticker": futureTickers,
                                   "input_costs": costs,
                                   "input_leverage": leverages,
                                   "input_version_name_strategy": versionName});

    return jsonData;

};

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

//// KEEP THE SELECTED VALUE WHILE RELOADING PAGE
//window.onload = function() {
//    var selItem = sessionStorage.getItem("selValTicker");
//    $('#input_signal_ticker_from_times').val(selItem);
//}
//
//$('#input_signal_ticker_from_times').change(function() {
//    var selValTicker = $(this).val();
//    sessionStorage.setItem("selValTicker", selValTicker);
//
//    var ticker = document.getElementById('input_signal_ticker_from_times').value;
//    console.log(ticker);
//
//    var jsonData = JSON.stringify({"input_signal_ticker_from_times": ticker,
//                                   "type_of_request": 'selected_ticker'});
//
//    $.ajax({
//            url: "receive_data_from_times_strategy_page",
//            data: {json_data:jsonData},
//            type: 'POST',
//            success: function(response){
//                console.log(response);
////                window.location.href = "times_strategy";
//            },
//            error: function(error){
//                console.log(error);
//            }
//        });
//});


$(function(){
	$('#contact-form-button-times').click(function(){
	    var jsonData = getDataFromTable();
	    console.log(jsonData);
        var form_data = $('form').serialize();
        var check = checkReceivedDataTimes();

        alert("Strategy is running...");

        if (check != 'error'){
            $.ajax({
                url: "received_data_times_form",
                data: {form_data: form_data, json_data:jsonData},
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
