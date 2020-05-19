
POSITIONS_ASSETS = document.getElementById('position_assets');

function positionsAssets(positions_gbp_overview, positions_cad_overview, positions_aud_overview, positions_eur_overview,
                          positions_jpy_overview, positions_ca_bonds_overview, positions_eu_bonds_overview,
                          positions_uk_bonds_overview, positions_us_bonds_overview, positions_hk_equities_overview,
                          positions_jp_equities_overview, positions_eu_equities_overview, positions_us_equities_overview)
{
    xValue = [positions_gbp_overview,
              positions_cad_overview,
              positions_aud_overview,
              positions_eur_overview,
              positions_jpy_overview,
              positions_ca_bonds_overview,
              positions_eu_bonds_overview,
              positions_uk_bonds_overview,
              positions_us_bonds_overview,
              positions_hk_equities_overview,
              positions_jp_equities_overview,
              positions_eu_equities_overview,
              positions_us_equities_overview]

    var trace1 = [{
                    type: 'bar',
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
                        'US Equities'
                        ],
                    orientation: 'h',
                    marker: {color: 'rgb(0, 170, 85)'}
                    }];

    var layout = {font: {size: 11},
                  xaxis: {autorange: true,
                          showgrid: false,
                          zeroline: false,
                          showline: false,
                          autotick: true,
                          ticks: '',
                          showticklabels: false },
                  yaxis: {autorange: true,
                          showgrid: false,
                          zeroline: false,
                          showline: false,
                          autotick: true,
                          ticks: '',
                          showticklabels: false },
                  width: 220,
                  height: 600,
                  margin: {l: 0, r: 30, b: 0, t: 5, pad: 2 }
                  };

    layout.title = {
                    text: '',
                    font: {size: 12, color: '#007faa', family: 'Arial, serif' },
                    x: 0.25,
                    y: 0.87,
                    xanchor: 'left',
                    yanchor: 'bottom',
                    };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(POSITIONS_ASSETS, trace1, layout, config);
}