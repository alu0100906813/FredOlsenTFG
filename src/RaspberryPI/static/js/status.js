
const RELOAD_SECONDS = 10000;

const brokerDOM = document.getElementById('brokerStatus');
const queueDOM = document.getElementById('queueStatus');
const counterDOM = document.getElementById('counter');

let counter = 0;

const RED_COLOR = 'Crimson';
const YELLOW_COLOR = 'AntiqueWhite';
const GREEN_COLOR = 'Chartreuse';

const Ajax = (url, callback) => {
  fetch(url)
    .then(response => response.json())
    .then(data => callback(data));
}

const changeBackgrounColor = (dom, color) => {
  dom.style.backgroundColor = color;
}

const updateCounter = () => {
  let result = ''
  switch (counter) {
    case counter < 3600: {
      result += Math.trunc(counter / 3600) + 'h ';
    }
    case counter < 60: {
      result += Math.trunc((counter % 3600) / 60) + 'm ';
    }
    default: {
      result += counter % 60 + 's';
    }
  }
  counterDOM.innerHTML = result;
}

const updateDOMContents = (data) => {
  if(typeof data === 'object' && data['status'] !== undefined) {
    brokerDOM.innerHTML = data['status'] ? 'Connected' : 'Disconnected';
    changeBackgrounColor(brokerDOM, data['status'] ? GREEN_COLOR : RED_COLOR);
    queueDOM.innerHTML = data['queue'];
    changeBackgrounColor(queueDOM, data['queue'] === 0 ? GREEN_COLOR : YELLOW_COLOR);
    counter = 0;
  }
};

const getStatus = () => {
  Ajax('/status', (response) => { updateDOMContents(response)});
};

setInterval(getStatus, RELOAD_SECONDS);
setInterval(() => {
  counter++;
  updateCounter();
}, 1000)
getStatus()