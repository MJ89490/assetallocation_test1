
PERFORMANCE_AUD = document.getElementById('performance_aud');

function performanceAudChart(data)
{
    var trace1 = {
                    y: data,
                    mode: 'lines',
                    name: 'AUD',
                    line: {color: '#ED1C24'}
                 };

    var data = [trace1];

    var layout = {
                    title: 'Performance AUD'.bold(),
                    titlefont: {color: '#007faa'},
                    showlegend: true,
                    legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                    margin: { l: 'auto', r: 0, b: 0, t: 25, pad: 4 }
                 };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(PERFORMANCE_AUD, data, layout, config);
}