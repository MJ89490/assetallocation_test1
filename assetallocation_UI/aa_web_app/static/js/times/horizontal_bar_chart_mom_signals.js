MOM_SIGNALS = document.getElementById('mom_signals');

function momSignalsChart(mom_signals, assets_names)
{
    var trace0 = {type: 'bar',
                  x: mom_signals,
                  y: assets_names,
                  orientation: 'h',
                  marker:{color: 'rgb(26, 102, 128)'}
                 }

    var data = [trace0];

    var config = { 'displayModeBar': false, 'responsive': true };
    var layout = {margin: {l: 100, t:0}};

    Plotly.newPlot(MOM_SIGNALS, data, layout, config);
}