import { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import MenuCard from "../components/MenuCard";

export default function Home() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch("http://localhost:5000/api/get-user")
      .then((res) => res.json())
      .then((data) => setUser(data));
  }, []);

  return (
    <Container>
      <Row>
        <Col>
          <h1>{user ? "Welcome " + user.name : ""}</h1>
        </Col>
      </Row>
      <Row>
        <Col lg={4} md={6}>
          <Link to="/my-courses">
            <MenuCard text="View/Drop Courses" />
          </Link>
        </Col>
        <Col lg={4} md={6}>
          <Link to="/course-search">
            <MenuCard text="Search/Add Courses" />
          </Link>
        </Col>
      </Row>
    </Container>
  );
}
