import { Link } from "react-router-dom";

export default function Landing({ isLoggedIn }) {
  return (
    <div>
      <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <img src="/getajob-logo.png" alt="GetAJob Logo" style={{ width: 60, height: 60, borderRadius: "50%" }} />
        </div>
        <nav>
          <Link to="/job-listing" style={{ margin: "0 10px" }}>Find Jobs</Link>
          <Link to="/maps" style={{ margin: "0 10px" }}>Maps</Link>
          <Link to="/login" style={{ margin: "0 10px" }}>
            <button style={{ background: "#F58220", color: "#fff", border: "none", padding: "8px 18px", borderRadius: "6px" }}>Log In</button>
          </Link>
        </nav>
      </header>
      <main style={{ textAlign: "center", marginTop: 40 }}>
        <h1 style={{ color: "#F58220", fontSize: "3rem", marginBottom: 0 }}>GetAJob</h1>
        <h2>Your user friendly job finder</h2>
        <p style={{ fontSize: "1.2rem", color: "#F58220", marginBottom: 20 }}>
          Only one step away from finding your future
        </p>
        <Link to="/job-listing">
          <button style={{ background: "#F58220", color: "#fff", border: "none", padding: "12px 38px", fontSize: "1.1rem", borderRadius: "6px", marginBottom: 40 }}>
            Get Started
          </button>
        </Link>
        <section>
          <h2 style={{ color: "#F58220", marginTop: 60 }}>Our Purpose</h2>
          <div style={{ display: "flex", justifyContent: "space-around", gap: 13 }}>
            <div style={{ maxWidth: 250 }}>
              <img src="/purpose-community.png" alt="Helping community illustration" style={{ width: "100%", borderRadius: 20 }} />
              <h3 style={{ color: "#F58220", fontSize: "1rem", margin: "10px 0 5px 0" }}>Helping our community find jobs</h3>
              <p style={{ fontSize: "0.98rem" }}>
                Nowadays finding job opportunities is difficult, that’s where we come in. Our goal is help others find employment, whether it be odd jobs or tenured positions, we have it.
              </p>
            </div>
            <div style={{ maxWidth: 250 }}>
              <img src="/purpose-audience.png" alt="Audience illustration" style={{ width: "100%", borderRadius: 20 }} />
              <h3 style={{ color: "#F58220", fontSize: "1rem", margin: "10px 0 5px 0" }}>Our Audience</h3>
              <p style={{ fontSize: "0.98rem" }}>
                No matter who you are or where you are, everyone is welcome to use our website. We welcome everyone no matter the situation.
              </p>
            </div>
            <div style={{ maxWidth: 250 }}>
              <img src="/purpose-can-do.png" alt="Features illustration" style={{ width: "100%", borderRadius: 20 }} />
              <h3 style={{ color: "#F58220", fontSize: "1rem", margin: "10px 0 5px 0" }}>What We Can Do</h3>
              <p style={{ fontSize: "0.98rem" }}>
                Enjoy our filtered search, mapping features, easy-2-use interface, fast application and more!
              </p>
            </div>
          </div>
        </section>
        <section>
          <div style={{ display: "flex", justifyContent: "center", gap: 26, marginTop: 45 }}>
            <div style={{ background: "#fff", border: "1px solid #eee", borderRadius: 10, padding: 13, minWidth: 180 }}>
              <blockquote>"I never found a job so quick"</blockquote>
              <div><span style={{ fontWeight: "bold" }}>Herky</span> <span style={{ color: "#555" }}>Contractor</span></div>
            </div>
            <div style={{ background: "#fff", border: "1px solid #eee", borderRadius: 10, padding: 13, minWidth: 180 }}>
              <blockquote>"I love the design of this site!"</blockquote>
              <div><span style={{ fontWeight: "bold" }}>Benjamin Franklin</span> <span style={{ color: "#555" }}>Client</span></div>
            </div>
            <div style={{ background: "#fff", border: "1px solid #eee", borderRadius: 10, padding: 13, minWidth: 180 }}>
              <blockquote>"So much better than Indeed"</blockquote>
              <div><span style={{ fontWeight: "bold" }}>Mike Tyson</span> <span style={{ color: "#555" }}>Client</span></div>
            </div>
          </div>
        </section>
        {/* Placeholder for logged in/out content */}
        <section style={{ marginTop: 80 }}>
          {/* You can swap this space dynamically when user is logged in */}
          {isLoggedIn ? <div>[Logged In Home Content]</div> : null}
        </section>
      </main>
    </div>
  );
}
