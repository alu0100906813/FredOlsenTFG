
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import { divIcon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import shipIconURL from './ship-icon.svg';
import './map.css';
import { useEffect, useState } from 'react';
import { GET } from '../../utils/ajax';
import Loading from '../Loading/Loading';
import Alert from '../Alert/Alert';

const POSITION = [28.468907, -16.2132297];

const SHIP_POSITION_API = '/getShipPosition';

const Map = (props) => {

  const [shipPositon, setShipPosition] = useState();

  const generateMarket = (shipName) => {
    return divIcon({
      html: 
        `<div>
          <h6>${shipName}</h6>
          <img style="width:30px; height:30px" src="${shipIconURL}"/>
        </div>`,
      className : 'shipIcon'
    });
  }

  useEffect(() => {
    GET(SHIP_POSITION_API, {params : {ship : props.shipName}}, (response) => {
      if (response['lat']) {
        // FALTA POR HACER
      } else { // No hay ningún sensor que de la posición
        setShipPosition({lat : undefined, lon : undefined});
      }
    });
  }, [])

  if(!shipPositon) {
    return <Loading/>
  } else {
    if(!shipPositon['lat']) {
      return (
        <Alert>
          Error, el barco {props.shipName} no cuenta con ningún sensor de GPS
        </Alert>
      );
    } else {
      return (
        <MapContainer style={{height : '80vh'}} center={POSITION} zoom={11} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={POSITION} icon={generateMarket(props.shipName)}/>
        </MapContainer>
      )
    }
  }

};

export default Map;