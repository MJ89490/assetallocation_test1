MOM_SIGNALS = document.getElementById('mom_signals');

function momSignalsChart(mom_signals, assets_names)
{
    var trace1 = {x: mom_signals,
                  y: assets_names,
                  orientation: 'h',
                  type: 'bar',
                  textposition: 'none',
                  marker: {color: 'rgb(26, 102, 128)',
                           opacity: 0.8,
                           line: {
                              color: 'rgb(26, 102, 128)',
                              width: 0.2
                            }
                  }
    };

    var data = [trace1];

    var config = { 'displayModeBar': false, 'responsive': true };

    var layout = {barmode: 'stack', margin: {l: 180, t:0}};
    Plotly.newPlot(MOM_SIGNALS, data, layout, config);
}