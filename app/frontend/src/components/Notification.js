import { useState } from "react";
import { Alert, Button, Form } from "react-bootstrap";
import { post } from "../utilities";

export default function Notification({ notification, callback, destroy }) {
  const [error, setError] = useState(null);
  const handleSubmit = (e) => {
    e.preventDefault();

    if (notification.action) {
      let data = notification.data;
      if (notification.value_name) {
        let value = e.target[notification.value_name].value;
        if (!value) {
          setError("You must select a value");
          return;
        } else {
          data[notification.value_name] = value;
        }
      }
      post(`http://localhost:5000/api/${notification.action}`, data, callback);
    }
  };
  return (
    <Alert variant={notification.type} onClose={() => destroy()} dismissible>
      <p>{notification.msg}</p>
      {notification.action && (
        <Form onSubmit={handleSubmit}>
          {notification.value_name && (
            <div>
              {notification.options.map((o, i) => (
                <Form.Check
                  type="radio"
                  id={notification.value_name}
                  value={o.value}
                  label={o.label}
                />
              ))}
            </div>
          )}
          {error && <div>{error}</div>}
          <Button type="submit">{notification.submit_text}</Button>
        </Form>
      )}
    </Alert>
  );
}
