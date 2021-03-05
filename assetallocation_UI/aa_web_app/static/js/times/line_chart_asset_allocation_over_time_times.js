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

    for (i = 0; i < traces.length; i++) {
        Object.assign(traces[i], dates[0]);
        Object.assign(traces[i], names[i]);
    }

    Plotly.plot(ASSET_ALLOCATION, [], layout, config);
    traces.forEach(function(trace, i) {setTimeout(function() {Plotly.addTraces(ASSET_ALLOCATION, trace);},(i+1))});






//    var trace1 = {
//                    y: positions,
//                    name: 'S&P 500',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(0, 153, 204)'
//                    }


//    var trace2 = {
//                    y: positions_eu_equities ,
//                    name: 'Eurostoxx',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(0, 170, 85)'
//                    };
//
//    var trace3 = {
//                    y: positions_jp_equities,
//                    name: 'Topix',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(255, 204, 0)'
//                 };
//
//    var trace4 = {
//                    y: positions_hk_equities,
//                    name: 'Hang-Seng',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(163, 163, 163)'
//                 };
//
//    var trace5 = {
//                    y: positions_us_bonds,
//                    name: 'Treasury bond',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: '#ED1C24'
//                };
//
//    var trace6 = {
//                    y: positions_uk_bonds,
//                    name: 'Gilt',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: '#007faa'
//                 };
//
//    var trace7 = {
//                    y: positions_eu_bonds,
//                    name: 'Bund',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(0, 153, 204)'
//                 };
//
//    var trace8 = {
//                    y: positions_ca_bonds,
//                    name: 'Russell 2000',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(102, 102, 102)'
//                 };
//
//    var trace9 = {
//                    y: positions_jpy,
//                    name: 'JPY',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(0, 102, 136)'
//                 };
//
//    var trace10 = {
//                    y: positions_eur,
//                    name: 'EUR',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(102, 204, 238)'
//                  };
//
//    var trace11 = {
//                    y: positions_aud,
//                    name: 'AUD',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(192, 0, 0)'
//                  };
//
//    var trace12 = {
//                    y: positions_cad,
//                    name: 'CAD',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(0, 170, 85)'
//                  };
//
//    var trace13 = {
//                    y: positions_gbp,
//                    name: 'GBP',
//                    fill: 'tozeroy',
//                    type: 'scatter',
//                    mode: 'none',
//                    fillcolor: 'rgb(255, 224, 102)'
//                  };



//    Plotly.newPlot(ASSET_ALLOCATION, data, layout, config);
}