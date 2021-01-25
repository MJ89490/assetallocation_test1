ready_to_send = false
type_of_request = ''
dateTo = []

var type_of_request = ''
// Funds to select from strategy page
fundSelectedFromStrategyPage = []

// Versions to select from strategy page
versionSelectedFromStrategyPage = []

// Calendar
show_calendar = ''

function selectFund() {
        var select_box = document.getElementById("select-fund-from-strategy-page");
        var fund = select_box.options[select_box.selectedIndex].value;

        fundSelectedFromStrategyPage.push(fund);

        if (fundSelectedFromStrategyPage.length != 1){
            fundSelectedFromStrategyPage.splice(0, fundSelectedFromStrategyPage.length-1);
        }

         type_of_request = 'fund_selected';
        ready_to_send = true;
        sendDataToPython();
}

function selectVersion() {
        var select_box = document.getElementById("select-version-from-strategy-page");
        var version = select_box.options[select_box.selectedIndex].value;

        versionSelectedFromStrategyPage.push(parseInt(version));

        if (versionSelectedFromStrategyPage.length != 1){
            versionSelectedFromStrategyPage.splice(0, versionSelectedFromStrategyPage.length-1);
        }
        console.log(versionSelectedFromStrategyPage);
         type_of_request = 'version_selected';
        show_calendar = 'show_calendar';
        ready_to_send = true;
        sendDataToPython();

}

function selectDateTo(){
    var dateToPage =  document.getElementById("input_date_to_times").value;
    console.log(dateToPage);
    type_of_request = 'date_selected';
    ready_to_send = true;
    dateTo.push(dateToPage);
    this.sendDataToPython();
}

function sendDataToPython(){

    if (ready_to_send == true){
       var json_data = JSON.stringify({'fund': fundSelectedFromStrategyPage[0],
                                       'version': versionSelectedFromStrategyPage[0],
                                       'date_to': dateTo[0],
                                       'show_calendar': show_calendar,
                                       'type_of_request':  type_of_request});

       console.log(json_data);

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


