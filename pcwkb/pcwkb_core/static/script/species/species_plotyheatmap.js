const PLOT = document.getElementById('grafico');

var xValues = Array.from(new Set(Object.values(biomasscomp).flatMap(Object.keys)));

var yValues = Object.keys(biomasscomp);

var zValues = [];

console.log(biomasscomp[0]);

for (var part in biomasscomp) {
    console.log(part);
    var values = [];
    for (var component in biomasscomp[part]) {
      console.log(component,biomasscomp[part][component]);
      values.push(biomasscomp[part][component]);
    }
    zValues.push(values);
};

console.log(zValues);

var data = [{
  x: xValues, 
  y: yValues,
  z: zValues,
  type: 'heatmap',
  showscale: true,
  hoverinfo: 'x+y',
}];

var layout = {
  title: 'Plant components distribution',
  annotations: [],
  xaxis: {
    ticks: '',
    side: 'top',
    autosize: true
  },
  yaxis: {
    ticks: '',
    ticksuffix: ' ',
    automargin: true,
    autosize: true
  }
};

for ( var i = 0; i < yValues.length; i++ ) {
  for ( var j = 0; j < xValues.length; j++ ) {
    var currentValue = zValues[i][j]+"%";
    var result = {
      xref: 'x1',
      yref: 'y1',
      x: xValues[j],
      y: yValues[i],
      text: zValues[i][j]+"%",
      font: {
        family: 'Arial',
        size: 12,
        color: 'rgb(50, 171, 96)'
      },
      showarrow: false,
      font: {
        color: textColor = 'white'
      }
    };
    layout.annotations.push(result);
  }
}

Plotly.newPlot(PLOT, data, layout);
