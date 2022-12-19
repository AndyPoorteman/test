/* function functionA(){
    //using the Django context variable
    inner_js_var = {{django_var}};
  } */
  const datanpy = js_var_from_dj;
  //JSON.parse("{{data|escapejs}}");
  console.log(datanpy)
  console.log('daga',datanp);
    
  console.log('label',label);
  
  console.log(titre,'titre');
  //const chartist=JSON.parse("['myChart','myChart2','myChart3','myChart4']");
  const today = new Date()
  const yesterday = new Date(today)
  const last_month = new Date(today)
  const timi = today.getTime();
  const ts = () => Math.floor(timi / 1000);

  function secondsToHms(d) {
  d = Number(d);
  var h = Math.floor(d / 3600);
  var m = Math.floor(d % 3600 / 60);
  var s = Math.floor(d % 3600 % 60);

  var hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " hours, ") : "";
  var mDisplay = m > 0 ? m + (m == 1 ? " minute, " : " minutes, ") : "";
  var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";
  return hDisplay + mDisplay + sDisplay; 
}
  yesterday.setDate(yesterday.getDate() - 1)
  last_month.setDate(last_month.getDate() - 30)
  
  console.log(timi);
  console.log(last_month.toDateString());
  console.log(yesterday.toDateString());
const data = {
labels: label[0],
datasets: [{
  label: titre[0],
  backgroundColor: 'rgb(0, 99, 132)',
  borderColor: 'rgb(0, 99, 132)',
  data: datanp[0],
}]
};

const config = {
type: 'line',
data: data,
options: {
  scales:{
    x: {
      type: 'time',
      time: {
        unit:'minute',
        min:yesterday.toDateString(), 
      }       
    },
    y:{
      beginAtZero: true,
      steps: 20,
      stepValue: 25,
      max: 500,
      title: {
        display: true,
        
    }
    },
    plugins:{
      legend:{
        labels:{
          boxWidth:0
        }
      }
    }
},
legend: {
  labels: {
    boxWidth: 0,
  }
}
}
};


const data2 = {
labels: label[1],
datasets: [{
  label: titre[1],
  backgroundColor: 'rgb(0, 99, 132)',
  borderColor: 'rgb(0, 99, 132)',
  data: datanp[1],
}]
};

const config2 = {
type: 'line',
data: data2,
options: {
  scales:{
    x: {
      type: 'time',
      time: {
        unit:'minute',
        min:yesterday.toDateString(),
        
      }       
    },
    y:{
      beginAtZero: true,
      steps: 20,
      stepValue: 25,
      max: 500
    }
  },
  plugins:{
    legend:{
      labels:{
        boxWidth:0
      }
    }
  }
  ,
  legend: {
    labels: {
      boxWidth: 0,
    }
  }
}
};
const data3 = {
labels: label[2],
datasets: [{
  label: titre[2],
  backgroundColor: 'rgb(0, 99, 132)',
  borderColor: 'rgb(0, 99, 132)',
  data: datanp[2],
}]
};

const config3 = {
type: 'line',
data: data3,
options: {
  scales:{
    x: {
      type: 'time',
      time: {
        unit:'minute',
        min:yesterday.toDateString(),
        
      }       
    },
    y:{
      beginAtZero: true,
      steps: 14,
      stepValue: 1,
      max: 14
    }
  },
  plugins:{
    legend:{
      labels:{
        boxWidth:0
      }
    }
  },
  legend: {
    labels: {
      boxWidth: 0,
    }
  }
}
};
const data4 = {
labels: label[3],
datasets: [{
  label: titre[3],
  backgroundColor: 'rgb(0, 99, 132)',
  borderColor: 'rgb(0, 99, 132)',
  data: datanp[3],
}]
};

const config4 = {
type: 'line',
data: data4,
options: {
  scales:{
    x: {
      type: 'time',
      time: {
        unit:'minute',
        min:yesterday.toDateString(),
        
      }       
    },
    y:{
      beginAtZero: true,
      steps: 75,
      stepValue: 1,
      max: 20
    }
  },
  plugins:{
    legend:{
      labels:{
        boxWidth:0
      }
    }
  },
         legend: {
           labels: {
             boxWidth: 0,
           }
         }
}
};


const myChart = new Chart(
document.getElementById('myChart'),
config
);
const myChart2 = new Chart(
document.getElementById('myChart2'),
config2
);

const myChart3 = new Chart(
document.getElementById('myChart3'),
config3
);

const myChart4 = new Chart(
document.getElementById('myChart4'),
config4
);


setInterval(addData, 10000);
 //setting the loop with time interval
 function addData() {
  $.ajax({
    method:'get',
    contentType:"applocation/json",
    url: "/hello-world/",
    dataType : "json",
    success: function(response){
      
      var labels=JSON.parse(response.labels);
      console.log(labels)
      //var labels2=response.labels.replaceAll( '[]', '');
      //console.log(labels2)
      //var labels3=response.labels.replaceAll('', '');
      //console.log(labels3)
      //const test =labels.split(',');
      //console.log(test);
      var datas=JSON.parse(response.datas);
      

      if (String(myChart.data.labels.slice(-1)) == labels[0]){
          console.log('same content');
          console.log('visua',String(myChart.data.labels.slice(-1)),' : ',labels[0]);
        }
        else{
          console.log('updating content',String(myChart.data.labels.slice(-1)),'to',String(labels[0]), 'with value : ',datas[0]);
          myChart.data.datasets[0].data.push(datas[0]);
          myChart.data.labels.push(labels[0]);
          myChart.update();
        };

        if (String(myChart2.data.labels.slice(-1)) == labels[1]){
          console.log('same content');
          console.log('visua',String(myChart2.data.labels.slice(-1)),' : ',labels[1]);
          }
          else{
          console.log('updating content',String(labels[1]),'to',String(myChart2.data.labels.slice(-1)), 'with value : ',datas[1]);
            
            myChart2.data.datasets[0].data.push(datas[1]);
            myChart2.data.labels.push(labels[1]);
            myChart2.update();
        };
        if (String(myChart3.data.labels.slice(-1)) == labels[2]){
          console.log('same content');
          console.log('visua',String(myChart3.data.labels.slice(-1)),' : ',labels[2]);
          }
          else{
            console.log('updating content',String(labels[2]),'to',String(myChart3.data.labels.slice(-1)), 'with value : ',datas[2]);
            
            myChart3.data.datasets[0].data.push(datas[2]);
            myChart3.data.labels.push(labels[2]);
            myChart3.update();
        };
        if (String(myChart4.data.labels.slice(-1)) == labels[3]){
          console.log('same content');
          console.log('visua',String(myChart4.data.labels.slice(-1)),' : ',labels[3]);
        }
        else{
          console.log('updating content',String(labels[3]),'to',String(myChart4.data.labels.slice(-1)), 'with value : ',datas[3]);
          
          myChart4.data.datasets[0].data.push(datas[3]);
          myChart4.data.labels.push(labels[3]);
          myChart4.update();
      };
        
 } 
});
}

function updateConfigAsNewObject(day_range) {
const today = new Date();
const min_date = new Date(today);
console.log(min_date);
min_date.setDate(min_date.getDate() - day_range);
console.log(min_date);

myChart.options = {
  responsive: true,
      scales: {
          x: {
            time: {
            unit:'hour',
            min:min_date.toDateString(),
            
          } ,
              display: true
          }
      }
  };
  myChart.update();

  myChart2.options = {responsive: true,
      scales: {
          x: {
            time: {
            unit:'hour',
            min:min_date.toDateString(),
            
          } ,
              display: true
          }
      }
  };
  myChart2.update();

  myChart3.options = {responsive: true,
      scales: {
          x: {
            time: {
            unit:'hour',
            min:min_date.toDateString(),
            
          } ,
              display: true
          }
      }
  };
  myChart3.update();
  myChart4.options = {responsive: true,
      scales: {
          x: {
            time: {
            unit:'hour',
            min:min_date.toDateString(),
            
          } ,
              display: true
          }
      }
  };
  myChart4.update();
}

function updateConfigAsObject() {
myChart.options = {responsive: true,
    scales: {
        x: {
          time: {
          unit:'hour',
          min:label[0][0]
          
        } ,
            display: true
        }
    }
};
myChart.update();


myChart2.options = {responsive: true,
scales: {
    x: {
      time: {
      unit:'hour',
      min:label[1][0]
      
    } ,
        display: true
    }
}
};
myChart2.update();


myChart3.options = {responsive: true,
scales: {
    x: {
      time: {
      unit:'hour',
      min:label[2][0],
      
    } ,
        display: true
    }
  }
};
myChart3.update();

myChart4.options = {responsive: true,
scales: {
    x: {
      time: {
      unit:'hour',
      min:label[3][0]
      
    } ,
        display: true
    }
}
};
myChart4.update();
}


