NEW_POSITIONS = document.getElementById('new_positions');

function newPositionsChart(new_positions)
{
    var trace0 = {type: 'bar',
                  x: new_positions,
                  orientation: 'h',
                  marker:{color: 'rgb(26, 102, 128)'}
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {title: 'New'.bold(),
                  titlefont: {color: '#007faa',
                              family: 'Arial, serif'},
                  yaxis: {showticklabels: false}
                 };

    Plotly.newPlot(NEW_POSITIONS, data, layout, config);
}