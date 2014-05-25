import os
import cgi
import random
from google.appengine.ext import db
from dataFile import remoteSettings, electricalValues

import jinja2
import webapp2

 
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
 

 
class MainPage(webapp2.RequestHandler):
 
  def get(self):
    self.response.write("<html>")
    #template = JINJA_ENVIRONMENT.get_template('index.html')
    #self.response.write(template.render())
    
    for j in range(0, 10):
      electricalValues(v = random.randint(1, 10), i = random.randint(1, 10)).put()
    
    self.response.write("Most recent values: <br>")
    query = db.Query(electricalValues)
    query.order('-tdate')
    for temp in query.run(limit=5):
      self.response.write("voltage: " + str(temp.v) + ",current: " + str(temp.i) + "<br>")
    
    self.response.write("""
    <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Voltage', 'Current'],
          ['1',  100],
          ['2',  15],
          ['3',  20],
          ['4',  30]
        ]);



        var firstChart = new google.visualization.LineChart(document.getElementById('chart_div'));
        var secondChart = new google.visualization.LineChart(document.getElementById('second_chart'));
     
        
        firstChart.draw(data, {title: 'IV characteristic',
                          width: 500, height: 500,
                          hAxis: {title: "Voltage(V)"},
                          vAxis: {title: "Current(mA)"},
                          legend: {alignment: "center"},
                          lineWidth: 10
        });
        
       secondChart.draw(data, {title: 'VI characteristic',
                          width: 500, height: 500,
                          hAxis: {title: "Current(mA)"},
                          vAxis: {title: "Voltage(V)"},
                          legend: {alignment: "end"},
                          pointSize: 5, 
                          colors: ['red','#004411']
        });
      }
                          
     //google.setOnLoadCallback(drawChart);
    </script>
  </head>
  <body>
    <div id="chart_div"  style="width: 500px; height: 500px; float: right;"></div>
    <div id="second_chart" style="width: 500px; height: 500px; float: left;"></div>
  </body>
</html> """)
                        
    
 
 
 
class sensorParameters(webapp2.RequestHandler):
 
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('parametersPage.html')
    self.response.write(template.render())
 
  def post(self):
    self.response.write('<html><body>You wrote:<pre>')
    self.response.write('Remote Variables are:<br>')
    sampleTime = cgi.escape(self.request.get('SampleTime', '0'))
    watchdogTime = cgi.escape(self.request.get('WatchdogTime', '0'))
    noLines = cgi.escape(self.request.get('nolines', '0'))
    startOfDay = cgi.escape(self.request.get('startDay', '0'))
    self.response.write( sampleTime + '<br>')
    self.response.write( watchdogTime + '<br>')
    self.response.write( noLines + '<br>')
    self.response.write( startOfDay + '<br>')
    self.response.write( '<br>')
    self.response.write('</pre></body></html>')
 
 
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Parameters', sensorParameters),
], debug=True)

