AGG_LINE_CHART = document.getElementById('aggregate_line_chart_effect');

function agg_line_chart(total_excl_signals, total_incl_signals, spot_incl_signals, spot_excl_signals, agg_dates)
{
    var trace1 = {  x: agg_dates,
                    y: total_excl_signals,
                    mode: 'lines',
                    name: 'Total Excl Signals',
                    line: {color:'#005774'}
                 };

    var trace2 = {  x: agg_dates,
                    y: total_incl_signals,
                    mode: 'lines',
                    name: 'Total Incl Signals',
                    line: {color: 'rgb(102, 204, 238)'}
                 };

    var trace3 = {  x: agg_dates,
                    y: spot_incl_signals,
                    mode: 'lines',
                    name: 'Spot Incl Signals',
                    line: {color: 'rgb(17, 119, 153)'}
                 };

    var trace4 = {  x: agg_dates,
                    y: spot_excl_signals,
                    mode: 'lines',
                    name: 'Spot Excl Signals',
                    line: {color:  'rgb(255, 204, 0)'}
                 };

    var data = [trace1, trace2, trace3, trace4];

    var layout = {showlegend: true,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  margin: { l: 'auto', r: 0, b: 0, t: 0, pad: 0 },
                  xaxis: {tickfont: {size: 14, color: 'rgb(107, 107, 107)'},  color: 'rgb(107, 107, 107)'}
                 };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(AGG_LINE_CHART, data, layout, config);
}