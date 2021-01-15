var colDefs = [];
var rowsDefs = [];

// coloring cells: https://www.ag-grid.com/documentation/javascript/row-styles/#example-row-class-rules

//https://plnkr.co/edit/?p=preview&preview  POUR LES DATES NON EDITABLES

// Add rows to table
function createRowsTable(col, rowsValues){

    for (var val = 0; val < rowsValues.length; val++){
        for (var subVal = 0; subVal < rowsValues[val].length; subVal++){
            rows = {};
            for (var name = 0; name < col.length; name++){
                rows[col[name]] = rowsValues[name][subVal];
            }
            rowsDefs.push(rows);
        }
    }
}

// Add columns to table
function createColumnsTable(val){
    for (var i = 0; i < val.length; i++) {
      //var dict = {headerName: val[i], field: val[i]}; AJOUTER DATES NON EDITABLES
      var dictField = {field: val[i]};
      colDefs.push(dictField);
    }
}

// GridOptions for the table
var gridOptions = {
  columnDefs: colDefs ,
  defaultColDef: {
    flex: 1,
    editable: true
  },
  onCellValueChanged: onCellValueChanged,
  rowData: rowsDefs,
  groupDefaultExpanded: 1,
  enableCellChangeFlash: true,
  animateRows: true,
};

function onCellValueChanged(params){
      //params.colDef.cellStyle = {backgroundColor: 'green'};
      //gridOptions.api.refreshCells({force : true});


//      const focusedCell =  params.api.getFocusedCell();
//      focusedCell.column.colDef.cellStyle = { 'background-color': '#b7e4ff' };
//      params.api.refreshCells({force: true });

      const focusedCell =  params.api.getFocusedCell();
      const rowNode = params.api.getRowNode(focusedCell.rowIndex);
      const column = focusedCell.column.colDef.field;
      focusedCell.column.colDef.cellStyle = { 'background-color': 'green'};
      console.log(rowNode);
      console.log(column);

      params.api.refreshCells({
            force: true,
            columns: [column],
            rowNodes: [rowNode]
        });





}


// Get the data from AG grid table   TO AUTOMATE BECAUSE COL MAY CHANGE
function getDataFromTable(){


    // param: noms des colonnes
    // créer double listes dans une liste avec loopant sur les noms des cols
    // renvoie json doubles listes avec les noms des colonne
    // dans python: on transforme ça en df pour l'envoyer dans la db

    var input_asset = [];

    var col = ['AUD']

    gridOptions.api.forEachNode(function(rowNode, index) {
        input_asset.push(rowNode.data['AUD']);
    });


    console.log(input_asset);

//    var input_asset = [];
//    var input_category = [];
//    var input_signal_ticker = [];
//    var input_future_ticker = [];
//    var input_costs = [];
//    var input_leverage = [];
//
//    gridOptions.api.forEachNode(function(rowNode, index) {
//        input_asset.push(rowNode.data.asset);
//        input_category.push(rowNode.data.category);
//        input_signal_ticker.push(rowNode.data.signal_ticker);
//        input_future_ticker.push(rowNode.data.future_ticker);
//        input_costs.push(rowNode.data.costs);
//        input_leverage.push(rowNode.data.s_leverage);
//    });
//
//    var json_data = JSON.stringify({"input_asset": input_asset,
//                                    "input_category": input_category,
//                                    "input_signal_ticker": input_signal_ticker,
//                                    "input_future_ticker": input_future_ticker,
//                                    "input_costs": input_costs,
//                                    "input_leverage": input_leverage});
//    return json_data;
}

$(function(){
	$('#contact-form-button-times').click(function(){

	    var json_data = getDataFromTable();
        var form_data = $('form').serialize();

        var check = checkReceivedDataTimes();
        console.log(check);

        if (check != 'error'){
            $.ajax({
                url: "received_data_times_form",
                data: {form_data: form_data, json_data: json_data},
                type: 'POST',
                success: function(response){
                    console.log(response);
                    alert('The strategy has been run successfully!');
                    window.location.href = "times_dashboard";
                },
                error: function(error){
                    console.log(error);
                }
            });

		}
	});
});


// wait for the document to be loaded, otherwise
// ag-Grid will not find the div in the document.
document.addEventListener('DOMContentLoaded', function () {
  var eGridDiv = document.querySelector('#myGrid');
  new agGrid.Grid(eGridDiv, gridOptions);
});