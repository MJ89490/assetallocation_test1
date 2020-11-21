REGION_LINE_CHART = document.getElementById('region_line_chart_effect');

function region_line_chart(latam_data, ceema_data, asia_data, total_data, average_data, region_dates)
{
    var trace1 = {  x:region_dates,
                    y: latam_data,
                    mode: 'lines',
                    name: 'LatAm',
                    line: {color:'#005774'}
                 };

    var trace2 = {  x:region_dates,
                    y: ceema_data,
                    mode: 'lines',
                    name: 'CEEMA',
                    line: {color: 'rgb(102, 204, 238)'}
                 };

    var trace3 = {  x:region_dates,
                    y: asia_data,
                    mode: 'lines',
                    name: 'Asia',
                    line: {color: 'rgb(17, 119, 153)'}
                 };

    var trace4 = {  x:region_dates,
                    y: total_data,
                    mode: 'lines',
                    name: 'Total',
                    line: {color: 'rgb(0, 128, 64)'}
                 };

    var trace5 = {  x:region_dates,
                    y: average_data,
                    mode: 'lines',
                    name: 'Average',
                    line: {color: 'rgb(255, 192, 0)', dash: 'dot'}
                 };

    var data = [trace1, trace2, trace3, trace4, trace5];

    var layout = {showlegend: true,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  margin: { l: 'auto', r: 0, b: 0, t: 25, pad: 4 },
                  xaxis: {tickfont: {size: 14, color: 'rgb(107, 107, 107)'}, color: 'rgb(107, 107, 107)'},
                  yaxis: {title: 'net positions',  titlefont: {size: 12, color: 'lightgrey'}}
                 };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(REGION_LINE_CHART, data, layout, config);
}