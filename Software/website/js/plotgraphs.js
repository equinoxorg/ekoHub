

function drawVisualization() {

          // collect sensor data formatted into JSON
          var results = {{ json_data|safe }};
          
          // 1.First Data table....
          var system = new google.visualization.DataTable();
          // need to have a title for each individual line/curve
          // we plot in the graph
          system.addColumn('datetime', 'Date');
          system.addColumn('number', 'voltage');
          system.addColumn('number', 'current');


          // 2.Second Data Table 
          var dataSet2 = new google.visualization.DataTable();
          dataSet2.addColumn('number', 'voltage');
          dataSet2.addColumn('number', 'current');
      
          // add row for every grouping of voltage and current readings
          for(var i = 0; i < results.length; i++){
            system.addRow([new Date(results[i].tdate), results[i].voltage,
            results[i].current]);

          }
          dataSet2.sort(0);

          var plot = new google.visualization.AnnotatedTimeLine(
            document.getElementById('timeline'));
          plot.draw(system, {'displayAnnotations': true, 
                                     'allowRedraw': false,
                                     'displayRangeSelector': true,
                                     'scaleType': 'allmaximized',
                                     'displayZoomButtons': true,
                                     'allValuesSuffix': 'A'
                                    });  
          
      }
      