
const RELOAD_SECONDS = 10000;

const brokerDOM = document.getElementById('brokerStatus');
const queueDOM = document.getElementById('queueStatus');
const counterDOM = document.getElementById('counter');

let counter = 0;

const RED_COLOR = 'Crimson';
const YELLOW_COLOR = 'AntiqueWhite';
const GREEN_COLOR = 'Chartreuse';

/**
 * Hace una petición AJAX al backend para obtener el estado del IOT y del broker
 * @param {String} url Dirección hacia donde hacer el GET
 * @param {Function} callback Función la cual se ejecuta después de realizar el AJAX
 */
const Ajax = (url, callback) => {
  try {
    fetch(url)
    .then(response => response.json())
    .then(data => callback(data))
  } catch (e) {}
}

/**
 * Cambia el color de fondo de un DOM
 * @param {Object} dom DOM a cambiar el color de fondo
 * @param {String} color Color nuevo a cambiar
 */
const changeBackgrounColor = (dom, color) => {
  dom.style.backgroundColor = color;
}

/**
 * Actualiza el DOM que muestra el contador.
 * Este contador simplemente transforma la variable counter a segundos, horas y minutos
 * La variable de counter contiene el total de segundos
 */
 const updateCounter = () => {
  const getHours = (seconds) => seconds > 3600 ? Math.trunc(seconds / 3600) + 'h ' : '';
  const getMinutes = (seconds) => seconds > 60 ? Math.trunc((seconds % 3600) / 60) + 'm ' : '';
  const result = getHours(counter) + getMinutes(counter) + (counter % 60 + 's')
  counterDOM.innerHTML = result;
}


/**
 * Actualiza los DOMS de la página que muestran el estado del broker y del IOT
 * @param {Object} data Contiene datos sobre el broker los items que se encuentran en cola en el IOT
 */
const updateDOMContents = (data) => {
  if(typeof data === 'object' && data['status'] !== undefined) {
    brokerDOM.innerHTML = data['status'] ? 'Connected' : 'Disconnected';
    changeBackgrounColor(brokerDOM, data['status'] ? GREEN_COLOR : RED_COLOR);
    queueDOM.innerHTML = data['queue'];
    changeBackgrounColor(queueDOM, data['queue'] === 0 ? GREEN_COLOR : YELLOW_COLOR);
    counter = 0;
  }
};

/**
 * Obtenemos el estado del IOT (El número de paquetes en cola y si el broker está en activo)
 */
const getStatus = () => {
  Ajax('/status', (response) => { updateDOMContents(response)});
};

setInterval(getStatus, RELOAD_SECONDS);
setInterval(() => {
  counter++;
  updateCounter();
}, 1000)
getStatus()