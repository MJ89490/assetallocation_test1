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

        weight = document.getElementById("input_weight_fund_strategy").value

        weightFund.push(parseFloat(document.getElementById("input_weight_fund_strategy").value))

        var json_data = JSON.stringify({'fund_weight': weightFund[0],
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

//function selectFund() {
//        var select_box = document.getElementById("select-fund-from-strategy-page");
//        var fund = select_box.options[select_box.selectedIndex].value;
//        console.log(select_box);
//        console.log(fund);
//
//        fundSelectedFromStrategyPage.push(fund);
//
//        if (fundSelectedFromStrategyPage.length != 1){
//            fundSelectedFromStrategyPage.splice(0, fundSelectedFromStrategyPage.length-1);
//        }
//
//        console.log(fundSelectedFromStrategyPage);
//        var json_data = JSON.stringify({'fund': fundSelectedFromStrategyPage[0],
//                                        'type_of_request': 'selected_fund'});
//
//        $.ajax({
//
//                url: "receive_data_from_times_strategy_page",
//                data: {json_data: json_data},
//                type: 'POST',
//                success: function(response){
//                    console.log('success');
//                },
//                error: function(error){
//                    console.log(error);
//                }
//            });
//}
//
//function selectVersion() {
//        var select_box = document.getElementById("select-version-from-strategy-page");
//        var version = select_box.options[select_box.selectedIndex].value;
//
//        versionSelectedFromStrategyPage.push(parseInt(version));
//
//        if (versionSelectedFromStrategyPage.length != 1){
//            versionSelectedFromStrategyPage.splice(0, versionSelectedFromStrategyPage.length-1);
//        }
////        weightFund.push(parseFloat(document.getElementById("input_weight_fund_strategy").value))
//}


$('#select-version-from-strategy-page').change(function() {
//        var selValVersion = $(this).val();
//        sessionStorage.setItem("selValVersion", selValVersion);

        version = document.getElementById("select-version-from-strategy-page").value

        versionSelectedFromStrategyPage.push(parseInt(version));

        if (versionSelectedFromStrategyPage.length != 1){
            versionSelectedFromStrategyPage.splice(0, versionSelectedFromStrategyPage.length-1);
        }



        var json_data = JSON.stringify({'version': versionSelectedFromStrategyPage[0],
                                        'type_of_request': 'selected_version'});

        $.ajax({url: "receive_data_from_times_strategy_page",
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





//function selectDateTo(){
//    var dateToPage =  document.getElementById("select-date-to-from-strategy-page").value;
//    type_of_request = 'send_data';
//    console.log(dateToPage);
//    ready_to_send = true;
//    dateTo.push(dateToPage);
//    this.sendDataToPython();
//}

$('#select-date-to-strategy-page').change(function() {
//        var selValDateTo = $(this).val();
//        sessionStorage.setItem("selValDateTo", selValDateTo);

        dateToPage = document.getElementById("select-date-to-strategy-page").value

        dateTo.push(dateToPage);

        if (dateTo.length != 1){
            dateTo.splice(0, dateTo.length-1);
        }

        var json_data = JSON.stringify({'date_to': dateTo[0],
                                        'type_of_request': 'selected_date_to',
                                        'run_existing-version': true});

        $.ajax({

                url: "receive_data_from_times_strategy_page",
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


