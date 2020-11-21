DRAWDOWN_LINE_CHART = document.getElementById('drawdown_line_chart_effect');

function drawdown_line_chart(drawdown_no_signals, drawdown_with_signals)
{
    var trace1 = {
                    y: drawdown_no_signals,
                    mode: 'lines',
                    name: 'All EM FX',
                    line: {color:'#005774'}
                 };

    var trace2 = {
                    y: drawdown_with_signals,
                    mode: 'lines',
                    name: 'L = 16, S = 4, r = 2%, Forward CPI, Incl shorts',
                    line: {color:'rgb(132, 224, 255)'}
                 };

    var data = [trace1, trace2];

    var layout = {showlegend: true,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  margin: { l: 'auto', r: 0, b: 0, t: 25, pad: 4 },
                  yaxis: {title: 'drawdown (%)',  titlefont: {size: 12, color: 'lightgrey'}, tickformat: ',.3%'},
                  xaxis: {titlefont: {size: 12, color: 'rgb(107, 107, 107)'}, color: 'rgb(107, 107, 107)'}
                 };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(DRAWDOWN_LINE_CHART, data, layout, config);
}