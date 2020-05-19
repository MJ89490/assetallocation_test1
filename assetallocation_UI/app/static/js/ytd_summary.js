
YTD_SUMMARY = document.getElementById('ytd_summary');

function ytdSummary(sum_performance_ytd_fx, sum_performance_ytd_bonds, sum_performance_ytd_equities)
{

    xValue = [sum_performance_ytd_fx, sum_performance_ytd_bonds, sum_performance_ytd_equities];

    var trace1 = [{type: 'bar',
                   x: xValue,
                   text: xValue.map(String),
                   textposition: 'auto',
                   textfont: {color: 'black'},
                   hoverinfo: 'none',
                   marker: {color: '#00AEEF'},
                   y: ['FX', 'Bonds', 'Equities'],
                   orientation: 'h',
                  }];

    var layout = {font: {size: 9},
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
                          showticklabels: false},
                  width: 150,
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

    Plotly.newPlot(YTD_SUMMARY, trace1, layout, config);
}