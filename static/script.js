
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
        chart.scrollbarX = new am4core.Scrollbar();
        
        
        // Create axes
        var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
        dateAxis.dataFields.category = "date";
        dateAxis.renderer.grid.template.location = 0;
        dateAxis.renderer.minGridDistance = 60;
        dateAxis.tooltip.disabled = true;
        
        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.renderer.minWidth = 50;
        valueAxis.min = 0;
        valueAxis.cursorTooltipEnabled = false;
        
        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries());
        series.sequencedInterpolation = true;
        series.dataFields.valueY = "ajout";
        series.dataFields.dateX = "date";
        series.tooltipText = "[{categoryX}: bold]+{valueY}[/]";
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
        
        series.columns.template.adapter.add("fill", function(fill, target) {
          return chart.colors.getIndex(target.dataItem.index);
        })
        
        
        // Cursor
        chart.cursor = new am4charts.XYCursor();
        chart.cursor.behavior = "panX";
        
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
    
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    
    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "cumul";
    series.dataFields.dateX = "date";
    series.tooltipText = "{cumul}"
    
    series.tooltip.pointerOrientation = "vertical";
    
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.snapToSeries = series;
    chart.cursor.xAxis = dateAxis;
    
    //chart.scrollbarY = new am4core.Scrollbar();
    chart.scrollbarX = new am4core.Scrollbar();
    
    }); // end am4core.ready()
}