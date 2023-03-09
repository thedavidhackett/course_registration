import { useEffect, useState } from "react";
import { get } from "../utilities";
import { Container, Row, Col } from "react-bootstrap";

export default function Restrictions() {
  const [restrictions, setRestrictions] = useState(null);

  useEffect(() => {
    get("http://localhost:5000/api/student/restrictions", setRestrictions);
  }, []);

  return (
    <Container>
      {restrictions && (
        <Row>
          <Col>
            <h2>Restrictions</h2>
            {restrictions.length > 0 ? (
              <ul>
                {restrictions.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            ) : (
              <p>You don't currently have any restrictions</p>
            )}
          </Col>
        </Row>
      )}
    </Container>
  );
}
