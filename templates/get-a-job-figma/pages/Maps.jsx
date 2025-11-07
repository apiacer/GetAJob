export default function Maps() {
  return (
    <div style={{ padding: 30 }}>
      <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <img src="/getajob-logo.png" alt="GetAJob Logo" style={{ width: 60, height: 60, borderRadius: "50%" }} />
        <nav>
          <a href="/job-listing" style={{ margin: "0 10px" }}>Find Jobs</a>
          <a href="/maps" style={{ margin: "0 10px" }}>Maps</a>
          <a href="/login" style={{ margin: "0 10px" }}>
            <button style={{ background: "#F58220", color: "#fff", border: "none", padding: "8px 18px", borderRadius: "6px" }}>Log In</button>
          </a>
        </nav>
      </header>
      <main>
        <h1 style={{ color: "#F58220", textAlign: "center", marginTop: 24 }}>Find Jobs Near You</h1>
        <div style={{ margin: "23px auto", maxWidth: 420, border: "1px solid #bbb", borderRadius: 12, background: "#f7f7f7", padding: 16 }}>
          <span style={{ color: "#F58220" }}>Your Location:</span>
          <input type="text" placeholder="Type Here" style={{ width: "70%", marginLeft: 12, padding: "7px", borderRadius: 6, border: "1px solid #eee" }} />
        </div>
        <div style={{ margin: "0 auto", width: "90%", minHeight: 260, background: "#eeecec", borderRadius: 16, border: "1px solid #eaeaea", display: "flex", alignItems: "center", justifyContent: "center" }}>
          {/* Map Placeholder */}
          <img src="/map-placeholder.png" alt="Map" style={{ width: "100%", height: "240px", objectFit: "cover", borderRadius: 10 }} />
        </div>
      </main>
    </div>
  );
}
