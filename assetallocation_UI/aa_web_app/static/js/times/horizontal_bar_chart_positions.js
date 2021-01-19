POSITIONS = document.getElementById('positions');

function positionsChart(positions, assets_names)
{
    var trace0 = {type: 'bar',
                  x: positions,
                  y: assets_names,
                  orientation: 'h',
                  marker:{color: 'rgb(26, 102, 128)'}
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {margin: {l: 100, t:0}};

    Plotly.newPlot(POSITIONS, data, layout, config);
}
