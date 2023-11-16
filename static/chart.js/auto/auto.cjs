const chartjs = require('chart.js');
const {Chart, registerables} = chartjs;

Chart.register(...registerables);

module.exports = Object.assign(Chart, chartjs);
