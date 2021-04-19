PREV_POSITIONS = document.getElementById('previous_positions');

function previousPositionsChart(prev_positions, assets_names)
{
    var trace0 = {type: 'bar',
                  x: prev_positions,
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
    var layout = {margin: {l: 100, t:0}};

    Plotly.newPlot(PREV_POSITIONS, data, layout, config);
}