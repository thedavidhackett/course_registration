import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import Notification from "../components/Notification";
import { post, get } from "../utilities";

export default function Course({ id }) {
  let { courseSectionId } = useParams();
  const [course, setCourse] = useState(null);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    get(
      `http://localhost:5000/api/course-section/${courseSectionId}`,
      setCourse
    );
  }, [notification]);

  const handleDrop = () => {
    post(
      `http://localhost:5000/api/drop-course/${courseSectionId}`,
      {},
      setNotification
    );
  };

  const handleRegister = () => {
    post(
      `http://localhost:5000/api/register`,
      { course_section_id: courseSectionId },
      setNotification
    );
  };

  return course ? (
    <Container>
      <Row>
        <Col>
          <h2>
            {course.course.name} - {course.course.id}
          </h2>
        </Col>
      </Row>
      {notification && (
        <Row>
          <Col>
            <Notification
              notification={notification}
              callback={setNotification}
            />
          </Col>
        </Row>
      )}
      <Row>
        <Col>
          {course.times.map((t, i) => (
            <h4 key={i}>
              {t.day} - {t.start_time} - {t.end_time}
            </h4>
          ))}
        </Col>
      </Row>
      <Row>
        <Col>
          <h3>Description</h3>
          <p>{course.course.description}</p>
        </Col>
      </Row>
      <Row>
        <Col>
          {course.enrolled ? (
            <Button onClick={handleDrop}>Drop</Button>
          ) : (
            <Button onClick={handleRegister}>Register</Button>
          )}
        </Col>
      </Row>
    </Container>
  ) : (
    ""
  );
}
