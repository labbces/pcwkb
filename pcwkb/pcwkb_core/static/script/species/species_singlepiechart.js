// script for making a lot of piecharts within a specie

console.log(scientificName);
console.log(biomass_composition);
const PLOT = document.getElementById('grafico');
console.log(PLOT)
if (PLOT) {

  var layout = {
    height: 400,
    width: 400,
  }

  for (var part in biomass_composition) {
    console.log(part)
    var values = [];
    var labels = [];
    for (var component in biomass_composition[part]) {
      console.log(component,biomass_composition[part][component])
      labels.push(component);
      values.push(biomass_composition[part][component]);
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