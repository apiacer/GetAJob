import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import JobListing from "./pages/JobListing";
import Maps from "./pages/Maps";
import Login from "./pages/Login";

function App() {
  // Add your own login state logic here (false by default)
  const isLoggedIn = false;

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing isLoggedIn={isLoggedIn} />} />
        <Route path="/job-listing" element={<JobListing />} />
        <Route path="/maps" element={<Maps />} />
        <Route path="/login" element={<Login />} />
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;
