
import './ChartTabs.css'

import { useEffect, useState } from 'react';

import Loading from '../Loading/Loading';

import { Row, Col } from 'react-bootstrap';
import LineChart from '../LineChart/LineChart';

import { capitalize } from '../../utils/string';
import { getTimeFromStringDate } from '../../utils/date';
import { truncDecimals } from '../../utils/number';

import socketIOClient from "socket.io-client";

/**
 * Contiene el punto donde se va a conectar el socket
 */
const ENDPOINT = ":5000";

/*
 Para lograr hacer los intervalos se ha usado:
 https://codesandbox.io/s/3499qqr565?file=/src/index.js
*/

/**
 * Separados entre los topics del MQTT
 * Recordemos que el MQTT solo puede mandar un topic por mensaje
 * Por lo tanto: S1/Bodega/Aceleracion/X
 * Vemos 4 tipos de variables separadas por "/"
 */
const TOPIC_SEPARATOR = '/';

/**
 * Contiene la página de gráficas que muestra las gráficas del barco seleccionado
 * @param {Object} props 
 * @returns 
 */
const ChartTabs = (props) => {

  const [data, setData] = useState();
  const [forceUpdate, setForceUpdate] = useState();

  const parsedRecivedData = (recivedData) => {
    if(Object.keys(recivedData).length === 0) {
      return recivedData;
    }
    let newData = {};
    const stringTopic = Object.keys(recivedData)[0];
    const arrayTopic = stringTopic.split(TOPIC_SEPARATOR);
    if(arrayTopic.length >= 3) {
      const arrayTopicLastItem = arrayTopic.pop();
      newData[arrayTopic.join(TOPIC_SEPARATOR)] = {};
      newData[arrayTopic.join(TOPIC_SEPARATOR)][arrayTopicLastItem] = recivedData[stringTopic];
    } else {
      newData = recivedData;
    }
    return newData;
  }

  const parseData = (recivedData, currentData) => {
    let needUpdate = false;
    for (const key in recivedData) {
      if (recivedData[key]['value'] === undefined) {
        if(currentData[key] === undefined) {
          currentData[key] = {};
        }
        parseData(recivedData[key], currentData[key]);
      } else {
        if (currentData[key] === undefined) {
          currentData[key] = [];
          needUpdate = true;
        }
        currentData[key].push(recivedData[key]);
      }
    }
    if (needUpdate) {
      setForceUpdate(lastForceUpdate => !lastForceUpdate);
    }
    return currentData;
  };
  
  const generateChartName = (topicName) => {
    let topics = topicName.split(TOPIC_SEPARATOR);
    if(topics.length >= 3) {
      return capitalize(topics.pop());
    }
    topics = topics.map(topic => capitalize(topic));
    return topics.join(" ");
  };

  const createCharts = (newData, topicName) => {
    let result = [];
    for (const key in newData) {
      if (!Array.isArray(newData[key])) {
        result.push(
          <Row key={key}>
            <h2 className="valueName bg-light">{generateChartName(topicName + key)}</h2>
            <Row>{createCharts(newData[key], key + '/')}</Row>
          </Row>
        )
      } else {
        result.push(
          <Col key={key} md={topicName ? 4 : 12}>
            <>
              <h2 className="valueName bg-light">{generateChartName(topicName + key)}</h2>
              <LineChart name={topicName + key} data={newData[key]} onRefresh={(chart, timeRef, valueRef) => getNewValues(topicName + key, chart, timeRef, valueRef)}/>
            </>
          </Col>
        );
      }
    }
    return result;
  }

  const getNewValues = (topicName, chart, timeRef, valueRef) => {
    const topics = topicName.split(TOPIC_SEPARATOR);
    let lastData;
    if(topics.length <= 2) {
      lastData = data[topicName].slice();
      data[topicName] = [];
    } else {
      const key = topics.pop();
      lastData = data[topics.join(TOPIC_SEPARATOR)];
      lastData = lastData[key].slice();
      data[topics.join(TOPIC_SEPARATOR)][key] = [];
    }
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
      const recivedData = parsedRecivedData(data);
      setData(oldData => parseData(recivedData, oldData ? oldData : {}));
    });
  }, []);


  if(!data) {
    return <Loading/>;
  } else {
    return createCharts(data, '');
  }

};

export default ChartTabs;