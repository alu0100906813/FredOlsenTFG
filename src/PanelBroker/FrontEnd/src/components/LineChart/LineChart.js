
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

import { getTimeFromStringDate } from '../../utils/date';

import { capitalize } from '../../utils/string';

import './lineChart.css';

import { BiTime } from 'react-icons/bi';
import { MdOutlineSensors } from 'react-icons/md';

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
    const color = 'rgb(13,110,253)';
    return {
      labels : data.map(value => getTimeFromStringDate(value.time)),
      datasets : [{
        label: capitalize(props.name),
        data: data.map(value => value.value),
        fill: true,
        backgroundColor: color,
        borderColor: color,
        tension: 0.3,
      }]
    }
  }

  return (
    <>
      <Line data={parseData(props.data)}/>
      <div className='lastUpdateAndValue bg-primary'>
        <div><BiTime/> Last Update: {props.data.length ? getTimeFromStringDate(props.data[props.data.length - 1]['time']) : '--'}</div>
        <div><MdOutlineSensors/> Value: {props.data.length ? props.data[props.data.length - 1]['value'] : '--'}</div>
      </div>
    </>
  );

};

export default LineChart;