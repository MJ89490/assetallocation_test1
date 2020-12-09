POSITIONS_EQUITIES = document.getElementById('positions_equities');

function positionsEquities(equities, dates)
{
    var trace1 = {y: equities,
                  x: dates,
                  type: 'scatter'
                 };

    var data = [trace1];

    var layout = {title: 'Equities'.bold(),
                  titlefont: {color: '#007faa',family: 'Arial, serif'},
                  showlegend: false,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  yaxis: {tickformat: ',.3%'}
                 };

    var config = { 'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(POSITIONS_EQUITIES, data, layout, config);

}



