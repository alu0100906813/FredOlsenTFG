
import { Container, Navbar, Nav } from 'react-bootstrap';

const TopNavBar = () => {

  return (
    <Navbar bg="primary" variant="dark">
      <Container>
      <Navbar.Brand className="me-auto">FredOlsen</Navbar.Brand>
      <Nav>
        <Nav.Link href="#home">Home</Nav.Link>
        <Nav.Link href="#features">Features</Nav.Link>
        <Nav.Link href="#pricing">Pricing</Nav.Link>
      </Nav>
      </Container>
    </Navbar>

  );

};

export default TopNavBar;