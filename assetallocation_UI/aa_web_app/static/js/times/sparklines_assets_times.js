SPARKLINES_ASSETS = document.getElementById('sparklines_assets');

function sparklinesAssets(positions)
{
    var traces = positions.map(function(y) { return {y: y, mode: 'lines', fill: 'tozeroy',  type: 'scatter', xaxis: 'x', yaxis: 'y'}; });

    var layout = {showlegend: true,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  margin: { l: 'auto', r: 0, b: 0, t: 25, pad: 4 },

                 };
    console.log(positions);
    var config = { 'displayModeBar': false, 'responsive': true };

    Plotly.plot(SPARKLINES_ASSETS, [], layout, config);
    traces.forEach(function(trace, i) {setTimeout(function() {Plotly.addTraces(SPARKLINES_ASSETS, trace);},(i+1))});
}

var trace1 = {
  x: [1, 2, 3],
  y: [4, 5, 6],
  type: 'scatter'
};

var trace2 = {
  x: [20, 30, 40],
  y: [50, 60, 70],
  xaxis: 'x2',
  yaxis: 'y2',
  type: 'scatter'
};

var trace3 = {
  x: [300, 400, 500],
  y: [600, 700, 800],
  xaxis: 'x3',
  yaxis: 'y3',
  type: 'scatter'
};

var trace4 = {
  x: [4000, 5000, 6000],
  y: [7000, 8000, 9000],
  xaxis: 'x4',
  yaxis: 'y4',
  type: 'scatter'
};

var data = [trace1, trace2, trace3, trace4];

var layout = {
  grid: {rows: 2, columns: 2, pattern: 'independent'},
};

Plotly.newPlot('myDiv', data, layout);