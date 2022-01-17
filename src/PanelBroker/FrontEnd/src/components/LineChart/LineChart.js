
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

import { useRef} from 'react';

import { Line } from 'react-chartjs-2';

import { BiTime } from 'react-icons/bi';
import { MdOutlineSensors } from 'react-icons/md';

import { getTimeFromStringDate } from '../../utils/date';

import { capitalize } from '../../utils/string';

import './lineChart.css';

import ChartStreaming from 'chartjs-plugin-streaming';
import 'chartjs-adapter-moment';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartStreaming
)


const LineChart = (props) => {

  const timeRef = useRef();
  const valueRef = useRef();

  const onRefresh = (chart) => {
    props.onRefresh(chart, timeRef, valueRef);
  }

  const options = {
    scales: {
      x: {
        type: 'realtime',
        realtime: {
          duration: 20000,
          refresh: 1000,
          delay: 2000,
          onRefresh : onRefresh
        }
      },
      y: {
        title: {
          display: true,
          text: 'Value'
        }
      }
    },
    interaction: {
      intersect: false
    }
  }

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
      <Line data={parseData(props.data)} options={options}/>
      <div className='lastUpdateAndValue bg-primary'>
        <div><BiTime/> Last Update: <span ref={timeRef}>--</span></div>
        <div><MdOutlineSensors/> Value: <span ref={valueRef}>--</span></div>
    </div>
    </>
  );

};

export default LineChart;