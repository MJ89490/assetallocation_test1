data_to_send_to_python = []
ready_to_send = false

function sideBarFund() {
//CREATE ERROR HANDLING BECAUSE WE CANNOT HAVE MORE THAN 1 FUND
        var select_box = document.getElementById("send_data_fund_from_sidebar");
        var fund = select_box.options[select_box.selectedIndex].value;
        this.sendDataToPython(fund);
}

function sideBarVersion() {
        var select_box = document.getElementById("send_data_version_from_sidebar");
        var version = select_box.options[select_box.selectedIndex].value;
        ready_to_send = true;
        sendDataToPython(parseInt(version));
}

function sendDataToPython(val){
    console.log(val);
    data_to_send_to_python.push(val);
    console.log(data_to_send_to_python);

    if (ready_to_send == true){
        var json_data = JSON.stringify({"inputs_sidebar": data_to_send_to_python});
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


