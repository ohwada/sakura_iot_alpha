/**
 * main.js
 * 2016-07-01 K.OHWADA
 */

var g_chart_temp_humi;
var g_chart_light_noise;
var g_chart_press;

var g_table_temp_humi;
var g_table_light_noise;
var g_table_press;

// chart options
var g_options_temp_humi = {
    vAxes: {
        0: { title: "Temperature (℃)", minValue: 0 },
        1: { title: "Humidity (%)", minValue: 0, maxValue: 100 }
    },
    series: {
        0: { targetAxisIndex:0 },
        1: { targetAxisIndex:1 }
    },
    legend: { position: 'top' },
    curveType: "function", 
    width: 900,
    height: 350,
    chartArea:{ left:70, top:50, width:750, height:250 },
}

var g_options_light_noise = {
    vAxes: {
        0: { title: "Light (Lux)", minValue: 0 },
        1: { title: "Noise", minValue: 0 }
    },
    series: {
        0: { targetAxisIndex:0 },
        1: { targetAxisIndex:1 }
    },
    legend: { position: 'top' },
    curveType: "function", 
    width: 900,
    height: 350,
    chartArea:{ left:70, top:50, width:750, height:250 },
}

var g_options_press = {
    vAxes: {
        0: { title: "Air Pressure (hPa)", minValue: 950 }
    },
    series: {
        0: { targetAxisIndex:0 }
    },
    legend: { position: 'top' },
    curveType: "function", 
    width: 900,
    height: 350,
    chartArea:{ left:70, top:50, width:750, height:250 },
}

// init
function init() {
    google.charts.load( 'current', {'packages':['corechart'], 'language': 'ja' });
    google.charts.setOnLoadCallback(startChart);
}
// startChart
function startChart() {
    initChart();
    drawChart();
}
// initChart
function initChart() {
    g_chart_temp_humi = new google.visualization.LineChart( 
        document.getElementById('chart_temp_humi') );
    g_chart_light_noise = new google.visualization.LineChart( 
        document.getElementById('chart_light_noise') );
    g_chart_press = new google.visualization.LineChart( 
        document.getElementById('chart_pressure') );
              
    g_table_temp_humi = new google.visualization.DataTable();
    g_table_temp_humi.addColumn('datetime', '');
    g_table_temp_humi.addColumn('number', "Temperature");
    g_table_temp_humi.addColumn('number', "Humidity");
    g_table_temp_humi.addRows( g_data_temp_humi )

    g_table_light_noise = new google.visualization.DataTable();
    g_table_light_noise.addColumn('datetime', '');
    g_table_light_noise.addColumn('number', "Light");
    g_table_light_noise.addColumn('number', "Noise");
    g_table_light_noise.addRows( g_data_light_noise )

    g_table_press = new google.visualization.DataTable();
    g_table_press.addColumn('datetime', '');
    g_table_press.addColumn('number', "Pressure");
    g_table_press.addRows( g_data_press )
}       
// drawChart
function drawChart() {
    g_chart_temp_humi.draw(
        g_table_temp_humi, g_options_temp_humi);
    g_chart_light_noise.draw(
        g_table_light_noise, g_options_light_noise);
    g_chart_press.draw(
        g_table_press, g_options_press);
}
