
import { useState, useEffect } from 'react';

import { GET } from './utils/ajax';

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import TopNavBar from './components/TopNavBar/TopNavBar';
import Loading from './components/Loading/Loading';
import ChartTabs from './components/ChartTabs/ChartTabs';

import { Container } from 'react-bootstrap';

const SHIPS_LIST_API = '/getShips';

function App() {

  const [shipsNames, setShipsNames] = useState();
  const [currentShip, setCurrentShip] = useState();

  useEffect(() => {
    GET(SHIPS_LIST_API, {}, (response) => {
      setShipsNames(response.data);
      setCurrentShip(response.data[0]);
    });
  }, []);

  const changeTab = (tabName) => {
    setCurrentShip(tabName);
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
          <ChartTabs currentShip={currentShip}/>
        </Container>
      </>
    );
  }

}

export default App;
