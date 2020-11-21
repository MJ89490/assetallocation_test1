VERTICAL_BAR_CHART = document.getElementById('vertical_bar_chart_effect');

function vertical_bar_chart(backtest, livetest, quarterly_backtest_dates, quarterly_live_dates, quarters_backtest,
                            quarters_live)
{

    var trace1 = {
      x: [quarterly_backtest_dates, quarters_backtest],
      y: backtest,
      name: 'Backtest performance',
      marker: {color: 'rgb(55, 83, 109)'},
      type: 'bar'
    };

    var trace2 = {
      x: [quarterly_live_dates, quarters_live],
      y: livetest,
      name: 'Live performance',
      marker: {color: 'rgb(255, 192, 0)'},
      type: 'bar'
    };

    var data = [trace1, trace2];

    var layout = {
      title: {text: 'Quarterly P&L', font: {color: 'lightgrey'}},
      xaxis: {tickfont: {size: 14, color: 'rgb(107, 107, 107)'}},
      yaxis: {title: 'MATR P&L contribution(quarterly)',
              titlefont: {size: 12, color: 'lightgrey'},
              tickfont: {size: 12},
              tickformat: ',.3%'},
      barmode: 'group',
      bargap: 0.15,
      bargroupgap: 0.1,
      legend:{xanchor:"center", yanchor:"top", y:-0.3, x:0.5}
    };

    var config = {'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(VERTICAL_BAR_CHART, data, layout, config);

}