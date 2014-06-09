function drawVisualization() {

          // collect sensor data formatted into JSON
          var results = {{ json_data|safe }};
          
          // 1.First Data table....
          var leftSolarPanel = new google.visualization.DataTable();
          // need to have a title for each individual line/curve
          // we plot in the graph
          leftSolarPanel.addColumn('datetime', 'Date');
          leftSolarPanel.addColumn('number', 'voltage');
          leftSolarPanel.addColumn('number', 'current');

          var rightSolarPanel = new google.visualization.DataTable();
          rightSolarPanel.addColumn('datetime', 'Date');
          rightSolarPanel.addColumn('number', 'voltage');
          rightSolarPanel.addColumn('number', 'current');

          var leftBattery = new google.visualization.DataTable();
          leftBattery.addColumn('datetime', 'Date');
          leftBattery.addColumn('number', 'voltage');
          leftBattery.addColumn('number', 'current');

          var rightBattery = new google.visualization.DataTable();
          rightBattery.addColumn('datetime', 'Date');
          rightBattery.addColumn('number', 'voltage');
          rightBattery.addColumn('number', 'current');

          var leftInverter = new google.visualization.DataTable();
          leftInverter.addColumn('datetime', 'Date');
          leftInverter.addColumn('number', 'voltage');
          leftInverter.addColumn('number', 'current');

          var rightInverter = new google.visualization.DataTable();
          rightInverter.addColumn('datetime', 'Date');
          rightInverter.addColumn('number', 'voltage');
          rightInverter.addColumn('number', 'current');

          // 2.Second Data Table 
          var dataSet2 = new google.visualization.DataTable();
          dataSet2.addColumn('number', 'voltage');
          dataSet2.addColumn('number', 'current');
      

          for(var i = 0; i < results.length; i++){
            leftSolarPanel.addRow([new Date(results[i].tdate), results[i].dc_voltage3,
            results[i].dc_current3]);

            rightSolarPanel.addRow([new Date(results[i].tdate), results[i].dc_voltage1,
            results[i].dc_current1]);

            leftBattery.addRow([new Date(results[i].tdate), results[i].dc_voltage4,
            results[i].dc_current4]);

            rightBattery.addRow([new Date(results[i].tdate), results[i].dc_voltage2,
            results[i].dc_current2]);

            leftInverter.addRow([new Date(results[i].tdate), results[i].ac_voltage2,
            results[i].ac_current2]);

            leftInverter.addRow([new Date(results[i].tdate), results[i].ac_voltage1,
            results[i].ac_current1]);


            /*document.write(results[i].tdate + ", " + results[i].ac_current1
              + " " + results[i].ac_current2 + "<br/>");
            dataSet2.addRow([results[i].ac_current1, results[i].ac_current2]); */ 
          }
          dataSet2.sort(0);

          var solarPanel1 = new google.visualization.AnnotatedTimeLine(
            document.getElementById('timeline'));
          solarPanel1.draw(leftSolarPanel, {'displayAnnotations': true, 
                                     'allowRedraw': false,
                                     'displayRangeSelector': true,
                                     'scaleType': 'allmaximized',
                                     'displayZoomButtons': true,
                                     'allValuesSuffix': 'A'
                                    });  
            

          /*var solarPanel2 = new google.visualization.AnnotatedTimeLine(
            document.getElementById('timeline2'));
          solarPanel2.draw(rightSolarPanel, {'displayAnnotations': true, 
                                     'allowRedraw': false,
                                     'displayRangeSelector': true,
                                     'scaleType': 'allmaximized',
                                     'displayZoomButtons': true,
                                    });  */

           /*
          var secondChart = new google.visualization.LineChart(document.getElementById('lineChart')); 


          secondChart.draw(dataSet2, {title: 'VI characteristic',
                            hAxis: {title: "Voltage(V)"},
                            vAxis: {title: "Current(mA)"},
                            pointSize: 5, 
                            colors: ['red','#004411']
          }); */
      }
      