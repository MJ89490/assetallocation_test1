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

// SELECT A FUND
window.onload = function() {
    var selItem = sessionStorage.getItem("SelItem");
    $('#select-fund-from-strategy-page').val(selItem);
    }

$('#select-fund-from-strategy-page').change(function() {
        var selVal = $(this).val();
        sessionStorage.setItem("SelItem", selVal);

        alert(document.getElementById("select-fund-from-strategy-page").value);

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
                    alert('success');
                },
                error: function(error){
                    console.log(error);
                }
            });

});


//SELECT
window.onload = function() {
    var selItem = sessionStorage.getItem("SelItem");
    $('#input_weight_fund_strategy').val(selItem);
    }

$('#input_weight_fund_strategy').change(function() {
        var selVal = $(this).val();
        sessionStorage.setItem("SelItem", selVal);

        alert(document.getElementById("input_weight_fund_strategy").value);

        weight = document.getElementById("input_weight_fund_strategy").value

        weightFund.push(parseFloat(document.getElementById("input_weight_fund_strategy").value))

//        var json_data = JSON.stringify({'fund': fundSelectedFromStrategyPage[0],
//                                        'type_of_request': 'selected_fund'});

//        $.ajax({
//
//                url: "receive_data_from_times_strategy_page",
//                data: {json_data: json_data},
//                type: 'POST',
//                success: function(response){
//                    console.log('success');
//                    alert('success');
//                },
//                error: function(error){
//                    console.log(error);
//                }
//            });

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

function selectVersion() {
        var select_box = document.getElementById("select-version-from-strategy-page");
        var version = select_box.options[select_box.selectedIndex].value;

        versionSelectedFromStrategyPage.push(parseInt(version));

        if (versionSelectedFromStrategyPage.length != 1){
            versionSelectedFromStrategyPage.splice(0, versionSelectedFromStrategyPage.length-1);
        }
//        weightFund.push(parseFloat(document.getElementById("input_weight_fund_strategy").value))
}

function selectDateTo(){
    var dateToPage =  document.getElementById("select-date-to-from-strategy-page").value;
    type_of_request = 'send_data';
    console.log(dateToPage);
    ready_to_send = true;
    dateTo.push(dateToPage);
    this.sendDataToPython();
}

function sendDataToPython(){
//    'fund': fundSelectedFromStrategyPage[0],

    if (ready_to_send == true){
       var json_data = JSON.stringify({
                                       'version': versionSelectedFromStrategyPage[0],
                                       'fund_weight': weightFund[0],
                                       'date_to': dateTo[0],
                                       'type_of_request': 'run_existing_version'});

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
    }
}


