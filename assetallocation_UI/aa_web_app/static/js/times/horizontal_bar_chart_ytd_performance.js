YTD_PERFORMANCE = document.getElementById('ytd_performance');

function ytdPerformanceChart(ytd_performance)
{
    var trace0 = {type: 'bar',
                  x: ytd_performance,
                  orientation: 'h',
                  marker:{color: 'rgb(26, 102, 128)'}
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {title: 'YTD'.bold(),
                  titlefont: {color: '#007faa',
                              family: 'Arial, serif'},
                  yaxis: {showticklabels: false}
                 };

    Plotly.newPlot(YTD_PERFORMANCE, data, layout, config);
}