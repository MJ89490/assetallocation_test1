HORIZONTAL_BAR_CHART = document.getElementById('horizontal_bar_chart_effect');

function horizontal_bar_chart(year_to_year_contrib, names_curr)
{

   var trace1 = {
                  type: 'bar',
                  x: year_to_year_contrib,
                  y: names_curr,
                  orientation: 'h',
                  line: {color: 'rgb(0, 128, 64)'}
                };

    var data = [trace1];

    var layout = {showlegend: false,
                  title: {text: 'Year-to-date contributions (scaled to MATR allocation)', font: {color: 'lightgrey'}},
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  margin: { l: 'auto', r: 0, b: 0, t: 25, pad: 4 },
                  xaxis: {tickformat: ',.0%'}
                 };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(HORIZONTAL_BAR_CHART, data, layout, config);
}