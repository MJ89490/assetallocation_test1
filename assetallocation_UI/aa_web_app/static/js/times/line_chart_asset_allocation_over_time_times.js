ASSET_ALLOCATION = document.getElementById('asset_allocation_over_time');

function assetAllocationChart(positions, dates_pos, names_pos)
{
    var traces = positions.map(function(y) { return {y: y, mode: 'none', fill: 'tozeroy',  type: 'scatter'}; });

    var dates = dates_pos.map(function(x) { return {x: x}; });

    var names = names_pos.map(function(n) { return {name: n}; });

    var layout = {showlegend: true,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  margin: { t:0 }
                  };

    var config = { 'displayModeBar': false, 'responsive': true };


    var traces1 = positions.map(function(y) { return {y: y, mode: 'none', fill: 'tozeroy',  type: 'scatter'}; });

    for (i = 0; i < traces.length; i++) {
        Object.assign(traces[i], dates[0]);
        Object.assign(traces[i], names[i]);
    }

    Plotly.plot(ASSET_ALLOCATION, [], layout, config);
    traces.forEach(function(trace, i) {setTimeout(function() {Plotly.addTraces(ASSET_ALLOCATION, trace);},(i+1))});

}