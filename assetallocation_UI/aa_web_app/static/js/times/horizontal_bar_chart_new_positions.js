NEW_POSITIONS = document.getElementById('new_positions');

function newPositionsChart(new_positions, assets_names)
{
    var trace0 = {type: 'bar',
                  x: new_positions,
                  y: assets_names,
                  orientation: 'h',
                  marker:{color: 'rgb(26, 102, 128)'}
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {margin: {l: 100, t:0}};

    Plotly.newPlot(NEW_POSITIONS, data, layout, config);
}