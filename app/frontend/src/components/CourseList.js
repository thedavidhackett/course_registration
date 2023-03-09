import Card from "react-bootstrap/Card";
import { Link } from "react-router-dom";

export default function CourseList({ courses }) {
  return (
    <div>
      {courses.map((c) => (
        <Course course={c} key={c.id} />
      ))}
    </div>
  );
}

function Course({ course }) {
  return (
    <Card>
      <Card.Body>
        <Card.Title>
          <Link to={`/course/${course.id}`}>
            {course.course.name} - {course.id}
          </Link>
        </Card.Title>
        <Card.Subtitle>
          {course.times.map((t, i) => (
            <div key={i}>
              {t.day} {t.start_time} - {t.end_time}
            </div>
          ))}
        </Card.Subtitle>
      </Card.Body>
    </Card>
  );
}
