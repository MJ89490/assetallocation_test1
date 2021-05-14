ready_to_send = false
type_of_request = ''
dateTo = []

var type_of_request = ''

// FUNDS TO SELECT FROM STRATEGY PAGE
fundSelectedFromStrategyPage = []

// VERSIONS TO SELECT FROM STRATEGY PAGE
versionSelectedFromStrategyPage = []

// WEIGHT
weightStrategy = []

// KEEP THE SELECTED VALUE WHILE RELOADING PAGE
window.onload = function() {
    var selItem = sessionStorage.getItem("selValFund");
    $('#select-fund-from-strategy-page').val(selItem);

    var selItemWeight = sessionStorage.getItem("SelItemWeight");
    $('#input_weight_strategy').val(selItemWeight);
}



// SELECT A FUND
$('.select-fund-from-strategy-page').change(function() {
        var selValFund = $(this).val();
        sessionStorage.setItem("selValFund", selValFund);

          alert(selValFund);

//        fund = document.getElementById("select-fund-from-strategy-page").value
//        var fund = document.getElementById('select-fund-from-strategy-page').fireEvent("onchange");

        console.log(selValFund);
        fundSelectedFromStrategyPage.push(selValFund);

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


//SELECT THE STRATEGY WEIGHT
$('#input_weight_strategy').change(function() {
        var selValWeight = $(this).val();
        sessionStorage.setItem("SelItemWeight", selValWeight);

        weight = document.getElementById("input_weight_strategy").value

        weightStrategy.push(parseFloat(document.getElementById("input_weight_strategy").value))

        var json_data = JSON.stringify({'strategy_weight': weightStrategy[0],
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

// SELECT THE VERSION OF THE STRATEGY
$('#select-version-from-strategy-page').change(function() {
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

// SELECT THE DATE
function SelectDateToStrategyPage(){

        dateToPage = document.getElementById("select-date-to-strategy-page").value

        dateTo.push(dateToPage);

        if (dateTo.length != 1){
            dateTo.splice(0, dateTo.length-1);
        }

        return dateTo[0]
};
