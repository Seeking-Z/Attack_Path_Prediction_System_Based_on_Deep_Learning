import {Chart, registerables} from 'chart.js';

Chart.register(...registerables);

export * from 'chart.js';
export default Chart;
