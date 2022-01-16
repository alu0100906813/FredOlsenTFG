
import BoostrapAlert from 'react-bootstrap/Alert';

const Alert = (props) => {

  return (
    <BoostrapAlert variant={props.variant ? props.variant : 'danger'}>
      {props.children}
    </BoostrapAlert>
  );

};

export default Alert;