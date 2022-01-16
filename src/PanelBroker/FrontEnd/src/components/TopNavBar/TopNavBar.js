
import { Container, Navbar, Nav } from 'react-bootstrap';

import './TopNavBar.css';

const TopNavBar = (props) => {

  return (
    <Navbar bg="primary" variant="dark">
      <Container>
        <Nav.Link href="/">
          <Navbar.Brand className="me-auto">FredOlsen</Navbar.Brand>
        </Nav.Link>
      <Nav>
        {props.tabs.map(tab => {
          return <Nav.Link key={tab} onClick={(e) => props.onClick(tab)} className={tab === props.currentTab ? 'active' : ''}>{tab}</Nav.Link>
        })}
      </Nav>
      </Container>
    </Navbar>

  );

};

export default TopNavBar;