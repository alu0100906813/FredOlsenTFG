
import './ChartTabs.css'

import { useEffect, useState } from 'react';

import Loading from '../Loading/Loading';

import { Row, Col } from 'react-bootstrap';
import LineChart from '../LineChart/LineChart';

import { capitalize } from '../../utils/string';
import { getTimeFromStringDate } from '../../utils/date';
import { truncDecimals } from '../../utils/number';

import socketIOClient from "socket.io-client";

const ENDPOINT = "http://127.0.0.1:5000";

const MAX_CHART_LENGTH = 10;

/*
 Para lograr hacer los intervalos se ha usado:
 https://codesandbox.io/s/3499qqr565?file=/src/index.js
*/

const ChartTabs = (props) => {

  const [data, setData] = useState();
  const [forceUpdate, setForceUpdate] = useState();

  const parseData = (recivedData, currentData) => {
    let needUpdate = false;
    for (const key in recivedData) {
      if (recivedData[key]['value'] === undefined) {
        if(currentData[key] === undefined) {
          currentData[key] = {};
        }
        parseData(currentData[key], recivedData[key]);
      } else {
        if (currentData[key] === undefined) {
          currentData[key] = [];
          needUpdate = true;
        }
        currentData[key].push(recivedData[key])
        if(currentData[key].length > MAX_CHART_LENGTH) {
          currentData[key].shift();
        }
      }
    }
    if (needUpdate) {
      setForceUpdate(lastForceUpdate => !lastForceUpdate);
    }
    return currentData;
  };
  

  const createCharts = (newData) => {
    let result = [];
    for (const key in newData) {
      if (!Array.isArray(newData[key])) {
        result.push(
          <Row key={key}>
            <h2 className="valueName bg-light">{capitalize(key)}</h2>
            {createCharts(newData[key])}
          </Row>
        )
      } else {
        result.push(
          <Col key={key}>
            <>
              <h2 className="valueName bg-light">{capitalize(key)}</h2>
              <LineChart name={key} data={newData[key]} onRefresh={(chart, timeRef, valueRef) => getNewValues(key, chart, timeRef, valueRef)}/>
            </>
          </Col>
        );
      }
    }
    return result;
  }

  const getNewValues = (topicName, chart, timeRef, valueRef) => {
    const lastData = data[topicName].slice();
    data[topicName] = [];
    lastData.forEach(item => {
      const time = new Date(item.time);
      chart.data.datasets[0].data.push({
        x : time.getTime(),
        y : item.value
      });
      if(timeRef && valueRef) {
        timeRef.current.innerHTML = getTimeFromStringDate(time);
        valueRef.current.innerHTML = typeof item.value === 'number' ? truncDecimals(item.value) : item.value; 
      }
    })
  }


  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    socket.on(props.currentShip , data => {
      setData(oldData => parseData(data, oldData ? oldData : {}));
    });
  }, []);


  if(!data) {
    return <Loading/>;
  } else {
    return createCharts(data);
  }

};

export default ChartTabs;