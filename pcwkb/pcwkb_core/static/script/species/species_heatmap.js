anychart.onDocumentReady(function () {

    // create data
    var testdata = []
    for (var part in biomasscomp) {
        for (var component in biomasscomp[part]){
            var row={}
            row['y']=part;
            row['x'] = component;
            row['heat'] = biomasscomp[part][component];
            row['custom_field'] = 'info';
        testdata.push(row)
        }
    }
    console.log(testdata)
    var data = [
      {y: "A", x: "2010", heat: 15, custom_field: "info 1"},
      {x: "2011", y: "A", heat: 17, custom_field: "info 2"},
      {x: "2012", y: "A", heat: 21, custom_field: "info 3"},
      {x: "2013", y: "A", heat: 23, custom_field: "info 4"},
      {x: "2010", y: "B", heat: 34, custom_field: "info 5"},
      {x: "2011", y: "B", heat: 33, custom_field: "info 6"},
      {x: "2012", y: "B", heat: 32, custom_field: "info 7"},
      {x: "2013", y: "B", heat: 30, custom_field: "info 8"},
      {x: "2010", y: "C", heat: 43, custom_field: "info 9"},
      {x: "2011", y: "C", heat: 42, custom_field: "info 10"},
      {x: "2012", y: "C", heat: 40, custom_field: "info 11"},
      {x: "2013", y: "C", heat: 38, custom_field: "info 12"},
      {x: "2010", y: "D", heat: 8, custom_field: "info 13"},
      {x: "2011", y: "D", heat: 8, custom_field: "info 14"},
      {x: "2012", y: "D", heat: 7, custom_field: "info 15"},
      {x: "2013", y: "D", heat: 8, custom_field: "info 16"}
    ];

    // create a chart and set the data
    var chart = anychart.heatMap(testdata);

    // enable HTML for labels
    chart.labels().useHtml(true);

    // configure labels
    chart.labels().format(function() {
      var heat = (this.heat);
      if (heat < 20)
        return "Low<br/>" + heat + "%";
      if (heat < 40)
        return "Medium<br/>" + heat + "%";
      if (heat >= 40)
        return "<span style='font-weight:bold'>High</span><br/>" +
               heat + "%";
    });

    // configure tooltips
    chart.tooltip().format(function() {
      var heat = (this.heat);
      if (heat < 20)
        return this.y + ": Low (" + heat + "%)\n\n" +
                        this.getData("custom_field");
      if (heat < 40)
        return this.y + ": Medium (" + heat + "%)\n\n" +
                        this.getData("custom_field");
      if (heat >= 40)
        return this.y + ": High (" + heat + "%)\n\n" +
                        this.getData("custom_field");
    });

    // set the chart title
    chart.title("Plant components distribution");

    // set the container id
    chart.container("grafico2");

    // initiate drawing the chart
    chart.draw();
});