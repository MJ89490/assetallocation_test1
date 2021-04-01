ready_to_send = false
type_of_request = ''
dateTo = []

var type_of_request = ''
// Funds to select from strategy page
fundSelectedFromStrategyPage = []

// Versions to select from strategy page
versionSelectedFromStrategyPage = []

// Weight
weightFund = []

// Calendar
show_calendar = ''

// KEEP THE SELECTED VALUE WHILE RELOADING PAGE
window.onload = function() {
    var selItem = sessionStorage.getItem("selValFund");
    $('#select-fund-from-strategy-page').val(selItem);

    var selItemWeight = sessionStorage.getItem("SelItemWeight");
    console.log(sessionStorage.getItem("SelItemWeight"));
    $('#input_weight_fund_strategy').val(selItemWeight);

//    var selValVersion = sessionStorage.getItem("selValVersion");
//    console.log(sessionStorage.getItem("selValVersion"));
//    $('#select-version-from-strategy-page').val(selValVersion);
//
//    var selValDateTo = sessionStorage.getItem("selValDateTo");
//    console.log(sessionStorage.getItem("selValDateTo"));
//    $('#select-date-to-strategy-page').val(selValDateTo);
}

// SELECT A FUND
$('#select-fund-from-strategy-page').change(function() {
        var selValFund = $(this).val();
        sessionStorage.setItem("selValFund", selValFund);

        fund = document.getElementById("select-fund-from-strategy-page").value

        fundSelectedFromStrategyPage.push(fund);

        if (fundSelectedFromStrategyPage.length != 1){
            fundSelectedFromStrategyPage.splice(0, fundSelectedFromStrategyPage.length-1);
        }

        var json_data = JSON.stringify({'fund': fundSelectedFromStrategyPage[0],
                                        'type_of_request': 'selected_fund'});

        $.ajax({

                url: "receive_data_from_times_strategy_page",
                data: {json_data: json_data},
                type: 'POST',
                success: function(response){
                    console.log('success');
                },
                error: function(error){
                    console.log(error);
                }
            });

});


//SELECT THE FUND WEIGHT
$('#input_weight_fund_strategy').change(function() {
        var selValWeight = $(this).val();
        sessionStorage.setItem("SelItemWeight", selValWeight);

        weight = document.getElementById("input_weight_strategy").value

        weightFund.push(parseFloat(document.getElementById("input_weight_fund_strategy").value))

        var json_data = JSON.stringify({'strategy_weight': weightFund[0],
                                        'type_of_request': 'selected_fund_weight'});

        $.ajax({

                url: "receive_data_from_times_strategy_page",
                data: {json_data: json_data},
                type: 'POST',
                success: function(response){
                    console.log('success');
                },
                error: function(error){
                    console.log(error);
                }
            });

});


$('#select-version-from-strategy-page').change(function() {
//        var selValVersion = $(this).val();
//        sessionStorage.setItem("selValVersion", selValVersion);

        version = document.getElementById("select-version-from-strategy-page").value

        versionSelectedFromStrategyPage.push(parseInt(version));

        if (versionSelectedFromStrategyPage.length != 1){
            versionSelectedFromStrategyPage.splice(0, versionSelectedFromStrategyPage.length-1);
        }

        // Take the date_to and send it with the version via AJAX
        var date_to = SelectDateToStrategyPage();

        var json_data = JSON.stringify({'version': versionSelectedFromStrategyPage[0],
                                        'date_to': dateTo[0],
                                        'type_of_request': 'selected_version_date_to',
                                        'run_existing-version': true});

        $.ajax({url: "receive_data_from_times_strategy_page",
                data: {json_data: json_data},
                type: 'POST',
                success: function(response){
                    console.log('success');
                    window.location.href = "times_strategy";
                },
                error: function(error){
                    console.log(error);
                }
            });
});

function SelectDateToStrategyPage(){

        dateToPage = document.getElementById("select-date-to-strategy-page").value

        dateTo.push(dateToPage);

        if (dateTo.length != 1){
            dateTo.splice(0, dateTo.length-1);
        }

        return dateTo[0]
};



















//
//
//function sendDataToPython(){
////    'fund': fundSelectedFromStrategyPage[0],
//
//    if (ready_to_send == true){
//       var json_data = JSON.stringify({
//                                       'version': versionSelectedFromStrategyPage[0],
//                                       'fund_weight': weightFund[0],
//                                       'date_to': dateTo[0],
//                                       'type_of_request': 'run_existing_version'});
//
//        $.ajax({
//                url: "receive_data_from_times_strategy_page",
//                data: {json_data: json_data},
//                type: 'POST',
//                success: function(response){
//                    console.log('success');
//                    window.location.href = "times_strategy";
//                },
//                error: function(error){
//                    console.log(error);
//                }
//            });
//    }
//}


