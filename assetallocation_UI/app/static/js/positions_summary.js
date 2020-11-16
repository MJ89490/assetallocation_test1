
POSITIONS_SUMMARY = document.getElementById('positions-summary');

function positionsSummary(sum_positions_fx, sum_positions_bonds, sum_positions_equities)
{
    var xValue = [sum_positions_fx,
                  sum_positions_bonds,
                  sum_positions_equities];

    var trace1 = [{type: 'bar',
                   text: xValue.map(String),
                   textposition: 'auto',
                   textfont: {color: 'black'},
                   hoverinfo: 'none',
                   x: xValue,
                   marker: { color: '#009F4B'},
                   y: ['FX', 'Bonds', 'Equities'],
                   orientation: 'h'}];

    var layout = {title:{text: 'Weekly'},
                   font: {size: 11},
                   xaxis: {autorange: true,
                           showgrid: false,
                           zeroline: false,
                           showline: false,
                           autotick: true,
                           ticks: '',
                           showticklabels: false},
                   yaxis: {autorange: true,
                           showgrid: false,
                           zeroline: false,
                           showline: false,
                           autotick: true,
                           ticks: '',
                           showticklabels: true},
                   width: 150,
                   height: 180,
                   margin: {l: 48, r: 0, b: 0, t: 20, pad: 4}};

    layout.title = {text: '',
                    font: {size: 11, color: 'black'},
                    y: 0.90,
                    xanchor: 'left',
                    yanchor: 'bottom'};

    var config = {'displayModeBar': false, 'responsive': true};

    Plotly.newPlot(POSITIONS_SUMMARY, trace1, layout, config);
}