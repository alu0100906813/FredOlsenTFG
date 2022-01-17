
import './ChartTabs.css'

import { useEffect, useState } from 'react';

import Loading from '../Loading/Loading';

import { Row, Col } from 'react-bootstrap';
import LineChart from '../LineChart/LineChart';

import { capitalize } from '../../utils/string';

import socketIOClient from "socket.io-client";

const ENDPOINT = "http://127.0.0.1:5000";

const MAX_CHART_LENGTH = 10;

/*
 Para lograr hacer los intervalos se ha usado:
 https://codesandbox.io/s/3499qqr565?file=/src/index.js
*/

const ChartTabs = (props) => {

  const [data, setData] = useState();

  const [iter, setIter] = useState(0);

  const parseData = (recivedData, currentData) => {
    for (const key in recivedData) {
      if (recivedData[key]['value'] === undefined) {
        if(currentData[key] === undefined) {
          currentData[key] = {};
        }
        parseData(currentData[key], recivedData[key]);
      } else {
        if (currentData[key] === undefined) {
          currentData[key] = [];
        }
        currentData[key].push(recivedData[key])
        if(currentData[key].length > MAX_CHART_LENGTH) {
          currentData[key].shift();
        }
      }
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
              <LineChart name={key} data={newData[key]} onRefresh={(chart) => getNewValues(key, chart)}/>
            </>
          </Col>
        );
      }
    }
    return result;
  }

  const getNewValues = (topicName, chart) => {
    // FALTA POR IMPLEMENTAR
    const now = Date.now();
    chart.data.datasets.forEach(dataset => {
      dataset.data.push({
        x: now,
        y: 20
      });
    });
  }


  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    socket.on(props.currentShip , data => {
      setData(oldData => parseData(data, oldData ? oldData : {}));
      //setIter(iter => iter + 1); /* Soluciona un error, que el estado setData no actualiza (Hay que revisarlo)*/
    });
  }, []);


  if(!data) {
    return <Loading/>;
  } else {
    return createCharts(data);
  }

};

export default ChartTabs;