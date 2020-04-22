
ASSET_ALLOCATION = document.getElementById('asset_allocation_over_times');

function assetAllocationChart(positions_us_equities, positions_eu_equities, positions_jp_equities, positions_hk_equities,
                             positions_us_bonds, positions_uk_bonds, positions_eu_bonds, positions_ca_bonds, positions_jpy,
                             positions_eur, positions_aud, positions_cad, positions_gbp)
{

    var trace1 = {
                    y: positions_us_equities,
                    name: 'S&P 500',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none',
                    fillcolor: 'rgba(0, 153, 204, 0.5)'
                    };

    var trace2 = {
                    y: positions_eu_equities ,
                    name: 'Eurostoxx',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                    };

    var trace3 = {
                    y: positions_jp_equities,
                    name: 'Topix',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                 };

    var trace4 = {
                    y: positions_hk_equities,
                    name: 'Hang-Seng',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                 };

    var trace5 = {
                    y: positions_us_bonds,
                    name: 'Treasury bond',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                };

    var trace6 = {
                    y: positions_uk_bonds,
                    name: 'Gilt',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                 };

    var trace7 = {
                    y: positions_eu_bonds,
                    name: 'Bund',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none',
                    fillcolor: 'rgba(0, 153, 204, 0.5)'
                 };

    var trace8 = {
                    y: positions_ca_bonds,
                    name: 'Russell 2000',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                 };

    var trace9 = {
                    y: positions_jpy,
                    name: 'JPY',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                 };

    var trace10 = {
                    y: positions_eur,
                    name: 'EUR',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                  };

    var trace11 = {
                    y: positions_aud,
                    name: 'AUD',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                  };

    var trace12 = {
                    y: positions_cad,
                    name: 'CAD',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                  };

    var trace13 = {
                    y: positions_gbp,
                    name: 'GBP',
                    fill: 'tozeroy',
                    type: 'scatter',
                    mode: 'none'
                  };

    var layout = {
                    title: 'Asset Allocation Over Times'.bold(),
                    titlefont: {color: '#007faa',family: 'Arial, serif'},
                    showlegend: true,
                    legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                    margin: { l: 'auto', r: 0, b: 0, t: 25, pad: 4 }
                 };

    var config = { 'displayModeBar': false, 'responsive': true }
    var data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12, trace13];
    Plotly.newPlot(ASSET_ALLOCATION, data, layout, config);
}