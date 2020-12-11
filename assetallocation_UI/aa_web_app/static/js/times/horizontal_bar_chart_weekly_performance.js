WEEKLY_PERFORMANCE = document.getElementById('weekly_performance');

function weeklyPerformanceChart(weekly_performance, assets_names)
{
    var trace0 = {type: 'bar',
                  x: weekly_performance,
                  y: assets_names,
                  orientation: 'h',
                  marker:{color: 'rgb(26, 102, 128)'}
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {title: 'Weekly'.bold(),
                  titlefont: {color: '#007faa',
                              family: 'Arial, serif'},
                   margin: {l: 100}
                 };

    Plotly.newPlot(WEEKLY_PERFORMANCE, data, layout, config);
}