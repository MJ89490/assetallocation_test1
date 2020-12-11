POSITIONS = document.getElementById('positions');

function positionsChart(positions)
{
    var trace0 = {type: 'bar',
                  x: positions,
                  orientation: 'h',
                  marker:{color: 'rgb(26, 102, 128)'}
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {title: 'Previous'.bold(),
                  titlefont: {color: '#007faa',
                              family: 'Arial, serif'}
                 };

    Plotly.newPlot(POSITIONS, data, layout, config);
}
