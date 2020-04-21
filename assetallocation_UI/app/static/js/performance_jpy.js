
PERFORMANCE_JPY = document.getElementById('performance_jpy');

function performanceJpyChart(data)
{
    var trace1 = {
                    y: data,
                    mode: 'lines',
                    name: 'JPY',
                    line: {color: '#FFD503'}
                 };

    var data = [trace1];

    var layout = {
                    title: 'Performance JPY'.bold(),
                    titlefont: {color: '#007faa'},
                    showlegend: true,
                    legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                    margin: { l: 'auto', r: 0, b: 0, t: 25, pad: 4 }
                };

    var config = { 'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(PERFORMANCE_JPY, data, layout, config);
}