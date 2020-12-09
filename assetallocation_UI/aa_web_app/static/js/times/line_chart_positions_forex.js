POSITIONS_FOREX = document.getElementById('positions_forex');

function positionsForex(forex, dates)
{
    var trace1 = {y: forex,
                  x: dates,
                  type: 'scatter'
                 };

    var data = [trace1];

    var layout = {title: 'Forex'.bold(),
                  titlefont: {color: '#007faa',family: 'Arial, serif'},
                  showlegend: false,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  yaxis: {tickformat: ',.3%'}
                 };

    var config = { 'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(POSITIONS_FOREX, data, layout, config);

}



