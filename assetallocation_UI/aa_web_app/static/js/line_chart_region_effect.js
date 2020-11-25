REGION_LINE_CHART = document.getElementById('region_line_chart_effect');

function region_line_chart(data, dates, names)
{
    var traces = data.map(function(y) { return {y: y, mode: 'lines'}; });

    var dates = dates.map(function(x) { return {x: x}; });

    var names = names.map(function(n) { return {name: n}; });

    var line_average = [{color: 'rgb(255, 192, 0)', dash: 'dot'}];

    var line_average = line_average.map(function(l) { return {line: l}; });

    //  Add more colors later and use random choosing colors
    var colors = ['rgb(0, 87, 116)', 'rgb(102, 204, 238)', 'rgb(17, 119, 153)', 'rgb(0, 128, 64)'];
    var line_colors = colors.map(function(r) { return {line: {color: r}}; });

    var layout = {showlegend: true,
                  legend: { xanchor: 'center', y: -0.1, x: 0.5, orientation: 'h' },
                  xaxis: {tickfont: {size: 14, color: 'rgb(107, 107, 107)'}, color: 'rgb(107, 107, 107)'},
                  yaxis: {title: 'net positions',  titlefont: {size: 12, color: 'lightgrey'}},
                  margin: { l: 'auto', r: 0, b: 0, t: 0, pad: 4 }
                 };

    var config = {'displayModeBar': false, 'responsive': true };

    for (i = 0; i < traces.length; i++) {
        Object.assign(traces[i], dates[0]);
        Object.assign(traces[i], line_colors[i]);
         Object.assign(traces[i], names[i]);
         if (Object.values(names[i]) == "Average")
            {
                Object.assign(traces[i], line_average[0]);
            }
    }
    Plotly.plot(REGION_LINE_CHART, [], layout, config);
    traces.forEach(function(trace, i) {setTimeout(function() {Plotly.addTraces(REGION_LINE_CHART, trace);},(i+1))});
}