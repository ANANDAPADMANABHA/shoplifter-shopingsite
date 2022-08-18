/*
Template Name: Niche
Author: UXLiner
*/
$(function() {
    "use strict";

// Use Morris.Area instead of Morris.Line

// ======
// Yearly Earning Starts
// ======

var day_data = [
  {"elapsed": "2012", "Sales": 60, "Earning": 80},
  {"elapsed": "2013", "Sales": 100, "Earning": 130},
  {"elapsed": "2014", "Sales": 70, "Earning": 50},
  {"elapsed": "2015", "Sales": 80, "Earning": 155},
  {"elapsed": "2016", "Sales": 155, "Earning": 105},
  {"elapsed": "2017", "Sales": 120, "Earning": 110},
  {"elapsed": "2018", "Sales": 250, "Earning": 180}
];
Morris.Line({
  element: 'earning',
  data: day_data,
  xkey: 'elapsed',
  ykeys: ['Sales', 'Earning'],
  labels: ['Sales', 'Earning'],
  fillOpacity: 0,
  pointStrokeColors: ['#1976d2', '#26c6da'],
  behaveLikeLine: true,
  gridLineColor: '#e0e0e0',
  lineWidth: 3,
  hideHover: 'auto',
  lineColors: ['#5867dd', '#008cd3'],
  parseTime: false,
  resize: true
});

// ======
// Yearly Earning Ending
// ======

})(jQuery);