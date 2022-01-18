
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
 * @param {Object} props Propiedades del componente
 * - currentShip: El barco actual donde queremos ver las gráficas
 * @returns {JSX} Componente renderizado
 */
const ChartTabs = (props) => {

  /**
   * Contiene los datos que se va a mostrar en las gráficas
   * Estos se van vaciando según se van mostrando los valores en la gráfica
   * Y se van llenando a través de un socket conectado al backend
   */
  const [data, setData] = useState();

  /**
   * Al actualizar el estado anterior Data, con el setData este no renderiza el componente
   * Tampoco queremos que haga esto, porque si no, no muestra correctamente las gráficas
   * Para ello, forzamos el renderizado utilizando este estado que es como un comodin
   * Es necesario actualizar cuando llega del backend datos de un sensor que no estaba registrado previamente
   * porque si no, no se genera la gráfica
   */
  const [forceUpdate, setForceUpdate] = useState();

  /**
   * Parsea los datos recividos por el backend
   * Ej. ubicacion/sensorA/opcionA lo convierte a:
   * {
   *  ubicacion/sensorA : {
   *    opcionA : valor
   *  }
   * }
   * @param {Object} recivedData Datos recibidos del socker. Estos son topic, valor y time
   * @returns {Object} Objetos recibidos anteriormente y correctamente parseados
   */
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

  /**
   * Guarda los datos recibidos del servidor en el objeto de datos
   * Se encarga de verificar si la key del sensor ya existe en el objeto
   * Y guarda los valores de cada uno de estos en un array
   * Este array se va vaciando según se van mostrando los valores en una gráfica
   * @param {Object} recivedData Datos recibidos del socker y ya parseados correctamente
   * @param {Object} currentData Datos que ya se encuentran guardados en el componente
   * @returns {Object} Nuevos datos que se van a guardar en el estado del componente
   */
  const saveRecivedData = (recivedData, currentData) => {
    let needUpdate = false;
    for (const key in recivedData) {
      if (recivedData[key]['value'] === undefined) {
        if(currentData[key] === undefined) {
          currentData[key] = {};
        }
        saveRecivedData(recivedData[key], currentData[key]);
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
  
  /**
   * Obtiene el topic del sensor, y muestra el nombre de este correctamente en la cabecera de la gráfica
   * Ej. emulator/sensorA Lo transforma a Emulator SensorA
   * @param {String} topicName El Topic recibido por el sensor
   * @returns {String} Nombre a mostrar
   */
  const generateChartName = (topicName) => {
    let topics = topicName.split(TOPIC_SEPARATOR);
    if(topics.length >= 3) {
      return capitalize(topics.pop());
    }
    topics = topics.map(topic => capitalize(topic));
    return topics.join(" ");
  };

  /**
   * Genera cada una de las gráficas
   * Tener en cuenta, que podemos tener subgráficas
   * Por ejemplo, la aceleración tiene los componentes X, Y y Z.
   * Por lo tanto, tendremos que mostrar tres gráficas dentro de aceleración
   * Esto hace que sea recursiva.
   * @param {Object} newData Contiene los datos a mostrar en la gráfica
   * @param {String} topicName El nombre actual del topic. Cada vez que la función se llama a si misma, este se amplia
   * @returns {Array} Contiene cada una de las gráficas o subgráficas
   */
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
      setData(oldData => saveRecivedData(recivedData, oldData ? oldData : {}));
    });
  }, []);


  if(!data) {
    return <Loading/>;
  } else {
    return createCharts(data, '');
  }

};

export default ChartTabs;