
WEEKLY_SUMMARY = document.getElementById('weekly_summary');

function weeklySummary(sum_performance_weekly_fx, sum_performance_weekly_bonds, sum_performance_weekly_equities)
{
    var xValue = [sum_performance_weekly_fx, sum_performance_weekly_bonds, sum_performance_weekly_equities]

    var trace1 = [{type: 'bar',
                   x: xValue,
                   text: xValue.map(String),
                   textposition: 'auto',
                   textfont: {color: 'black'},
                   hoverinfo: 'none',
                   marker: {color: '#FFD503'},
                   y: ['FX', 'Bonds', 'Equities'],
                   orientation: 'h'}];

    var layout = {font:{size: 11},
                  xaxis:{autorange: true,
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
                          showticklabels: false},
                  width: 130,
                  height: 180,
                  margin: {l: 58, r: 0, b: 0, t: 20, pad: 4}
                  };

    layout.title = {text: '',
                    font: {size: 11, color: 'black'},
                    y: 0.90,
                    xanchor: 'left',
                    yanchor: 'bottom',
                   };

    var config = {'displayModeBar': false, 'responsive': true};

    Plotly.newPlot(WEEKLY_SUMMARY, trace1, layout, config);
}