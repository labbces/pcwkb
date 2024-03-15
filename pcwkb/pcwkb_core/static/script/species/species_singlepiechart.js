// script for making a lot of piecharts within a specie

console.log(scientificName);
console.log(biomasscomp);
const PLOT = document.getElementById('grafico');
console.log(PLOT)
if (PLOT) {

  var layout = {
    height: 400,
    width: 400,
  }

  for (var part in biomasscomp) {
    console.log(part)
    var values = [];
    var labels = [];
    for (var component in biomasscomp[part]) {
      console.log(component,biomasscomp[part][component])
      labels.push(component);
      values.push(biomasscomp[part][component]);
    }
  }
  
  var data = [{
    type: "pie",
    values: values,
    labels: labels,
    hoverinfo: "label+percent",
    textinfo: "label+percent",
    textposition: "outside",
    automargin: true,
    }]

  Plotly.newPlot(PLOT, data, layout);
}

console.log(layout)
console.log(pieChartData)