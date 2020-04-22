
PERFORMANCE_CAD = document.getElementById('performance_cad');

function performanceCadChart(data)
{
    var trace1 = {
                    y: data,
                    mode: 'lines',
                    name: 'CAD',
                    line: {color: '#00AEEF'}
                    };

    var data = [trace1];

    var layout = {
                    title: 'Performance CAD'.bold(),
                    titlefont: {color: '#007faa', family: 'Arial, serif'},
                    font: {size: 12},
                    showlegend: true,
                    legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                    margin: { l: 'auto', r: 0, b: 0, t: 25, pad: 4 }
                   };

    var config = { 'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(PERFORMANCE_CAD, data, layout, config);
}