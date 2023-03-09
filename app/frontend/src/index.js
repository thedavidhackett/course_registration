import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import Home from "./routes/Home";
import Course from "./routes/Course";
import Courses from "./routes/Courses";
import CourseSearch from "./routes/CourseSearch";
import Restrictions from "./routes/Restrictions";
import reportWebVitals from "./reportWebVitals";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "",
        element: <Home />,
      },
      {
        path: "/my-courses",
        element: <Courses />,
      },
      {
        path: "/course/:courseSectionId",
        element: <Course />,
      },
      {
        path: "/course-search",
        element: <CourseSearch />,
      },
      {
        path: "/restrictions",
        element: <Restrictions />,
      },
    ],
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
