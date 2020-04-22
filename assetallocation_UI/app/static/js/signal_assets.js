
SIGNALS_ASSETS = document.getElementById('signals_assets');

function signalsAssets(signals_gbp, signals_cad, signals_aud, signals_eur, signals_jpy, signals_ca_bonds, signals_eu_bonds,
              signals_uk_bonds, signals_us_bonds, signals_hk_equities, signals_jp_equities, signals_eu_equities,
              signals_us_equities)
{
    var xValue = [  signals_gbp,
                    signals_cad,
                    signals_aud,
                    signals_eur,
                    signals_jpy,
                    signals_ca_bonds,
                    signals_eu_bonds,
                    signals_uk_bonds,
                    signals_us_bonds,
                    signals_hk_equities,
                    signals_jp_equities,
                    signals_eu_equities,
                    signals_us_equities,
                 ]

    var trace1 = [{ type: 'bar',
                    text: xValue.map(String),
                    textposition: 'auto',
                    hoverinfo: 'none',
                    textfont: {color: 'black'},
                    x: xValue,
                    marker: { color: 'rgb(0, 153, 204)' },
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
                    line: {color: 'grey'},
                    orientation: 'h',
                    }];

    var layout = {  font: {size: 12, family: 'Arial, serif'},
                    xaxis: {
                            autorange: true,
                            showgrid: false,
                            zeroline: false,
                            showline: false,
                            autotick: true,
                            ticks: '',
                            showticklabels: false
                           },
                    yaxis: {
                            autorange: true,
                            showgrid: false,
                            zeroline: false,
                            showline: false,
                            autotick: true,
                            ticks: '',
                            showticklabels: true,
                           },
                    width: 220,
                    height: 600,
                    margin: {l: 90, r: 0, b: 0, t: 5, pad: 2 }
                    };

    var config = { 'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(SIGNALS_ASSETS, trace1, layout, config);
};