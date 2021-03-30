YTD_PERFORMANCE = document.getElementById('ytd_performance');

function ytdPerformanceChart(ytd_performance, assets_names)
{
    var trace0 = {type: 'bar',
                  x: ytd_performance,
                  y: assets_names,
                  orientation: 'h',
                  marker:{color: 'rgb(26, 102, 128)'}
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {margin: {l: 100, t:0}};

    Plotly.newPlot(YTD_PERFORMANCE, data,  layout, config);
}