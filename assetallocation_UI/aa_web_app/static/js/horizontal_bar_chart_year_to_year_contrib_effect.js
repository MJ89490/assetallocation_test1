HORIZONTAL_BAR_CHART = document.getElementById('horizontal_bar_chart_effect');

function horizontal_bar_chart(year_to_year_contrib, year_to_date_contrib_sum_prod_total, names_curr)
{

   var trace1 = {
                  type: 'bar',
                  x: year_to_year_contrib,
                  y: names_curr,
                  name: 'Currency',
                  orientation: 'h',
                  marker: {color: '#005774'}
                };

   var trace2 = {
                  type: 'bar',
                  x: year_to_date_contrib_sum_prod_total,
                  y: ['Total'],
                  name: 'Total',
                  orientation: 'h',
                  marker: {color: 'rgb(192, 0, 0)'}
                };

    var data = [trace1, trace2];

    var layout = {showlegend: false,
                  title: {text: 'Year-to-date contributions (scaled to MATR allocation)', font: {color: 'lightgrey'}},
                  xaxis: {titlefont: {size: 12, color: 'rgb(107, 107, 107)'}, color: 'rgb(107, 107, 107)', tickformat: ',.3%'},
                   margin: { l: 'auto', r: 0, b: 25, t: 25, pad: 4 }
                 };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(HORIZONTAL_BAR_CHART, data, layout, config);
}