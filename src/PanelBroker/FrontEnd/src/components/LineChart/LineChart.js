
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const LineChart = (props) => {

  const parseData = (data) => {
    return {
      labels : data.map(value => value.time),
      datasets : [{
        label: props.name,
        data: data.map(value => value.value)
      }]
    }
  }

  return <Line data={parseData(props.data)}/>;

};

export default LineChart;