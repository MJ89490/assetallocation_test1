POSITIONS_BONDS = document.getElementById('positions_bonds');

function positionsBonds(bonds, dates)
{
    var trace1 = {y: bonds,
                  x: dates,
                  type: 'scatter'
                 };

    var data = [trace1];

    var layout = {title: 'Bonds'.bold(),
                  titlefont: {color: '#007faa',family: 'Arial, serif'},
                  showlegend: false,
                  legend: { xanchor: 'center', x: 0.5, orientation: 'h' },
                  yaxis: {tickformat: ',.3%'}
                 };

    var config = { 'displayModeBar': false, 'responsive': true };

    Plotly.newPlot(POSITIONS_BONDS, data, layout, config);

}



