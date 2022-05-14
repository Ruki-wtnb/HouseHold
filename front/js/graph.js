
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['2015年', '2016年', '2017年', '2018年'],
    datasets: [{
      label: 'Dataset 1',
      data: [4, 15, 12, 23],
    }, {
      label: 'Dataset 2',
      data: [10, 9, 3, 16],
    }, {
      label: 'Dataset 3',
      data: [12, 20, 14, 3],
    }]
  },
  options: {
    plugins: {
      colorschemes: {
        scheme: 'brewer.Paired12'
      }
    }
  }

});
