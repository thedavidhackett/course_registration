import { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import MenuCard from "../components/MenuCard";
import Notification from "../components/Notification";
import { get, delete_request } from "../utilities";

export default function Home() {
  const [user, setUser] = useState(null);
  const [notifications, setNotifications] = useState([]);

  const getNotifications = () => {
    get("http://localhost:5000/api/student/notifications", setNotifications);
  };

  const deleteNotification = (id) => {
    delete_request(
      `http://localhost:5000/api/notifications/${id}`,
      getNotifications
    );
  };

  useEffect(() => {
    get("http://localhost:5000/api/get-user", setUser);
    getNotifications();
  }, []);

  return (
    <Container>
      <Row>
        <Col>
          {notifications.map((n, id) => (
            <Notification
              notification={n}
              callback={getNotifications}
              destroy={() => deleteNotification(n.id)}
              key={id}
            />
          ))}
        </Col>
      </Row>
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
        <Col lg={4} md={6}>
          <Link to="/restrictions">
            <MenuCard text="View Restrictions" />
          </Link>
        </Col>
      </Row>
    </Container>
  );
}
