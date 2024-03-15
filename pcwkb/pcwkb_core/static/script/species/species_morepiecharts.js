// script for making a lot of piecharts within a specie

console.log(scientificName);
console.log(biomass_composition);
const PLOT = document.getElementById('grafico');
console.log(PLOT)
if (PLOT) {

  var pieChartData = [];      
  
  var row = 0;
  var column = 0;
  var cell_Counter = 0;

  var layout = {
    title: 'Plant components distribution',
    annotations: [],
    height: 400*(Math.ceil(Object.keys(biomass_composition).length/4)),
    width: 1200,
    showlegend: false,
    grid: { rows: Math.ceil(Object.keys(biomass_composition).length/4), columns: 4 }
  };

  for (var part in biomass_composition) {
    console.log(part)
    var values = [];
    var labels = [];
    for (var component in biomass_composition[part]) {
      console.log(component,biomass_composition[part][component])
      labels.push(component);
      values.push(biomass_composition[part][component]);
    }

    pieChartData.push({
      values: values,
      labels: labels,
      domain: { row: row, column: column },
      name: scientificName + ' - ' + part,
      hoverinfo: 'label+percent',
      hole: .7,
      type: 'pie',
      automargin: true
    });

    var annotation = {
    font: {
    size: 12
    },
    showarrow: false,
    text: part,
    x: 0.06 + (column * 0.3),
    y: 0.7 - (row * 0.35),
    };

    cell_Counter++;
    if (cell_Counter % 4 === 0) {
        row++;
        column = 0;
    } else {
        column++;
    }

    layout.annotations.push(annotation);
  }

  Plotly.newPlot(PLOT, pieChartData, layout);
}
console.log(layout)
console.log(pieChartData)