version_data_to_send_to_python = []
fund_data_to_send_to_python = []
ready_to_send = false
type_of_request = ''
dateTo = []

// KEEP THE SELECTED VALUE WHILE RELOADING PAGE
//window.onload = function() {
//    var selItemFund = sessionStorage.getItem("selBarFund");
//    $('#send_data_fund_from_sidebar').val(selItemFund);
//
//    var selItemVersion = sessionStorage.getItem("selBarVersion");
//    $('#send_data_version_from_sidebar').val(selItemVersion);
//
//    var selItemChartsDateTo= sessionStorage.getItem("selBarChartsDateTo");
//    $('#input_date_to_side_bar_times').val(selItemChartsDateTo);
//}

function sideBarFund() {
        var select_box = document.getElementById("send_data_fund_from_sidebar");
        var fund = select_box.options[select_box.selectedIndex].value;
//        sessionStorage.setItem("selBarFund", fund);

        fund_data_to_send_to_python.push(fund);
        console.log(fund);

        if (fund_data_to_send_to_python.length != 1){
            fund_data_to_send_to_python.splice(0, fund_data_to_send_to_python.length-1);
        }
}

function sideBarVersion() {
        var select_box = document.getElementById("send_data_version_from_sidebar");
        var version = select_box.options[select_box.selectedIndex].value;
//        sessionStorage.setItem("selBarVersion", version);

        version_data_to_send_to_python.push(parseInt(version));
        console.log(version);

        if (version_data_to_send_to_python.length != 1){
            version_data_to_send_to_python.splice(0, version_data_to_send_to_python.length-1);
        }

        ready_to_send = true;
        type_of_request = 'charts_data_sidebar'
        this.sendDataToPython();
}

function populateChartsDateTo(dates){
         $("#input_date_to_side_bar_times").append("<option hidden >date to</option>");
        for( var i = 0; i< dates.length; i++){
            console.log('IN THE LOOP');
            var id = dates[i];
            var name = dates[i];
            console.log(id);
            $("#input_date_to_side_bar_times").append("<option>"+name+"</option>");
        }
}

function sendDateToSidebar(){
    var dateToSidebar =  document.getElementById("input_date_to_side_bar_times").value;
    sessionStorage.setItem("selBarChartsDateTo", dateToSidebar);

    console.log(dateToSidebar);
    dateTo.push(dateToSidebar);
    type_of_request = 'date_to_data_sidebar'

    var json_data = JSON.stringify({"inputs_date_to": dateTo[0],
                                    "type_of_request": type_of_request
                                   });
    $.ajax({
        url: "receive_sidebar_data_times_form",
        data: {json_data: json_data},
        type: 'POST',
        success: function(data){
            window.location.href = "times_sidebar_dashboard";
        },
        error: function(error){
            console.log(error);
        }
    });
}

function sideBarExportFund() {
        var select_box = document.getElementById("send_data_fund_export_from_sidebar");
        var fund = select_box.options[select_box.selectedIndex].value;

        fund_data_to_send_to_python.push(fund);

        if (fund_data_to_send_to_python.length != 1){
            fund_data_to_send_to_python.splice(0, fund_data_to_send_to_python.length-1);
        }
}

function sideBarExportVersion() {
        var select_box = document.getElementById("send_data_version_export_from_sidebar");
        var version = select_box.options[select_box.selectedIndex].value;
        ready_to_send = true;
        type_of_request = 'export_data_sidebar'

        version_data_to_send_to_python.push(parseInt(version));

        if (version_data_to_send_to_python.length != 1){
            version_data_to_send_to_python.splice(0, version_data_to_send_to_python.length-1);
        }
        this.sendDataToPython();
}

function sendDataToPython(){

    if (ready_to_send == true){

        var json_data = JSON.stringify({"input_fund": fund_data_to_send_to_python[0],
                                        "inputs_version": version_data_to_send_to_python[0],
                                        "type_of_request": type_of_request,
                                        });
        console.log(json_data);

        $.ajax({
                url: "receive_sidebar_data_times_form",
                data: {json_data: json_data},
                type: 'POST',
                success: function(data){
                    populateChartsDateTo(data['sidebar_date_to']);
                    alert('You can select a date to!');
                },
                error: function(error){
                    console.log(error);
                }
            });
    }
}
