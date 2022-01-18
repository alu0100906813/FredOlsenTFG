
import { Container, Navbar, Nav } from 'react-bootstrap';

/**
 * Contiene el NavBar de la parte inferior de la página
 * @returns 
 */
const BottomNavBar = () => {

  return (
    <Navbar bg="primary" variant="dark" style={{marginTop : '2rem'}}>
      <Container>
        <Nav.Link href="/">
          <Navbar.Brand className="me-auto">Bottom</Navbar.Brand>
        </Nav.Link>
      </Container>
    </Navbar>

  );

};

export default BottomNavBar;