
YTD_ASSETS = document.getElementById('ytd_assets');

function ytdAssets(performance_ytd_gbp, performance_ytd_cad, performance_ytd_aud, performance_ytd_eur, performance_ytd_jpy,
                   performance_ytd_ca_bonds, performance_ytd_eu_bonds, performance_ytd_uk_bonds, performance_ytd_us_bonds,
                   performance_ytd_hk_equities, performance_ytd_jp_equities, performance_ytd_eu_equities, performance_ytd_us_equities)
{
    xValue = [performance_ytd_gbp,
              performance_ytd_cad,
              performance_ytd_aud,
              performance_ytd_eur,
              performance_ytd_jpy,
              performance_ytd_ca_bonds,
              performance_ytd_eu_bonds,
              performance_ytd_uk_bonds,
              performance_ytd_us_bonds,
              performance_ytd_hk_equities,
              performance_ytd_jp_equities,
              performance_ytd_eu_equities,
              performance_ytd_us_equities]

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
                       'Eu 10y Bonds',
                       'UK 10y Bonds',
                       'US 10y Bonds',
                       'HK Equities',
                       'JP Equities',
                       'EU Equities',
                       'US Equities'],
                   orientation: 'h',
                    marker: {color: 'rgb(163, 163, 163)' }
                    }];

    var layout = {font: {size: 11, family: 'Arial, serif'},
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
                    margin: {l: 0, r: 30, b: 0, t: 5, pad: 2}
                    };

    layout.title = {text: '',
                    font: {size: 12, color: 'black'},
                    x: 0.25,
                    y: 0.87,
                    xanchor: 'left',
                    yanchor: 'bottom',
                    };

    var config = {'displayModeBar': false, 'responsive': true};

    Plotly.newPlot(YTD_ASSETS, trace1, layout, config);
}