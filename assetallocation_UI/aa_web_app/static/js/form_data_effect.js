var rowData = [
  {currency: 'BRL', implied_ticker: 'BCNI3M Curncy', spot_ticker: 'BRLUSD Curncy', carry_ticker: 'BRLUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'LatAm'},
  {currency: 'PEN', implied_ticker: 'PSNI3M Curncy', spot_ticker: 'PENUSD Curncy', carry_ticker: 'PENUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'LatAm'},
  {currency: 'MXN', implied_ticker: 'MXNI3M Curncy', spot_ticker: 'MXNUSD Curncy', carry_ticker: 'MXNUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'LatAm'},
  {currency: 'COP', implied_ticker: 'CLNI3M Curncy', spot_ticker: 'COPUSD Curncy', carry_ticker: 'COPUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'LatAm'},
  {currency: 'CLP', implied_ticker: 'CHNI3M Curncy', spot_ticker: 'CLPUSD Curncy', carry_ticker: 'CLPUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'LatAm'},
  {currency: 'TRY', implied_ticker: 'TRYI3M Curncy', spot_ticker: 'TRYUSD Curncy', carry_ticker: 'TRYUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'CEEMA'},
  {currency: 'RUB', implied_ticker: 'RUBI3M Curncy', spot_ticker: 'RUBUSD Curncy', carry_ticker: 'RUBUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'CEEMA'},
  {currency: 'CZK', implied_ticker: 'CZKI3M Curncy', spot_ticker: 'CZKEUR Curncy', carry_ticker: 'CZKEURCR Curncy', weight_on_usd: 0, eur_usd_base: 'EUR', region: 'CEEMA'},
  {currency: 'HUF', implied_ticker: 'HUFI3M Curncy', spot_ticker: 'HUFEUR Curncy', carry_ticker: 'HUFEURCR Curncy', weight_on_usd: 0, eur_usd_base: 'EUR', region: 'CEEMA'},
  {currency: 'PLN', implied_ticker: 'PLNI3M Curncy', spot_ticker: 'PLNEUR Curncy', carry_ticker: 'PLNEURCR Curncy', weight_on_usd: 0, eur_usd_base: 'EUR', region: 'CEEMA'},
  {currency: 'ZAR', implied_ticker: 'ZARI3M Curncy', spot_ticker: 'ZARUSD Curncy', carry_ticker: 'ZARUSDCR Curncy', weight_on_usd: 50, eur_usd_base: 'USD', region: 'CEEMA'},
  {currency: 'CNY', implied_ticker: 'CCNI3M Curncy', spot_ticker: 'CNYUSD Curncy', carry_ticker: 'CNYUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'Asia'},
  {currency: 'KRW', implied_ticker: 'KWNI3M Curncy', spot_ticker: 'KRWUSD Curncy', carry_ticker: 'KRWUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'Asia'},
  {currency: 'IDR', implied_ticker: 'IHNI3M Curncy', spot_ticker: 'IDRUSD Curncy', carry_ticker: 'IDRUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'Asia'},
  {currency: 'INR', implied_ticker: 'IRNI3M Curncy', spot_ticker: 'INRUSD Curncy', carry_ticker: 'INRUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'Asia'},
  {currency: 'PHP', implied_ticker: 'PPNI3M Curncy', spot_ticker: 'PHPUSD Curncy', carry_ticker: 'PHPUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'Asia'},
  {currency: 'THB', implied_ticker: 'THBI3M Curncy', spot_ticker: 'THBUSD Curncy', carry_ticker: 'THBUSDCR Curncy', weight_on_usd: 100, eur_usd_base: 'USD', region: 'Asia'}
];

var gridOptions = {
  columnDefs: [
    { headerName: 'Currency', field: 'currency' },
    { headerName: '3M Implied Ticker', field: 'implied_ticker' },
    { headerName: 'Spot Ticker', field: 'spot_ticker' },
    { headerName: 'Carry Ticker', field: 'carry_ticker' },
    { headerName: 'Weight on USD (%)', field: 'weight_on_usd' },
    { headerName: 'EUR/USD base', field: 'eur_usd_base' },
    { headerName: 'Region', field: 'region' }
  ],
  defaultColDef: {flex: 1, editable: true},
  rowData: rowData,
  rowSelection: 'multiple',
  animateRows: true,
};

// Create a row to add in the table
function createNewRowData() {
  var newData = {
    currency: 'currency',
    implied_ticker: 'implied ticker ',
    spot_ticker: 'spot ticker',
    carry_ticker: 'carry ticker',
    weight_on_usd: 'weight on usd',
    eur_usd_base: 'eur/usd base',
    region: 'region'
  };
  return newData;
}

// Clear the data from the table (clear all)
function clearData() {
  gridOptions.api.setRowData([]);
}

// Add a new line in the table => let the user to enter new asset
function onAddRow() {
    var newItem = createNewRowData();
    var res = gridOptions.api.updateRowData({add: [newItem]});
    printResult(res);
}

// Remove a row from the table
function onRemoveSelected() {
  var selectedData = gridOptions.api.getSelectedRows();
  var res = gridOptions.api.applyTransaction({ remove: selectedData });
  printResult(res);
}

// Get the data from AG grid table
function getDataFromTable(){

    var input_currency = [];
    var input_implied = [];
    var input_spot_ticker = [];
    var input_carry_ticker = [];
    var input_weight_usd = [];
    var input_usd_eur = [];
    var input_region = [];

    gridOptions.api.forEachNode(function(rowNode, index) {
        input_currency.push(rowNode.data.currency);
        input_implied.push(rowNode.data.implied_ticker);
        input_spot_ticker.push(rowNode.data.spot_ticker);
        input_carry_ticker.push(rowNode.data.carry_ticker);
        input_weight_usd.push(rowNode.data.weight_on_usd);
        input_usd_eur.push(rowNode.data.eur_usd_base);
        input_region.push(rowNode.data.region);
    });

    var json_data = JSON.stringify({"input_currency": input_currency,
                                    "input_implied": input_implied,
                                    "input_spot_ticker": input_spot_ticker,
                                    "input_carry_ticker": input_carry_ticker,
                                    "input_weight_usd": input_weight_usd,
                                    "input_usd_eur": input_usd_eur,
                                    "input_region": input_region});
    return json_data
}

$(function(){
	$('#contact-form-button-effect').click(function(){

	    var json_data = getDataFromTable();
        var form_data = $('form').serialize();

		$.ajax({
			url: 'received_data_effect_form',
			data: {form_data: form_data, json_data: json_data},
			type: 'POST',
			success: function(response){
				console.log(response);
				alert('The strategy has been run successfully!');
				window.location.href = "effect_dashboard";
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});


// wait for the document to be loaded, otherwise
// ag-Grid will not find the div in the document.
document.addEventListener('DOMContentLoaded', function () {
  var eGridDiv = document.querySelector('#myGrid');
  new agGrid.Grid(eGridDiv, gridOptions);
});