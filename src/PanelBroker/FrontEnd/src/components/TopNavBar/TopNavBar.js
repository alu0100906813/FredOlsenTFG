
import { Container, Navbar, Nav } from 'react-bootstrap';

import './TopNavBar.css';

const TopNavBar = (props) => {

  return (
    <Navbar bg="primary" variant="dark">
      <Container>
      <Navbar.Brand className="me-auto">FredOlsen</Navbar.Brand>
      <Nav>
        {props.tabs.map(tab => {
          return <Nav.Link onClick={(e) => props.onClick(tab)} className={tab === props.currentTab ? 'active' : ''}>{tab}</Nav.Link>
        })}
      </Nav>
      </Container>
    </Navbar>

  );

};

export default TopNavBar;