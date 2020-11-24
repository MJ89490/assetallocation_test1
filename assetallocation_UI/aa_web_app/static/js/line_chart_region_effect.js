REGION_LINE_CHART = document.getElementById('region_line_chart_effect');

//function region_line_chart(latam_data, ceema_data, asia_data, total_data, average_data, region_dates)
function region_line_chart(data, dates)
{




//    var t = [[1, 2, 3], [2, 3, 4]]
    let zipped = data.map((x, i) => [x, dates[i]]);
    console.log(zipped[0][1]);

    var traces = data.map(function(y) {
                                                          return {
                                                            y: y,

                                                            mode: 'lines'
                                                          };
                                                        });

        var d = dates.map(function(y) {
                                                          return {
                                                            x: y,
                                                            mode: 'lines'
                                                          };
                                                        });


    var layout = {showlegend: true,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  xaxis: {tickfont: {size: 14, color: 'rgb(107, 107, 107)'}, color: 'rgb(107, 107, 107)'},
                  yaxis: {title: 'net positions',  titlefont: {size: 12, color: 'lightgrey'}},
                  margin: { l: 'auto', r: 0, b: 0, t: 0, pad: 4 }
                 };

    var config = {'displayModeBar': false, 'responsive': true };


    Plotly.plot(REGION_LINE_CHART, [], layout, config);

    traces.forEach(function(trace, i) {
                                        setTimeout(function() {
                                                                Plotly.addTraces(REGION_LINE_CHART, trace);

                                                                console.log(d[0]);

                                                              },

                                                              (i+1))

                                      });




}





//    var trace1 = {
//                    y: data,
//                    mode: 'lines',
//                    name: name_data,
//                    line: {color:'#005774'}
//                 };

//    var trace2 = {  x:region_dates,
//                    y: ceema_data,
//                    mode: 'lines',
//                    name: 'CEEMA',
//                    line: {color: 'rgb(102, 204, 238)'}
//                 };
//
//    var trace3 = {  x:region_dates,
//                    y: asia_data,
//                    mode: 'lines',
//                    name: 'Asia',
//                    line: {color: 'rgb(17, 119, 153)'}
//                 };
//
//    var trace4 = {  x:region_dates,
//                    y: total_data,
//                    mode: 'lines',
//                    name: 'Total',
//                    line: {color: 'rgb(0, 128, 64)'}
//                 };
//
//    var trace5 = {  x:region_dates,
//                    y: average_data,
//                    mode: 'lines',
//                    name: 'Average',
//                    line: {color: 'rgb(255, 192, 0)', dash: 'dot'}
//                 };

//    var data = [trace1, trace2, trace3, trace4, trace5];
//    var data = [trace1];
//
//    var layout = {showlegend: true,
//                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
//                  xaxis: {tickfont: {size: 14, color: 'rgb(107, 107, 107)'}, color: 'rgb(107, 107, 107)'},
//                  yaxis: {title: 'net positions',  titlefont: {size: 12, color: 'lightgrey'}},
//                  margin: { l: 'auto', r: 0, b: 0, t: 0, pad: 4 }
//                 };
//
//    var config = {'displayModeBar': false, 'responsive': true };
//
//    Plotly.newPlot(REGION_LINE_CHART, data, layout, config);
//}