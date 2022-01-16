
import { Button } from 'react-bootstrap';

import './changeButton.css';

import { AiFillPieChart } from 'react-icons/ai';
import { RiRoadMapFill } from 'react-icons/ri';


export const CHART = 1;
export const MAP = 2;

export const ChangeButton = (props) => {

  const buttonText = () => {
    return props.selected === CHART ? 
      [<RiRoadMapFill key={'mapIcon'}/>, <span key={'mapText'}>Mapa</span>] : 
      [<AiFillPieChart key={'chartIcon'}/>, <span key={'chartText'}>Gráfica</span>]; 
  }

  return (
    <Button onClick={() => props.onClick()} className="changeButton" variant="primary" size="lg">{buttonText()}</Button>
  )

};