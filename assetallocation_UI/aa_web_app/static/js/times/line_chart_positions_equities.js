POSITIONS_EQUITIES = document.getElementById('positions_equities');

function positionsEquities(equities, percentile_fifth, equities_ninety_five_percentile, dates)
{
    var trace1 = {y: equities,
                  x: dates,
                  type: 'scatter',
                  name: 'Equities'
                 };

    var trace2 = {y: percentile_fifth,
                  x: dates,
                  type: 'scatter',
                  name: '5th percentile',
                  line: {dash: 'dot', width: 4, color: '#87CEFA'}
                 }

    var trace3 = {y: equities_ninety_five_percentile,
                  x: dates,
                  type: 'scatter',
                  name: '95th percentile',
                  line: {dash: 'dot', width: 4, color: '#87CEFA'}
                 }

    var data = [trace1, trace2, trace3];

    var layout = {title: 'Equities'.bold(),
                  titlefont: {color: '#007faa',family: 'Arial, serif'},
                  showlegend: false,
                  legend: { xanchor: 'center', x: 0.5, y: -0.2, orientation: 'h' },
                  yaxis: {tickformat: ',.3%'}
                 };

    var config = { 'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(POSITIONS_EQUITIES, data, layout, config);

}



