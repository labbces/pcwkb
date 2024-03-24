// script for making a lot of piecharts within a specie

console.log(scientificName);
console.log(biomasscomp);
const PLOT = document.getElementById('grafico');
console.log(PLOT)

var layout = {
  title: "Biomass composition pie chart for <br> PO: " + PO,
};

for (var part in biomasscomp) {
  console.log(part)
  var values = [];
  var labels = [];
  for (var component in biomasscomp[part]) {
    console.log(component, biomasscomp[part][component])
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

var config = {responsive: true}

Plotly.newPlot(PLOT, data, layout, config);

console.log(layout)