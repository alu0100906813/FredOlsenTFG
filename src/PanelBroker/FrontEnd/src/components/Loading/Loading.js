
import Spinner from 'react-bootstrap/Spinner'

const Loading = () => {

  const generateSpinners = (numberOfSpinners = 3) => {
    let result = [];
    for (let i = 0; i < numberOfSpinners; ++i) {
      result.push(
        <Spinner key={i} animation="grow" variant="primary" />
      );
    }
    return result;
  }

  return (
    <div style={{'textAlign' : 'center', 'paddingTop' : '1rem'}}>
      {generateSpinners()}
    </div>
  );
};

export default Loading;

