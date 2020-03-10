

trace1 = {
  fill: 'tozeroy',
  line: {
    color: 'rgba(255, 204, 0, 1)',
    width: 1
  },
  mode: 'lines',
  name: 'US Equities',
  type: 'scatter',
  y: {{ us_equities_sparklines }},
  xaxis: 'x',
  yaxis: 'y',
  fillcolor: 'rgba(255, 204, 0, 0.5)'
};

trace2 = {
  fill: 'tozeroy',
  line: {
    color: 'rgba(0, 153, 204, 1)',
    width: 1
  },
  mode: 'lines',
  name: 'EU Equities',
  type: 'scatter',
  y: {{ positions_eu_equities_sparklines }},
  xaxis: 'x2',
  yaxis: 'y2',
  fillcolor: 'rgba(0, 153, 204, 0.5)',
};

trace3 = {
  fill: 'tozeroy',
  line: {
    color: 'rgba(0, 170, 85, 1)',
    width: 1
  },
  mode: 'lines',
  name: 'JP Equities',
  type: 'scatter',
  y: {{ positions_jp_equities_sparklines }},
  xaxis: 'x3',
  yaxis: 'y3',
  fillcolor: 'rgba(0, 170, 85, 0.5)'
};

trace4 = {
  fill: 'tozeroy',
  line: {
    color: 'rgba(238, 34, 34, 1)',
    width: 1
  },
  mode: 'lines',
  name: 'HK Equities',
  type: 'scatter',
  y: {{ positions_hk_equities_sparklines }},
  xaxis: 'x4',
  yaxis: 'y4',
  fillcolor: 'rgba(238, 34, 34, 0.5)'
};

trace5 = {
  fill: 'tozeroy',
  line: {
    color: 'rgba(68, 84, 106, 1)',
    width: 1
  },
  mode: 'lines',
  name: 'US 10y Bonds',
  type: 'scatter',
  y: {{ positions_us_bonds_sparklines }},
  xaxis: 'x5',
  yaxis: 'y5',
  fillcolor: 'rgba(68, 84, 106, 0.5)'
};

trace6 = {
  fill: 'tozeroy',
  line: {
    color: 'rgba(163, 163, 163, 1)',
    width: 1
  },
  mode: 'lines',
  name: 'UK 10y Bonds',
  type: 'scatter',
  y: {{ positions_uk_bonds_sparklines }},
  xaxis: 'x6',
  yaxis: 'y6',
  fillcolor: 'rgba(163, 163, 163, 0.5)'
};

data = [trace1, trace2, trace3, trace4, trace5, trace6];

var config = {
          'displayModeBar': false,
          'responsive': true,
           };

layout = {
          showlegend: true,
          legend: { xanchor: 'center', y:0.40,  x: 0.5, orientation: 'h' },
          font: {family: 'Arial, serif'},
          height:430,
          width: 775,
          margin: {l: 10,
                   r: 0,
                   b: 0,
                   t: 80,
                   pad:4},
          xaxis: {
            type: 'linear',
            range: [0, 999],
            ticks: '',
            anchor: 'y',
            domain: [0, 1],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          yaxis: {
            type: 'linear',
            range: [-4.967737446105644, 10.299745285002633],
            ticks: '',
            anchor: 'x',
            domain: [0.9258333333333333, 1],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          xaxis2: {
            type: 'linear',
            range: [0, 999],
            ticks: '',
            anchor: 'y2',
            domain: [0, 1],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          xaxis3: {
            type: 'linear',
            range: [0, 999],
            ticks: '',
            anchor: 'y3',
            domain: [0, 1],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          xaxis4: {
            type: 'linear',
            range: [0, 999],
            ticks: '',
            anchor: 'y4',
            domain: [0, 1],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          xaxis5: {
            type: 'linear',
            range: [0, 999],
            ticks: '',
            anchor: 'y5',
            domain: [0, 1],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          xaxis6: {
            type: 'linear',
            range: [0, 999],
            ticks: '',
            anchor: 'y6',
            domain: [0, 1],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          yaxis2: {
            type: 'linear',
            range: [-5.458676464524098, 3.4985553364348685],
            ticks: '',
            anchor: 'x2',
            domain: [0.8416666666666667, 0.9158333333333334],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          yaxis3: {
            type: 'linear',
            range: [-8.876358909845749, 11.82745161707441],
            ticks: '',
            anchor: 'x3',
            domain: [0.7575000000000001, 0.8316666666666668],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false,
          },
          yaxis4: {
            type: 'linear',
            range: [-15.61598919694067, 2.5446814048727404],
            ticks: '',
            anchor: 'x4',
            domain: [0.6733333333333333, 0.7475],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          yaxis5: {
            type: 'linear',
            range: [-8.630730872223673, 4.805328993705582],
            ticks: '',
            anchor: 'x5',
            domain: [0.5891666666666666, 0.6633333333333333],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          },
          yaxis6: {
            type: 'linear',
            range: [-5.89974432058536, 6.58391660738584],
            ticks: '',
            anchor: 'x6',
            domain: [0.505, 0.5791666666666667],
            mirror: false,
            showgrid: false,
            showline: false,
            zeroline: false,
            autorange: true,
            showticklabels: false
          }
        };

        layout.title = {
                  text: '',
                  font: {
                    size: 12,
                    color: 'black'
                  },
                  y: 0.87,
                  xanchor: 'left',
                  yanchor: 'bottom',
                };

        Plotly.plot('positions-sparklines', { data: data, layout: layout, config: config});
