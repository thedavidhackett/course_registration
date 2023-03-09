import { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import CourseList from "../components/CourseList";

export default function Courses() {
  const [courses, setCourses] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/student/courses")
      .then((res) => res.json())
      .then((data) => setCourses(data));
  }, []);

  return (
    <Container>
      <Row>
        <Col>
          <h2>Your Courses</h2>
        </Col>
      </Row>
      {courses && (
        <div>
          <Row>
            <Col>
              <h3>Registered</h3>
              <p>Classes you are currently registered for:</p>
              <CourseList courses={courses.registered} />
            </Col>
          </Row>
          <Row>
            <Col>
              <h3>Pending</h3>
              <p>Classes where registration is pending department approval:</p>
              <CourseList courses={courses.pending} />
            </Col>
          </Row>
          <Row>
            <Col>
              <h3>Tentative</h3>
              <p>
                Classes where registration is tentative based on instructor
                approval:
              </p>
              <CourseList courses={courses.tentative} />
            </Col>
          </Row>
        </div>
      )}
    </Container>
  );
}
