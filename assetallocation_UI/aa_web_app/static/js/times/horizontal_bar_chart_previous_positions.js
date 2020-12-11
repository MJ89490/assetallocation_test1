PREV_POSITIONS = document.getElementById('previous_positions');

function previousPositionsChart(prev_positions)
{
    var trace0 = {type: 'bar',
                  x: prev_positions,
                  orientation: 'h',
                   marker:{color: 'rgb(26, 102, 128)'}
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {title: 'Previous'.bold(),
                  titlefont: {color: '#007faa',
                              family: 'Arial, serif'},
                  yaxis: {showticklabels: false}
                 };

    Plotly.newPlot(PREV_POSITIONS, data, layout, config);
}