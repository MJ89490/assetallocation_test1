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

// KEEP THE SELECTED VALUE WHILE RELOADING PAGE IN THE SELECT BOX AND TEXT BOX
window.onload = function() {
    const getFundName = sessionStorage.getItem("sessionFundName");
    $('#select_fund_name').val(getFundName);

    const getStrategyWeight = sessionStorage.getItem("sessionStrategyWeight");
    $('#select_weight_strategy').val(getStrategyWeight);
}

// SELECT A FUND
$('.select-fund-from-strategy-page').change(function() {
        var fundValue = $(this).val();
        sessionStorage.setItem("sessionFundName", fundValue);
});


//SELECT THE STRATEGY WEIGHT
$('#select_weight_strategy').change(function() {
        var weightValue = $(this).val();
        sessionStorage.setItem("sessionStrategyWeight", weightValue);
});

// SELECT THE VERSION OF THE STRATEGY
$('#select-version-from-strategy-page').change(function() {
        version = document.getElementById("select-version-from-strategy-page").value

        sessionStorage.setItem("sessionStrategyVersion", version.split(':')[0]);

        versionSelectedFromStrategyPage.push(parseInt(version));

        if (versionSelectedFromStrategyPage.length != 1){
            versionSelectedFromStrategyPage.splice(0, versionSelectedFromStrategyPage.length-1);
        }

        // Take the date_to and send it with the version via AJAX
        var date_to = SelectDateToStrategyPage();

        let fundNameValue = sessionStorage.getItem('sessionFundName');
        let strategyWeightValue = sessionStorage.getItem('sessionStrategyWeight');

        var json_data = JSON.stringify({'strategy_version': versionSelectedFromStrategyPage[0],
                                        'date_to': dateTo[0],
                                        'fund_name': fundNameValue,
                                        'strategy_weight_user': strategyWeightValue,
                                        'type_of_request': 'selected_version',
                                        'run_existing-version': true});

        $.ajax({url: "times_strategy",
                data: {json_data: json_data},
                type: 'POST',
                success: function(data){
                    console.log('success');

                    let userNameValue = sessionStorage.getItem('username');

                    window.location.href = "times_strategy_existing_version/" + data['version_selected'] + "/" + data['assets'] + "/" + data['message']
                    + "/" + data['inputs_existing_versions_times'] + "/" + userNameValue;

                },
                error: function(error){
                    console.log(error);
                }
            });
});

// SELECT THE DATE
function SelectDateToStrategyPage(){

        dateToPage = document.getElementById("select-date-to-strategy-page").value
        sessionStorage.setItem("sessionDateTo", dateToPage);

        dateTo.push(dateToPage);

        if (dateTo.length != 1){
            dateTo.splice(0, dateTo.length-1);
        }

        return dateTo[0]
};



