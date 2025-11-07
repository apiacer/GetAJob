import { Link } from "react-router-dom";

export default function Login() {
  return (
    <div style={{ padding: 30 }}>
      <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <img src="/getajob-logo.png" alt="GetAJob Logo" style={{ width: 60, height: 60, borderRadius: "50%" }} />
        <nav>
          <Link to="/job-listing" style={{ margin: "0 10px" }}>Find Jobs</Link>
          <Link to="/maps" style={{ margin: "0 10px" }}>Maps</Link>
          <Link to="/login" style={{ margin: "0 10px" }}>
            <button style={{ background: "#F58220", color: "#fff", border: "none", padding: "8px 18px", borderRadius: "6px" }}>Log In</button>
          </Link>
        </nav>
      </header>
      <main style={{ maxWidth: 560, margin: "0 auto", marginTop: 90 }}>
        <h2 style={{ color: "#F58220", textAlign: "left" }}>Log In Here:</h2>
        <form style={{ background: "#fff", borderRadius: 12, border: "1px solid #eee", padding: 22, marginBottom: 24 }}>
          <div>
            <label>Email</label><br />
            <input type="text" placeholder="Type Here" style={{ width: "99%", marginBottom: 10 }} />
          </div>
          <div>
            <label>Password</label><br />
            <input type="password" placeholder="Type Here" style={{ width: "99%", marginBottom: 10 }} />
          </div>
          <button style={{ background: "#F58220", color: "#fff", border: "none", padding: "8px 14px", borderRadius: "6px", marginBottom: 14 }}>
            Log In
          </button>
          <div>
            <a href="/resetting-password" style={{ color: "#F58220", fontSize: "0.98rem" }}>Forgot password?</a>
          </div>
        </form>
        <h2 style={{ color: "#F58220", textAlign: "left" }}>New to GetAJob?</h2>
        <Link to="/signup">
          <button style={{ width: "100%", background: "#F58220", color: "#fff", border: "none", padding: "10px 0", borderRadius: "6px" }}>
            Sign Up Here
          </button>
        </Link>
      </main>
    </div>
  );
}
