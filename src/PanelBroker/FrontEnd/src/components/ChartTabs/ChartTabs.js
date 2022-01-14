
import { useEffect, useState, useRef } from 'react';
import { GET } from '../../utils/ajax';

import Loading from '../Loading/Loading';

import { Row, Col } from 'react-bootstrap';

const SHIP_API = '/getAllMetrics';

const TIME_TO_RELOAD = 2000; // In seconds

const MAX_CHART_LENGTH = 10;

/*
 Para lograr hacer los intervalos se ha usado:
 https://codesandbox.io/s/3499qqr565?file=/src/index.js
*/

const ChartTabs = (props) => {

  const [data, setData] = useState(0);

  const savedCallback = useRef();

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
      if (newData[key]['value'] === undefined) {
        result.push(<Row>{createCharts(newData[key])}</Row>)
      } else {
        result.push(<Col>{key}</Col>);
      }
    }
    return result;
  }

  const getData = () => {
    GET(SHIP_API, { params : { ship : props.currentShip } }, (response) => {
      let newData = data ? Object.assign(data, {}) : {};
      parseData(newData, response.data);
      console.log(newData);
      setData(newData);
    });
  }

  useEffect(() => {
    savedCallback.current = getData;
  });

  useEffect(() => {
    const interval = setInterval(() => savedCallback.current(), TIME_TO_RELOAD);
    return (() => {
      clearInterval(interval);
    })
  }, []);

  if(!data) {
    return <Loading/>;
  } else {
    return null;
    //return createCharts(data);
  }

};

export default ChartTabs;