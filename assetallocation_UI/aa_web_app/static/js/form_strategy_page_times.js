version_data_to_send_to_python = []

ready_to_send = false
type_of_request = 'send_data_for_times_strategy'
dateTo = []

var type_request = ''
// Funds to select from strategy page
fund_selected_from_strategy_page = []

// Versions to select from strategy page
version_selected_from_strategy_page = []
show_calendar = ''

function selectFund() {
        var select_box = document.getElementById("select-fund-from-strategy-page");
        var fund = select_box.options[select_box.selectedIndex].value;

        fund_selected_from_strategy_page.push(fund);

        if (fund_selected_from_strategy_page.length != 1){
            fund_selected_from_strategy_page.splice(0, fund_selected_from_strategy_page.length-1);
        }

        type_request = 'fund_selected';
        ready_to_send = true;
        sendDataToPython();
}

function selectVersion() {
        var select_box = document.getElementById("select-version-from-strategy-page");
        var version = select_box.options[select_box.selectedIndex].value;

        version_selected_from_strategy_page.push(parseInt(version));

        if (version_selected_from_strategy_page.length != 1){
            version_selected_from_strategy_page.splice(0, version_selected_from_strategy_page.length-1);
        }
        console.log(version_selected_from_strategy_page);
        type_request = 'version_selected';
        show_calendar = 'show_calendar';
        ready_to_send = true;
        sendDataToPython();

}

function selectDateTo(){
    var dateToPage =  document.getElementById("input_date_to_times").value;
    console.log(dateToPage);
    ready_to_send = true;
    dateTo.push(dateToPage);
    this.sendDataToPython();
}

function sendDataToPython(){

    if (ready_to_send == true){
//        var json_data = JSON.stringify({
//                                        "inputs_version": version_data_to_send_to_python[0],
//                                        "inputs_date_to": dateTo[0],
//                                        "type_of_request": type_of_request,
//                                        });
       var json_data = JSON.stringify({'fund': fund_selected_from_strategy_page[0],
                                       'version': version_selected_from_strategy_page[0],
                                       'show_calendar': show_calendar,
                                       'type_request': type_request});

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


