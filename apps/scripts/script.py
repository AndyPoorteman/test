from airium import Airium
a = Airium()
listing=input('nbr of graph : ')
# Generating HTML file
a("""{% extends "layouts/base.html" %}
{% load static %}
{% block title %} Dashboard {% endblock %} 

<!-- Specific CSS Plugins goes HERE  -->
{% block css_plugins %}
      <link rel="stylesheet" type="text/css" media="all" href="{% static 'assets/css/daterangepicker.css' %}" />

      <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.js"></script>

      <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.1/moment.min.js"></script>

      <script type="text/javascript" src="{% static 'assets/js/daterangepicker.js'%}"></script>
{% endblock css_plugins %}

<!-- Specific Page CSS goes HERE  -->
{% block stylesheets %}<style>
  h2 {text-align: center;};
  div.button{padding-bottom:10px;}
</style>{% endblock stylesheets %}

{% block content %}
  <div class="content-wrapper">
    <div class = "title">
      {% for flux in influx %}  
      {% if flux.client_id.id == userid  and flux.page == url_parameter %}               
        <h2>{{flux.site}}</h2>
      {% endif %} 
    {% endfor %}""")

a("""<div id="date_selector"style="white-space: nowrap;
        overflow-x: auto;
        padding-bottom:20px;">      
                    <input type="text" id="config-demo" class="form-control"
                    style="display: inline-block;width:35%">
                    <button onclick="updateConfigAsObject()"
                    style="display: inline-block;">Reset</button>
                  </center></div>
      </div>""")
for chart in range(int(listing)):
    if (chart%2)==0:
        a("""<div class="row">""")
    a("""   <div class="col-lg-6 grid-margin stretch-card">
                <div class="card">
                    <div class="card-body">
                        <canvas id="{}"></canvas>
                    </div>
                </div>
            </div>""".format("myChart"+str(chart+1)))
    if (chart%2)==0:
        a("""</div>""")

a("""{% endblock content %}
<!-- Specific JS Plugins goes HERE  -->
{% block js_plugins %}
<script src="https://cdn.jsdelivr.net/npm/chart.js/dist/chart.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
<script src="{% static "assets/vendors/bootstrap-datepicker/bootstrap-datepicker.min.js"%}"></script>
{% endblock js_plugins %}
<!-- Specific Page JS goes HERE  -->
{% block javascripts %}
              <script type="text/javascript"> 
                datanp = JSON.parse("{{data|escapejs}}");
                titre = JSON.parse("{{title|escapejs}}");
                label = JSON.parse("{{label|escapejs}}");
                symbols= JSON.parse("{{symbols|escapejs}}");
                var count = Object.keys(titre).length;
                limit = JSON.parse("{{limit|escapejs}}");          
              </script>""")
a("""<script src="{% static "assets/js/index_"""+ str(listing) +""".js" %}" type="text/javascript"></script>""")
a("""<script type="text/javascript" src="https://cdn.jsdelivr.net/jquery/latest/jquery.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css" />
<script src="{% static "assets/js/index_basic.js" %}" type="text/javascript"></script> 
""")
a("{% endblock javascripts %}")
# Casting the file to a string to extract the value
html = str(a)
# Casting the file to UTF-8 encoded bytes:
html_bytes = bytes(a)
file=open('/home/Bsens/jbkb-master/apps/apps/templates/home/index_'+str(listing)+'.html','w')

file.write(html)
file.close
file=open('/home/Bsens/jbkb-master/apps/staticfiles/assets/js/index_'+str(listing)+'.js','w')

b = Airium()
for e in range(int(listing)):
    d=e+1
    b("""const data"""+str(e)+""" = {
    labels: label["""+str(e)+"""],
    datasets: [{
    label: titre["""+str(e)+"""],
    backgroundColor: 'rgb(0, 99, 132)',
    borderColor: 'rgb(0, 99, 132)',
    tension : 0.3,
    data: datanp["""+str(e)+"""],
    }]
    };

    const config"""+str(e)+""" = {
    type: 'line',
    data: data"""+str(e)+""",
    options: { elements:{
    point:{
    }
    
    }
    ,padding: {
    top: 50
    },
    scales:{
        x: {
        type: 'time',
        time: {
            unit:'day',
            displayFormats: {
            hour: 'HH:mm',
            day: 'yyyy-MM-dd '
            }
        },ticks: {
            autoSkip: false,
            maxRotation:0,
            major: {
            enabled: true
            }
            ,        font: function(context) {
            if (context.tick && context.tick.major) {
                return {
                weight: 'bold',
                };
            }
            }
        }
        },
        y:{
        beginAtZero: true,
        steps: 20,
        stepValue: 25,
        max: limit["""+str(e)+"""][1],
        display: true,
            title: {
            display: true,
            text: symbols["""+str(e)+"""]
            }
        }
    },
    plugins:{
        zoom:{
        zoom:{
            wheel:{
            enabled:true
            }
        }
        },
        legend:{
        labels:{
            boxWidth:0
        }
        }
    }
    }
    };
    
    const myChart"""+str(d)+""" = new Chart(
  document.getElementById('myChart"""+str(d)+"""'),
  config"""+str(e)+"""
  );""")
b("""setInterval(addData, 10000);
 //setting the loop with time interval
 function addData() {
  $.ajax({
    method:'get',
    contentType:"application/json",
    url: "/hello-world/",
    dataType : "json",
    success: function(response){
      console.log(response)
      var labels=JSON.parse(response.labels);
      var datas=JSON.parse(response.datas);""")
for e in range(int(listing)):
    d=e+1
    b(""" if (String(myChart"""+str(d)+""".data.labels.slice(-1)) == labels["""+str(e)+"""]){
            console.log('same content');
            console.log('visua',String(myChart"""+str(d)+""".data.labels.slice(-1)),' : ',labels["""+str(e)+"""]);
            }
            else{
            console.log('updating content',String(myChart"""+str(d)+""".data.labels.slice(-1)),'to',String(labels["""+str(e)+"""]), 'with value : ',datas["""+str(e)+"""]);
            myChart1.data.datasets[0].data.push(datas["""+str(e)+"""]);
            myChart1.data.labels.push(labels["""+str(e)+"""]);
            myChart1.update();
            };""")
b("""}
    });}""")

b("""function updateConfigAsNewObject(day_range) {
const today = new Date();
const yesterday=new Date();
yesterday.setDate(today.getDate() - day_range);
let formatted_date = (yesterday.getFullYear()) + "-" + String(yesterday.getMonth() + 1).padStart(2, '0') + "-" + String(yesterday.getDate()).padStart(2, '0')""")
for e in range(int(listing)):
    d=e+1
    b("""
    myChart"""+str(d)+""".options.scales.x.min=formatted_date;
    if (day_range ==1){
  myChart"""+str(d)+""".options.scales.x.time.unit='hour';
  myChart"""+str(d)+""".options.scales.y.beginAtZero=false;
  myChart"""+str(d)+""".options.elements.point.radius=0;
  myChart"""+str(d)+""".options.elements.point.pointHoverRadius=12;
  myChart"""+str(d)+""".options.scales.y.min=(Math.min.apply(Math, Object.values(myChart"""+str(d)+""".data.datasets[0].data))-2);
  myChart"""+str(d)+""".options.scales.y.max=(Math.max.apply(Math, Object.values(myChart"""+str(d)+""".data.datasets[0].data))+2);
  }
  else
  {
    myChart"""+str(d)+""".options.scales.x.time.unit='day';
  myChart"""+str(d)+""".options.elements.point.radius=3;
  myChart"""+str(d)+""".options.elements.point.pointHoverRadius=6;
  }
  myChart"""+str(d)+""".update();""")

b("};")
  

b("""function updateConfigAsObject() {""")
for e in range(int(listing)):
    d=e+1
    b("""myChart"""+str(d)+""".options.scales.x.min=label["""+str(e)+"""][0]
        myChart"""+str(d)+""".update();""")
b("};")
b("""function updateLimit(label) {""")
for e in range(int(listing)):
    d=e+1
    b("""myChart"""+str(d)+""".options.scales.x.min=label[0]
    myChart"""+str(d)+""".options.scales.x.max=label[1]
    myChart"""+str(d)+""".update();""")
b("};")


js = str(b)
# Casting the file to UTF-8 encoded bytes:
js_bytes = bytes(b)
file.write(js)
file.close