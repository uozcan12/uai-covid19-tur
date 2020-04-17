demo = {
    initPickColor: function(){
        $('.pick-class-label').click(function(){
            var new_class = $(this).attr('new-class');
            var old_class = $('#display-buttons').attr('data-class');
            var display_div = $('#display-buttons');
            if(display_div.length) {
            var display_buttons = display_div.find('.btn');
            display_buttons.removeClass(old_class);
            display_buttons.addClass(new_class);
            display_div.attr('data-class', new_class);
            }
        });
    },

    initDocChart: function(){
      chartColor = "#FFFFFF";

      // General configuration for the charts with Line gradientStroke
      gradientChartOptionsConfiguration = {
          maintainAspectRatio: false,
          legend: {
              display: false
          },
          tooltips: {
            bodySpacing: 4,
            mode:"nearest",
            intersect: 0,
            position:"nearest",
            xPadding:10,
            yPadding:10,
            caretPadding:10
          },
          responsive: true,
          scales: {
              yAxes: [{
                display:0,
                gridLines:0,
                ticks: {
                    display: false
                },
                gridLines: {
                    zeroLineColor: "transparent",
                    drawTicks: false,
                    display: false,
                    drawBorder: false
                }
              }],
              xAxes: [{
                display:0,
                gridLines:0,
                ticks: {
                    display: false
                },
                gridLines: {
                  zeroLineColor: "transparent",
                  drawTicks: false,
                  display: false,
                  drawBorder: false
                }
              }]
          },
          layout:{
            padding:{left:0,right:0,top:15,bottom:15}
          }
      };

      ctx = document.getElementById('lineChartExample').getContext("2d");

      gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
      gradientStroke.addColorStop(0, '#80b6f4');
      gradientStroke.addColorStop(1, chartColor);

      gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
      gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
      gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

      myChart = new Chart(ctx, {
          type: 'line',
          responsive: true,
          data: {
              labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
              datasets: [{
                  label: "Active Users",
                  borderColor: "#f96332",
                  pointBorderColor: "#FFF",
                  pointBackgroundColor: "#f96332",
                  pointBorderWidth: 2,
                  pointHoverRadius: 4,
                  pointHoverBorderWidth: 1,
                  pointRadius: 4,
                  fill: true,
                  backgroundColor: gradientFill,
                  borderWidth: 2,
                  data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
              }]
          },
          options: gradientChartOptionsConfiguration
      });
    },

    initDashboardPageCharts: function(){

      chartColor = "#FFFFFF";

      // General configuration for the charts with Line gradientStroke
      gradientChartOptionsConfiguration = {
          maintainAspectRatio: false,
          legend: {
              display: false
          },
          tooltips: {
            bodySpacing: 4,
            mode:"nearest",
            intersect: 0,
            position:"nearest",
            xPadding:10,
            yPadding:10,
            caretPadding:10
          },
          responsive: 1,
          scales: {
              yAxes: [{
                display:0,
                gridLines:0,
                ticks: {
                    display: false
                },
                gridLines: {
                    zeroLineColor: "transparent",
                    drawTicks: false,
                    display: false,
                    drawBorder: false
                }
              }],
              xAxes: [{
                display:0,
                gridLines:0,
                ticks: {
                    display: false
                },
                gridLines: {
                  zeroLineColor: "transparent",
                  drawTicks: false,
                  display: false,
                  drawBorder: false
                }
              }]
          },
          layout:{
            padding:{left:0,right:0,top:15,bottom:15}
          }
      };

      gradientChartOptionsConfigurationWithNumbersAndGrid = {
          maintainAspectRatio: false,
          legend: {
              display: false
          },
          tooltips: {
            bodySpacing: 4,
            mode:"nearest",
            intersect: 0,
            position:"nearest",
            xPadding:10,
            yPadding:10,
            caretPadding:10
          },
          responsive: true,
          scales: {
              yAxes: [{
                gridLines:0,
                gridLines: {
                    zeroLineColor: "transparent",
                    drawBorder: false
                }
              }],
              xAxes: [{
                display:0,
                gridLines:0,
                ticks: {
                    display: false
                },
                gridLines: {
                  zeroLineColor: "transparent",
                  drawTicks: false,
                  display: false,
                  drawBorder: false
                }
              }]
          },
          layout:{
            padding:{left:0,right:0,top:15,bottom:15}
          }
      };

      var ctx = document.getElementById('bigDashboardChart').getContext("2d");

      var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
      gradientStroke.addColorStop(0, '#80b6f4');
      gradientStroke.addColorStop(1, chartColor);

      var gradientFill = ctx.createLinearGradient(0, 200, 0, 50);
      gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
      gradientFill.addColorStop(1, "rgba(255, 255, 255, 0.24)");

      var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["11.03.2020", "12.03.2020", "13.03.2020", "14.05.2020",
              "15.03.2020", "16.03.2020", "17.03.2020", "18.03.2020",
              "19.03.2020", "20.03.2020", "21.03.2020", "22.03.2020",
              "23.03.2020", "24.03.2020", "25.03.2020", "26.03.2020",
              "27.03.2020", "28.03.2020", "29.03.2020", "30.03.2020",
              "31.03.2020", "01.04.2020", "02.04.2020", "03.04.2020",
              "04.04.2020", "05.04.2020", "06.04.2020", "07.04.2020",
              "08.04.2020", "09.04.2020", "10.04.2020", "11.04.2020",
              "12.04.2020", "13.04.2020", "14.04.2020", "15.04.2020"] ,
    datasets: [{
        data: [1, 0, 4, 1, 12, 29, 51, 93, 168, 311, 277, 289, 293, 343, 561,
          1196, 2069, 1704, 1815, 1610, 2704, 2148, 2456, 2786, 3013, 3135,
           3148, 3892, 4117, 4056, 4747, 5138, 4789, 4093, 4062, 4281],
        borderColor: chartColor,
        pointBorderColor: chartColor,
        label: "Günlük Vaka Sayısı",
        borderColor: "#3e95cd",
        fill: false
      }, {
        data: [1, 1, 5, 6, 18, 47, 98, 191, 359, 670, 947, 1236, 1529, 1872,
          2433, 3629, 5698, 7402, 9217, 10827, 13531, 15679, 18135, 20921,
          23934, 27069, 30217, 34109, 38226, 42282, 47029, 52167, 56956,
          61049, 65111, 69392],
        label: "Toplam Vaka Sayısı",
        borderColor: "#8e5ea2",
        fill: false
      }, {
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 0, 16, 28, 35, 57,
           81, 90, 82, 69, 302, 256, 284, 256, 264, 296, 281, 542, 481, 511,
           842, 875],
        label: "Günlük İyileşen Sayısı",
        borderColor: "#3cba9f",
        fill: false
      }, {
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 26, 42, 70, 105,
          162, 243, 333, 415, 484, 786, 1042, 1326, 1582, 1846, 2142, 2423,
          2965, 3446, 3957, 4799, 5674],
        label: "Toplam İyileşen Sayısı",
        borderColor: "#e8c3b9",
        fill: false
      }, {
        data: [0, 0, 0, 0, 0, 0, 1, 1, 2, 5, 12, 9, 7, 7, 15, 16, 17, 16, 23,
          37, 46, 63, 79, 69, 76, 73, 75, 76, 87, 96, 98, 95, 97, 98, 107, 115],
        label: "Günlük Vefat Sayısı",
        borderColor: "#c45850",
        fill: false
      },
      {
        data: [0, 0, 0, 0, 0, 0, 1, 1, 2, 5, 12, 9, 7, 7, 15, 16, 17, 16, 23,
          37, 46, 63, 79, 69, 76, 73, 75, 76, 87, 96, 98, 95, 97, 98, 107, 115],
        label: "Toplam Vefat Sayısı",
        borderColor: "#c368975",
        fill: false
      },
      {
        data: [0, 0, 0, 0, 0, 0, 0, 2015, 1981, 3656, 2953, 1741, 3672, 3952,
          5035, 7286, 7533, 7641, 9982, 11535, 15422, 14396, 18757, 16160,
          19664, 20065, 21400, 20023, 24900, 28578, 30864, 33170, 35720,
          34456, 33070, 34090],
        label: "Günlük Test Sayısı",
        borderColor: "#8bcd52",
        fill: false
      },
      {
        data: [0, 0, 0, 0, 0, 0, 8002, 10017, 11995, 15651, 18604, 20345,
          24017, 27969, 33004, 40290, 47823, 55464, 65446, 76981, 92403,
          106799, 125556, 141716, 161380, 181445, 202845, 222868, 247768,
          276338, 307210, 340380, 376100, 410556, 443626, 477716],
        label: "Toplam Test Sayısı",
        borderColor: "#FF7F50",
        fill: false
      }
    ]
  },
  options: {
    layout: {
        padding: {
            left: 20,
            right: 20,
            top: 0,
            bottom: 0
        }
    },
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: '#fff',
      titleFontColor: '#333',
      bodyFontColor: '#666',
      bodySpacing: 4,
      xPadding: 12,
      mode: "nearest",
      intersect: 0,
      position: "nearest"
    },
    legend: {
        position: "bottom",
        labels :{
          fontColor: "#FFFFFF",
        },
        fillStyle: "#FFF",
        display: true
    },
    scales: {
        yAxes: [{
            ticks: {
                fontColor: "rgba(255,255,255,0.4)",
                fontStyle: "bold",
                beginAtZero: true,
                maxTicksLimit: 5,
                padding: 10
            },
            gridLines: {
                drawTicks: true,
                drawBorder: false,
                display: true,
                color: "rgba(255,255,255,0.1)",
                zeroLineColor: "transparent"
            }

        }],
        xAxes: [{
            gridLines: {
                zeroLineColor: "transparent",
                display: false,

            },
            ticks: {
                padding: 10,
                fontColor: "rgba(255,255,255,0.4)",
                fontStyle: "bold"
            }
        }]
    }
}
  /*options: {
    title: {
      display: true,
      text: 'World population per region (in millions)'
    }
  }*/
});


      var cardStatsMiniLineColor = "#fff",
          cardStatsMiniDotColor = "#fff";

      ctx = document.getElementById('lineChartExample').getContext("2d");

      gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
      gradientStroke.addColorStop(0, '#80b6f4');
      gradientStroke.addColorStop(1, chartColor);

      gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
      gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
      gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

      myChart = new Chart(ctx, {
          type: 'line',
          responsive: true,
          data: {
              labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
              datasets: [{
                  label: "Active Users",
                  borderColor: "#f963f9633232",
                  pointBorderColor: "#FFF",
                  pointBackgroundColor: "#f96332",
                  pointBorderWidth: 2,
                  pointHoverRadius: 4,
                  pointHoverBorderWidth: 1,
                  pointRadius: 4,
                  fill: true,
                  backgroundColor: "gradientFill",
                  borderWidth: 2,
                  data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
              }]
          },
          options: gradientChartOptionsConfiguration
      });


      ctx = document.getElementById('lineChartExampleWithNumbersAndGrid').getContext("2d");

      gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
      gradientStroke.addColorStop(0, '#18ce0f');
      gradientStroke.addColorStop(1, chartColor);

      gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
      gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
      gradientFill.addColorStop(1, hexToRGB('#18ce0f',0.4));

      myChart = new Chart(ctx, {
          type: 'line',
          responsive: true,
          data: {
              labels: ["11.03.2020", "12.03.2020", "13.03.2020", "14.05.2020",
                "15.03.2020", "16.03.2020", "17.03.2020", "18.03.2020",
                "19.03.2020", "20.03.2020", "21.03.2020", "22.03.2020",
                "23.03.2020", "24.03.2020", "25.03.2020", "26.03.2020",
                "27.03.2020", "28.03.2020", "29.03.2020", "30.03.2020",
                "31.03.2020", "01.04.2020", "02.04.2020", "03.04.2020",
                "04.04.2020", "05.04.2020", "06.04.2020", "07.04.2020",
                "08.04.2020", "09.04.2020", "10.04.2020", "11.04.2020",
                "12.04.2020", "13.04.2020", "14.04.2020", "15.04.2020"],
              datasets: [{
                  label: "Email Stats",
                  borderColor: "#18ce0f",
                  pointBorderColor: "#FFF",
                  pointBackgroundColor: "#18ce0f",
                  pointBorderWidth: 2,
                  pointHoverRadius: 4,
                  pointHoverBorderWidth: 1,
                  pointRadius: 4,
                  fill: true,
                  backgroundColor: gradientFill,
                  borderWidth: 2,
                  data: [40, 500, 650, 700, 1200, 1250, 1300, 1900]
              }]
          },
          options: gradientChartOptionsConfigurationWithNumbersAndGrid
      });

      var e = document.getElementById("barChartSimpleGradientsNumbers").getContext("2d");

      gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
      gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
      gradientFill.addColorStop(1, hexToRGB('#2CA8FF', 0.6));

      var a =  {
        type : "bar",
        data : {
          labels : ["January","February","March","April","May","June","July","August","September","October","November","December"],
          datasets: [{
            label: "Active Countries",
            backgroundColor: gradientFill,
            borderColor: "#2CA8FF",
            pointBorderColor: "#FFF",
            pointBackgroundColor: "#2CA8FF",
            pointBorderWidth: 2,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 1,
            pointRadius: 4,
            fill: true,
            borderWidth: 1,
            data: [80,99,86,96,123,85,100,75,88,90,123,155]
          }]
        },
        options: {
            maintainAspectRatio: false,
            legend: {
                display: false
            },
            tooltips: {
              bodySpacing: 4,
              mode:"nearest",
              intersect: 0,
              position:"nearest",
              xPadding:10,
              yPadding:10,
              caretPadding:10
            },
            responsive: 1,
            scales: {
                yAxes: [{
                  gridLines:0,
                  gridLines: {
                      zeroLineColor: "transparent",
                      drawBorder: false
                  }
                }],
                xAxes: [{
                  display:0,
                  gridLines:0,
                  ticks: {
                      display: false
                  },
                  gridLines: {
                    zeroLineColor: "transparent",
                    drawTicks: false,
                    display: false,
                    drawBorder: false
                  }
                }]
            },
            layout:{
              padding:{left:0,right:0,top:15,bottom:15}
            }
        }
      };

      var viewsChart = new Chart(e,a);
    },

    initGoogleMaps: function(){
        var myLatlng = new google.maps.LatLng(40.748817, -73.985428);
        var mapOptions = {
          zoom: 13,
          center: myLatlng,
          scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
          styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}]
        };

        var map = new google.maps.Map(document.getElementById("map"), mapOptions);

        var marker = new google.maps.Marker({
            position: myLatlng,
            title:"Hello World!"
        });

        // To add the marker to the map, call setMap();
        marker.setMap(map);
    },

	showNotification: function(from, align){
    	color = 'primary';

    	$.notify({
        	icon: "now-ui-icons ui-1_bell-53",
        	message: "Welcome to <b>Now Ui Dashboard Pro</b> - a beautiful freebie for every web developer."

        },{
            type: color,
            timer: 8000,
            placement: {
                from: from,
                align: align
            }
        });
	}

};
