import logo from "./logo.svg";
import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch("http://localhost:5000/api/get-user")
      .then((res) => res.json())
      .then((data) => setUser(data));
  }, []);

  return (
    <div className="App">
      <h1>{user ? user.name : ""}</h1>
    </div>
  );
}

export default App;
