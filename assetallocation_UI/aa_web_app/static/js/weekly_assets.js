
WEEKLY_ASSETS = document.getElementById('weekly_assets');

function weeklyAssets(performance_gbp_overview, performance_cad_overview, performance_aud_overview,
                      performance_eur_overview, performance_jpy_overview, performance_ca_bonds,
                      performance_eu_bonds, performance_uk_bonds, performance_us_bonds, performance_hk_equities,
                      performance_jp_equities, performance_eu_equities, performance_us_equities)
{
    xValue = [performance_gbp_overview,
              performance_cad_overview,
              performance_aud_overview,
              performance_eur_overview,
              performance_jpy_overview,
              performance_ca_bonds,
              performance_eu_bonds,
              performance_uk_bonds,
              performance_us_bonds,
              performance_hk_equities,
              performance_jp_equities,
              performance_eu_equities,
              performance_us_equities]

    var trace1 = [{type: 'bar',
                   x: xValue,
                   text: xValue.map(String),
                   textposition: 'auto',
                   textfont: {color: 'black'},
                   hoverinfo: 'none',
                   y: ['GBP',
                       'CAD',
                       'AUD',
                       'EUR',
                       'JPY',
                       'CA 10y Bonds',
                       'EU 10y Bonds',
                       'UK 10y Bonds',
                       'US 10y Bonds',
                       'HK Equities',
                       'JP Equities',
                       'EU Equities',
                       'US Equities'],
                    orientation: 'h',
                    marker: {color: 'rgb(255, 204, 0)' }}];

    var layout = {text: '',
                   font: {size: 11},
                   xaxis: {autorange: true,
                           showgrid: false,
                           zeroline: false,
                           showline: false,
                           autotick: true,
                           ticks: '',
                           showticklabels: false},
                    yaxis: {autorange: true,
                            showgrid: false,
                            zeroline: false,
                            showline: false,
                            autotick: true,
                            ticks: '',
                            showticklabels: false},
                    width: 220,
                    height: 600,
                    margin: {
                    l: 0, r: 30, b: 0, t: 5, pad: 4}
                   };

    layout.title = {text: '',
                    font: {size: 12, color: '#007faa', family: 'Arial, serif'},
                    x: 0.25,
                    y: 0.87,
                    xanchor: 'left',
                    yanchor: 'bottom',
                    };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(WEEKLY_ASSETS,  trace1, layout, config);
}