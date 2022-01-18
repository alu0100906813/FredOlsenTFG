
import { useState, useEffect } from 'react';

import { GET } from './utils/ajax';

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import TopNavBar from './components/TopNavBar/TopNavBar';
import Loading from './components/Loading/Loading';
import ChartTabs from './components/ChartTabs/ChartTabs';

import { Container } from 'react-bootstrap';
import { ChangeButton, CHART, MAP } from './components/ChangeButton/ChangeButton';

import Map from './components/Map/Map';
import BottomNavBar from './components/BottomNavBar/BottomNavBar';

const SHIPS_LIST_API = '/getShips';

function App() {

  const [shipsNames, setShipsNames] = useState();
  const [currentShip, setCurrentShip] = useState();
  const [mapOrChart, setMapOrChart] = useState(CHART);

  useEffect(() => {
    GET(SHIPS_LIST_API, {}, (response) => {
      setShipsNames(response.data);
      setCurrentShip(response.data[0]);
    });
  }, []);

  const changeTab = (tabName) => {
    setCurrentShip(tabName);
  }

  const switchMapOrChart = () => {
    setMapOrChart(mapOrChart === CHART ? MAP : CHART);
  }

  if(!currentShip) {
    return (
      <Loading/>
    );
  } else {
    return (
      <>
        <div className="content">
          <TopNavBar tabs={shipsNames} onClick={changeTab} currentTab={currentShip}/>
        </div>
        <Container style={{'paddingTop' : '1rem'}}>
          {mapOrChart === CHART ? 
          <ChartTabs currentShip={currentShip}/> : 
          <Map shipName={currentShip}/>
          }
        </Container>
        <ChangeButton onClick={switchMapOrChart} selected={mapOrChart}/>
        <div className='content'>
          <BottomNavBar/>
        </div>
      </>
    );
  }

}

export default App;
