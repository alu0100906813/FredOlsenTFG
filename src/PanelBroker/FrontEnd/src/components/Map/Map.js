
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import { divIcon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import shipIconURL from './ship-icon.svg';
import './map.css';

const POSITION = [28.468907, -16.2132297];

const Map = (props) => {

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

  return (
    <MapContainer style={{height : '80vh'}} center={POSITION} zoom={11} scrollWheelZoom={false}>
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />
    <Marker position={POSITION} icon={generateMarket(props.shipName)}/>
    </MapContainer>
  )
};

export default Map;