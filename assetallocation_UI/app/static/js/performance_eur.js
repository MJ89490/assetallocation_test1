
PERFORMANCE_EUR = document.getElementById('performance_eur');

function performanceEurChart(data)
{
    var trace1 = {
                    y: data,
                    mode: 'lines',
                    name: 'EUR',
                    line: {color: '#009F4B'}
                    };

    var data = [trace1];

    var layout = {
                    title: 'Performance EUR'.bold(),
                    titlefont: {color: '#007faa'},
                    showlegend: true,
                    legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                    margin: { l: 'auto', r: 0, b: 0, t: 25, pad: 4 }
                  };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(PERFORMANCE_EUR, data, layout, config);
}