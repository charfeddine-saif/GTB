

var myData = JSON.parse('{{ data|escapejs }}');
var data1 = new Array();
var data2 = new Array();
var data3 = new Array();
var all_data = new Array();
for(let i=0;i<myData[0].length;i++){
  data1[i] = (myData[0][i][0] + myData[0][i][1])/2
}
for(let i=0;i<myData[1].length;i++){
  data2[i] = (myData[1][i][0] + myData[1][i][1])/2
}
for(let i=0;i<myData[2].length;i++){
  data3[i] = (myData[2][i][0] + myData[2][i][1])/2
}

for(let i=0;i<myData[0].length;i++){
  all_data[i] = ( data1[i] + data1[i] + data1[i] ) / 3;
}
  console.log("ll",data1);
var ctx = document.getElementById('myChart1').getContext('2d');
var myChart1 = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["00h00", "01h00", "02h00","03:00", "04h00", "05h00","06h00", "07h00","08h00", "09h00", "10h00","11h00","12h00" ,"13h00","14h00", "15h00", "16h00","17h00","18h00", "19h00","20h00", "21h00", "22h00","23h00"],
        datasets: [{
            label:'',
            data: data1,
            backgroundColor: [
                'rgba(54, 162, 235, 0.8)',
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 2
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});




  
var ctx = document.getElementById('myChart2').getContext('2d');
var myChart2 = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["00h00", "01h00", "02h00","03h00", "04h00", "05h00","06h00", "07h00","08h00", "09h00", "10h00","11h00","12h00" ,"13h00","14h00", "15h00", "16h00","17h00","18:00", "19h00","20h00", "21h00", "22h00","23h00"],
        datasets: [{
            label:'',
            data: data2,
            backgroundColor: [
                'rgba(54, 162, 235, 0.8)',
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',

            ],
            borderWidth: 2
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});





  
var ctx = document.getElementById('myChart3').getContext('2d');
var myChart3 = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["00h00", "01h00", "02h00","03h00", "04h00", "05h00","06h00", "07h00","08h00", "09h00", "10h00","11h00","12:00" ,"13h00","14h00", "15h00", "16h00","17h00","18:00", "19h00","20h00", "21h00", "22h00","23h00"],        datasets: [{
            label:'',
            data: data3,
            backgroundColor: [
                'rgba(54, 162, 235, 0.8)',
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',

            ],
            borderWidth: 2
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
