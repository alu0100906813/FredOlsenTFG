
import { Button } from 'react-bootstrap';

import './changeButton.css';

import { AiFillPieChart } from 'react-icons/ai';
import { RiRoadMapFill } from 'react-icons/ri';

/**
 * Opción que indica que es una gráfica
 */
export const CHART = 1;

/**
 * Opción que indica que es un mapa
 */
export const MAP = 2;

/**
 * Botón flotante en la parte inferior izquierda de la página que sirve para alternar entre las gráficas o el mapa
 * @param {Object} props Propiedades del Objeto
 * - selected: Opción que se encuentra seleccionada (Gráfica o mapa)
 * - onClick: Evento que es lanzado cuando el usuario pulsa el botón
 * @returns {JSX} Contiene el componente
 */
export const ChangeButton = (props) => {

  /**
   * Devuelve el contenido del texto del botón según esté seleccionado el mapa o la gráfica
   * @returns {JSX} Contine el texto del botón (Icono + span con texto)
   */
  const buttonText = () => {
    return props.selected === CHART ? 
      [<RiRoadMapFill key={'mapIcon'}/>, <span key={'mapText'}>Mapa</span>] : 
      [<AiFillPieChart key={'chartIcon'}/>, <span key={'chartText'}>Gráfica</span>]; 
  }

  return (
    <Button onClick={() => props.onClick()} className="changeButton" variant="primary" size="lg">{buttonText()}</Button>
  )

};