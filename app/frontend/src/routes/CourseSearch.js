import { useEffect, useState } from "react";
import { Container, Row, Col, Form, Button } from "react-bootstrap";
import { get } from "../utilities";
import CourseList from "../components/CourseList";

export default function CourseSearch() {
  const [courses, setCourses] = useState(null);
  const [departments, setDepartments] = useState([]);

  useEffect(() => {
    get("http://localhost:5000/api/departments", setDepartments);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    get("http://localhost:5000/api/courses", setCourses, {
      course_id: e.target.course_id.value,
      department_id: e.target.department_id.value,
    });
  };

  return (
    <Container>
      <Row>
        <Col>
          <h1>Courses</h1>
        </Col>
      </Row>
      <Row>
        <Col>
          <h2>Search for a course</h2>
        </Col>
      </Row>
      <Row>
        <Col>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="course_id">
              <Form.Label>Course ID</Form.Label>
              <Form.Control type="number" placeholder="Enter a course id" />
            </Form.Group>
            <Form.Group controlId="department_id">
              <Form.Label>Department</Form.Label>
              <Form.Select>
                <option></option>
                {departments.map((d, i) => (
                  <option key={i} value={d.id}>
                    {d.name}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </Col>
      </Row>
      {courses && (
        <Row>
          <Col>
            <h2>Results</h2>
            {courses.length > 0 ? (
              <CourseList courses={courses} />
            ) : (
              <p>No courses match that criteria</p>
            )}
          </Col>
        </Row>
      )}
    </Container>
  );
}
