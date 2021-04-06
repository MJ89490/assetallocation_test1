// GET VALUES FROM MODEL ASSETS TABLE
function getDataFromTable()
{
      var names = [];
      var assets = [];
      var signalTickers = [];
      var futureTickers = [];
      var costs = [];
      var leverages = [];
      var tickers = []

      // GET VALUES FROM INPUT ONLY
      $("#faqs").find('tr').each(function(){

         var name = $(this).find("td:eq(0) input[type='text']").val();
         var asset = $(this).find("td:eq(1) input[type='text']").val();
         var futureTicker = $(this).find("td:eq(2) input[type='text']").val();
         var signalTicker = $(this).find("td:eq(3) input[type='text']").val();
         var cost = $(this).find("td:eq(4) input[type='text']").val();
         var leverage = $(this).find("td:eq(5) input[type='text']").val();

        if (typeof name != 'undefined' || typeof asset != 'undefined' || typeof cost != 'undefined' || typeof leverage != 'undefined') {
            names.push(name);
            assets.push(asset);
            costs.push(parseFloat(cost));
            leverages.push(parseFloat(leverage));
        }

        if (typeof signalTicker != 'undefined'){
            signalTickers.push(signalTicker);
        }

        if (typeof futureTicker != 'undefined'){
            futureTickers.push(futureTicker);
        }
      });

      // GET VALUES FROM SELECT ONLY
      $("#faqs" + ' select').each(function(){
         tickers.push($(this).val());
      })

      // GET VALUES FOR THE SIGNAL AND FUTURE FROM TICKERS
      // IF INDEX IS EVEN == FUTURE OTHERWISE SIGNAL
      var i;

      for (i = 0; i < tickers.length; ++i) {

        // EVEN = FUTURE
        if(i % 2 == 0){
            futureTickers.push(tickers[i]);
        }
        else{
            signalTickers.push(tickers[i]);
        }
      }

    var versionName = $("#input_version_name_strategy").val();

    var jsonData = JSON.stringify({"input_name": names,
                                   "input_asset": assets,
                                   "input_signal_ticker": signalTickers,
                                   "input_future_ticker": futureTickers,
                                   "input_costs": costs,
                                   "input_leverage": leverages,
                                   "input_version_name_strategy": versionName});

    return jsonData;

};

// CHECKING IF VALUES OF THE SIGNALS ARE IN THE ASCENDING ORDER, OTHERWISE THE SIGNALS ARE WRONG
function checkArray(array) {
    var aa = array.slice(1);
    if (aa.every((a, i) => array[i] <= a)) {
        // No error
        return false;
    }
    return true;

}

// CHECKING VALUES OF THE FORM BEFORE RUNNING THE MODEL
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

// WRITE THE DAY OF THE WEEK IN THE TEXT BOX OF MODEL INPUTS TABLE
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

    console.log(dayName);

    document.getElementById("input_weekday_times").value = dayName.substring(0,3).toUpperCase();
}

// SEND THE DATA TO PYTHON
$(function(){
	$('#contact-form-button-times').click(function(){
	    var jsonData = getDataFromTable();
        var form_data = $('form').serialize();
        var check = checkReceivedDataTimes();

        alert("The strategy is about to run...");

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
