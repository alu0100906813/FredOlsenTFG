
import BoostrapAlert from 'react-bootstrap/Alert';

/**
 * Muestra una alerta que puede ser de información, de error, etc.
 * Para ello, utiliza las alertas de React Bootstrap
 * @param {Object} props Contiene las propiedades de la alerta
 * - Variant: El tipo de alerta (Información, error), según react bootstrap
 * @returns {JSX} Contiene el componente
 */
const Alert = (props) => {

  return (
    <BoostrapAlert variant={props.variant ? props.variant : 'danger'}>
      {props.children}
    </BoostrapAlert>
  );

};

export default Alert;