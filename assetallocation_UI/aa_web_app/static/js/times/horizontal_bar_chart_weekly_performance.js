WEEKLY_PERFORMANCE = document.getElementById('weekly_performance');

function weeklyPerformanceChart(weekly_performance, assets_names)
{
    var trace0 = {type: 'bar',
                  x: weekly_performance,
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

    Plotly.newPlot(WEEKLY_PERFORMANCE, data, layout, config);
}