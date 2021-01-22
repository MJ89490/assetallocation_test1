version_data_to_send_to_python = []
fund_data_to_send_to_python = []
ready_to_send = false
type_of_request = 'send_data_for_times_strategy'
dateTo = []

function sideBarFund() {
        var select_box = document.getElementById("send_data_fund_from_sidebar");
        var fund = select_box.options[select_box.selectedIndex].value;

        fund_data_to_send_to_python.push(fund);

        if (fund_data_to_send_to_python.length != 1){
            fund_data_to_send_to_python.splice(0, fund_data_to_send_to_python.length-1);
        }
}

function selectVersionPage() {
        var select_box = document.getElementById("send_data_version_from_page_times");
        var version = select_box.options[select_box.selectedIndex].value;

        version_data_to_send_to_python.push(parseInt(version));

        if (version_data_to_send_to_python.length != 1){
            version_data_to_send_to_python.splice(0, version_data_to_send_to_python.length-1);
        }
        console.log(version_data_to_send_to_python);

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
        var json_data = JSON.stringify({
                                        "inputs_version": version_data_to_send_to_python[0],
                                        "inputs_date_to": dateTo[0],
                                        "type_of_request": type_of_request,
                                        });

        console.log(json_data);

        $.ajax({
                url: "times_strategy",
                data: {json_data: json_data},
                type: 'POST',
                success: function(response){
                    console.log(response);
                },
                error: function(error){
                    console.log(error);
                }
            });
    }
}


