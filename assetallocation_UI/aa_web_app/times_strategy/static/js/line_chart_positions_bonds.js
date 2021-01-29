POSITIONS_BONDS = document.getElementById('positions_bonds');

function positionsBonds(bonds, percentile_fifth, equities_ninety_five_percentile, dates)
{
    var trace1 = {y: bonds,
                  x: dates,
                  type: 'scatter',
                  name: 'Bonds'
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

    var layout = {showlegend: false,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  yaxis: {tickformat: ',.3%'},
                  margin: {t:0}
                 };

    var config = { 'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(POSITIONS_BONDS, data, layout, config);

}



