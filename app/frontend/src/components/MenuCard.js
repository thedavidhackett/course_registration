import Card from "react-bootstrap/Card";

function MenuCard({ text, children }) {
  return (
    <Card>
      <Card.Body>
        <h3>{text}</h3>
        <div>{children}</div>
      </Card.Body>
    </Card>
  );
}

export default MenuCard;
