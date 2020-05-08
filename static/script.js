
function renderPredictionCharts(data){
    var data = JSON.parse(data)
    for(i in data) console.log(data[i])
    am4core.ready(function() {
        
      // Themes begin
      am4core.useTheme(am4themes_animated);
      // Themes end
      
      // Create chart instance
      var chart = am4core.create("prediction", am4charts.XYChart);
      chart.data = data;
      
      
      // Create axes
      var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.dataFields.category = "date";
      dateAxis.renderer.grid.template.location = 0;
      dateAxis.renderer.minGridDistance = 60;
      dateAxis.tooltip.disabled = true;
      dateAxis.renderer.grid.template.disabled = true;
      
      var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.renderer.minWidth = 50;
      valueAxis.min = 0;
      valueAxis.cursorTooltipEnabled = false;
      valueAxis.renderer.grid.template.disabled = true;
      
      // Create series
      var series = chart.series.push(new am4charts.ColumnSeries());
      series.sequencedInterpolation = true;
      series.dataFields.valueY = "ajout";
      series.dataFields.dateX = "date";
      series.tooltipText = '{dateX.formatDate("d MMM")}\nNouveau: [bold]+{ajout}[/]\n Cumul: [bold]{cumul}[/]';
      series.columns.template.strokeWidth = 0;
      
      series.tooltip.pointerOrientation = "vertical";
      
      series.columns.template.column.cornerRadiusTopLeft = 10;
      series.columns.template.column.cornerRadiusTopRight = 10;
      series.columns.template.column.fillOpacity = 0.8;
      
      // on hover, make corner radiuses bigger
      var hoverState = series.columns.template.column.states.create("hover");
      hoverState.properties.cornerRadiusTopLeft = 0;
      hoverState.properties.cornerRadiusTopRight = 0;
      hoverState.properties.fillOpacity = 1;
      
      /*series.columns.template.adapter.add("fill", function(fill, target) {
        return chart.colors.getIndex(target.dataItem.index);
      })*/
      
      
      // Cursor
      chart.cursor = new am4charts.XYCursor();
      //chart.cursor.xAxis = dateAxis;
      chart.cursor.behavior = "panX";
      chart.cursor.lineY.disabled = true;
      

      
    }); // end am4core.ready()
}





function renderEvolutionCharts(data){
    var data = JSON.parse(data)

    am4core.ready(function() {
    
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    var chart = am4core.create("evolution", am4charts.XYChart);

    chart.data = data;
    
    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 60;
    dateAxis.periodChangeDateFormats.setKey("day", "dd/MM");
    //dateAxis.renderer.labels.template.fontSize = 11;
    //dateAxis.tooltip.fontSize = 11;
    dateAxis.tooltipDateFormat = "dd MMM yyyy";
    dateAxis.renderer.grid.template.disabled = true;
    
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.cursorTooltipEnabled = false;
    valueAxis.renderer.grid.template.disabled = true;

    function createSeries(field, subfield, color, name) {
      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.valueY = field;
      series.dataFields.dateX = "date";
      //series.tooltipText = "{cumul}"
      series.tooltipText = name+": [b]{"+field+"}[/]  |  +{"+subfield+"}";
      series.tooltip.pointerOrientation = "vertical"
      series.name = name;

      //series.fontSize = 11;
      series.strokeWidth = 2;
      series.stroke = color;
      series.getStrokeFromObject = true;
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color(color);
      series.tooltip.label.fill = am4core.color("#000");
      //series.tooltip.fontSize = 11;
      series.sequencedInterpolation = true;
      series.fillOpacity = 0.2;
      series.fill = am4core.color(color);
      series.stroke = am4core.color(color);
      return series;
    }

    var series1 = createSeries("casesCumul", "casesAjout", "#007bff", "Confirmés");
    var series2 = createSeries("deathsCumul", "deathsAjout", "#a62d37", "Décès");
    var series3 = createSeries("recoveredCumul", "recoveredAjout", "#02733e", "Guérisons");


    
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.cursor.lineY.disabled = true;
    
    //chart.scrollbarY = new am4core.Scrollbar();
    //chart.scrollbarX = new am4core.Scrollbar();
    chart.legend = new am4charts.Legend();
    chart.cursor.behavior = "none";

    
    }); // end am4core.ready()
}






function renderComparisonCharts(data){
  var data = JSON.parse(data)

  am4core.ready(function() {
  
  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end
  
  var chart = am4core.create("comparaison", am4charts.XYChart);

  chart.data = data;
  
  // Create axes
  var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
  dateAxis.renderer.minGridDistance = 60;
  dateAxis.periodChangeDateFormats.setKey("day", "dd/MM");
  //dateAxis.renderer.labels.template.fontSize = 11;
  //dateAxis.tooltip.fontSize = 11;
  dateAxis.tooltipDateFormat = "dd MMM yyyy";
  dateAxis.renderer.grid.template.disabled = true;
  
  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
  valueAxis.cursorTooltipEnabled = false;
  valueAxis.renderer.grid.template.disabled = true;
  

  function createSeries(field, subfield, color, name) {
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = field;
    series.dataFields.dateX = "date";
    //series.tooltipText = "{cumul}"
    series.tooltipText = name+": [b]{"+field+"}[/]  |  +{"+subfield+"}";
    series.tooltip.pointerOrientation = "vertical"
    series.name = name;

    //series.fontSize = 11;
    series.strokeWidth = 2;
    series.stroke = color;
    series.getStrokeFromObject = true;
    series.tooltip.getFillFromObject = false;
    series.tooltip.background.fill = am4core.color(color);
    series.tooltip.label.fill = am4core.color("#000");
    //series.tooltip.fontSize = 11;
    series.sequencedInterpolation = true;
    series.fillOpacity = 0;
    series.fill = am4core.color(color);
    series.stroke = am4core.color(color);
    series.bullets.push(new am4charts.CircleBullet());
    return series;
  }

  var series1 = createSeries("cumul", "ajout", "#007bff", "Prédiction");
  var series2 = createSeries("obsvCumul", "obsvAjout", "#FCC404", "Réalité");


  
  chart.cursor = new am4charts.XYCursor();
  chart.cursor.xAxis = dateAxis;
  chart.cursor.lineY.disabled = true;
  
  //chart.scrollbarY = new am4core.Scrollbar();
  //chart.scrollbarX = new am4core.Scrollbar();
  chart.legend = new am4charts.Legend();
  chart.cursor.behavior = "none";

  
  }); // end am4core.ready()
}