POSITIONS = document.getElementById('positions');

function positionsChart(positions, assets_names)
{
    var trace0 = {type: 'bar',
                  x: positions,
                  y: assets_names,
                  orientation: 'h',
                  marker: {color: 'rgb(26, 102, 128)',
                           opacity: 0.8,
                           line: {
                              color: 'rgb(26, 102, 128)',
                              width: 0.2
                              }
                           }
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {margin: {l: 180, t:0}};

    Plotly.newPlot(POSITIONS, data, layout, config);
}
