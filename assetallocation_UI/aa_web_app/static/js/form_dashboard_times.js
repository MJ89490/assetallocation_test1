version_data_to_send_to_python = []
fund_data_to_send_to_python = []
ready_to_send = false
type_of_request = 'charts_data_sidebar'

function sideBarFund() {
        var select_box = document.getElementById("send_data_fund_from_sidebar");
        var fund = select_box.options[select_box.selectedIndex].value;

        fund_data_to_send_to_python.push(fund);
        console.log(fund_data_to_send_to_python.length);

        if (fund_data_to_send_to_python.length != 1){
            fund_data_to_send_to_python.splice(0, fund_data_to_send_to_python.length-1);
        }
}

function sideBarVersion() {
        var select_box = document.getElementById("send_data_version_from_sidebar");
        var version = select_box.options[select_box.selectedIndex].value;
        ready_to_send = true;
        version_data_to_send_to_python.push(parseInt(version));

        console.log(version_data_to_send_to_python);

        if (version_data_to_send_to_python.length != 1){
            version_data_to_send_to_python.splice(0, version_data_to_send_to_python.length-1);
        }

        this.sendDataToPython();

}

function sideBarExportFund() {
//CREATE ERROR HANDLING BECAUSE WE CANNOT HAVE MORE THAN 1 FUND
        var select_box = document.getElementById("send_data_fund_export_from_sidebar");
        var fund = select_box.options[select_box.selectedIndex].value;
        this.sendDataToPython(fund);
}

function sideBarExportVersion() {
        var select_box = document.getElementById("send_data_version_export_from_sidebar");
        var version = select_box.options[select_box.selectedIndex].value;
        ready_to_send = true;
        type_of_request = 'export_data_sidebar'
        sendDataToPython(parseInt(version));
}

function sendDataToPython(){

    if (ready_to_send == true){

        var json_data = JSON.stringify({"input_fund": fund_data_to_send_to_python, "inputs_version": version_data_to_send_to_python, "type_of_request": type_of_request});
        console.log(json_data);

        $.ajax({
                url: "receive_sidebar_data_times_form",
                data: {json_data: json_data},
                type: 'POST',
                success: function(response){
                    window.location.href = "times_dashboard";
                },
                error: function(error){
                    console.log(error);
                }
            });
    }
}


