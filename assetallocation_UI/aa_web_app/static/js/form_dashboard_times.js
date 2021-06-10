
version_data_to_send_to_python = []
fund_data_to_send_to_python = []
ready_to_send = false
type_of_request = ''
dateTo = []

// -------------------------------------------- CHARTS SIDEBAR --------------------------------------------------------
function sideBarFund() {
        var select_box = document.getElementById("send_data_fund_from_sidebar");
        var fund = select_box.options[select_box.selectedIndex].value;

        fund_data_to_send_to_python.push(fund);

        if (fund_data_to_send_to_python.length != 1){
            fund_data_to_send_to_python.splice(0, fund_data_to_send_to_python.length-1);
        }
}

function sideBarChartsVersion() {
        var select_box = document.getElementById("send_data_version_from_sidebar");
        var version = select_box.options[select_box.selectedIndex].value;

        version_data_to_send_to_python.push(parseInt(version));

        if (version_data_to_send_to_python.length != 1){
            version_data_to_send_to_python.splice(0, version_data_to_send_to_python.length-1);
        }

        var jsonData = JSON.stringify({"input_fund": fund_data_to_send_to_python[0],
                                        "inputs_version": version_data_to_send_to_python[0],
                                        "type_of_request": 'charts_data_sidebar',
                                        });

        $.ajax({
            url: $SIDEBAR_URL,
            data: {jsonData: jsonData},
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

function populateChartsDateTo(dates){
         $("#input_date_to_side_bar_times").append("<option hidden >date to</option>");
        for( var i = 0; i< dates.length; i++){
            var id = dates[i];
            var name = dates[i];
            $("#input_date_to_side_bar_times").append("<option>"+name+"</option>");
        }
}

function sendDateToSidebar(){
    var dateToSidebar =  document.getElementById("input_date_to_side_bar_times").value;
    sessionStorage.setItem("selBarChartsDateTo", dateToSidebar);

    console.log(dateToSidebar);
    dateTo.push(dateToSidebar);

    var jsonData = JSON.stringify({"inputs_date_to": dateTo[0],
                                    "type_of_request": 'date_charts_sidebar'
                                   });
    $.ajax({
        url: $SIDEBAR_URL,
        data: {jsonData: jsonData},
        type: 'POST',
        success: function(data){
                alert('The charts will be updated shortly...');

                let date = dateTo[0]
                date_to = date.split("/").join("S");

//                construction of the url CHANGE THE VARIABLES NAMES
                let pathArr = $PROJECTS_URL.split("/");
                let projectsPathArr = pathArr.slice(0, pathArr.length - 3);
                console.log(projectsPathArr);
                let strategyPathArr = projectsPathArr.concat([fund_data_to_send_to_python[0], version_data_to_send_to_python[0], date_to]);
                let strategyPathURL = strategyPathArr.join('/');

                window.location.href  = strategyPathURL
        },
        error: function(error){
            console.log(error);
        }
    });
}

// -------------------------------------------- EXPORT SIDEBAR --------------------------------------------------------
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

        version_data_to_send_to_python.push(parseInt(version));

        if (version_data_to_send_to_python.length != 1){
            version_data_to_send_to_python.splice(0, version_data_to_send_to_python.length-1);
        }

        var jsonData = JSON.stringify({"input_fund": fund_data_to_send_to_python[0],
                                        "inputs_version": version_data_to_send_to_python[0],
                                        "type_of_request": 'export_data_sidebar',
                                       });

        $.ajax({
                url: $SIDEBAR_URL,
                data: {jsonData: jsonData},
                type: 'POST',

                success: function(data){
                    populateExportDateTo(data['sidebar_date_to']);
                    alert('You can select a date to to export the data!');
                },

                error: function(error){
                    console.log(error);
                }
            });

}

function populateExportDateTo(dates){
         $("#input_date_to_export_side_bar_times").append("<option hidden >date to</option>");
        for( var i = 0; i< dates.length; i++){

            var id = dates[i];
            var name = dates[i];
            console.log(id);
            $("#input_date_to_export_side_bar_times").append("<option>"+name+"</option>");
        }
}

function sendDateToExportSidebar(){
    var dateToSidebar =  document.getElementById("input_date_to_export_side_bar_times").value;

    dateTo.push(dateToSidebar);

    var jsonData = JSON.stringify({"inputs_date_to": dateToSidebar,
                                   "input_fund": fund_data_to_send_to_python[0],
                                   "inputs_version": version_data_to_send_to_python[0],
                                   "type_of_request": 'date_to_export_data_sidebar'
                                   });

    $.ajax({
        url: $SIDEBAR_URL,
        data: {jsonData: jsonData},
        type: 'POST',
        success: function(success){
            console.log(success);

            type_of_request = 'export_charts_data';
            start_date_sidebar = 'None';
            let fundNameValue = sessionStorage.getItem('sessionFundName');
            let strategyVersionValue = sessionStorage.getItem('sessionStrategyVersion');
            let dateToValue = sessionStorage.getItem('sessionDateTo');
            date_to = dateToValue.split("/").join("S");

            let pathArr = $PROJECTS_URL.split("/");
            let projectsPathArr = pathArr.slice(0, pathArr.length - 3);
            let strategyPathArr = projectsPathArr.concat([fundNameValue, strategyVersionValue, date_to, start_date_sidebar, type_of_request]);
            let strategyPathURL = strategyPathArr.join('/');
            window.location.href  = strategyPathURL;
        },
        error: function(error){
            console.log(error);
        }
    });
}
