
import './ChartTabs.css'

import { useEffect, useState } from 'react';
import { GET } from '../../utils/ajax';

import Loading from '../Loading/Loading';

import { Row, Col } from 'react-bootstrap';
import LineChart from '../LineChart/LineChart';

import { capitalize } from '../../utils/string';

const SHIP_API = '/getAllMetrics';

const TIME_TO_RELOAD = 2000; // In seconds

const MAX_CHART_LENGTH = 10;

/*
 Para lograr hacer los intervalos se ha usado:
 https://codesandbox.io/s/3499qqr565?file=/src/index.js
*/

const ChartTabs = (props) => {

  const [data, setData] = useState();

  const [iter, setIter] = useState(0);

  const parseData = (currentData, recivedData) => {
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
              <LineChart name={key} data={newData[key]}/>
            </>
          </Col>
        );
      }
    }
    return result;
  }


  const getData = (response, newData) => {
    parseData(newData, response.data);
    return newData;
  }

  useEffect(() => {
    const interval = setInterval(() => {
      GET(SHIP_API, { params : { ship : props.currentShip } }, (response) => {
        setData(oldData => { return getData(response, oldData ? oldData : {}) });
        setIter(iter => iter + 1);
      });
    }, TIME_TO_RELOAD);
    return (() => {
      clearInterval(interval);
    });
  }, []);

  if(!data) {
    return <Loading/>;
  } else {
    return createCharts(data);
  }

};

export default ChartTabs;