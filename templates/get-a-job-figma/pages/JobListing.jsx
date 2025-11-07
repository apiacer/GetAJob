export default function JobListing() {
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
        <h1 style={{ color: "#F58220", textAlign: "center", marginTop: 20 }}>Find Your Future Here</h1>
        <section style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div style={{ border: "1px solid #bbb", borderRadius: 14, padding: 22, margin: "20px 0", maxWidth: 440, background: "#f7f7f7" }}>
            <div>
              <label>
                <input type="checkbox" /> Yardwork
              </label>
              <label>
                <input type="checkbox" /> Indoors
              </label>
              <label>
                <input type="checkbox" /> Unskilled
              </label>
              <label>
                <input type="checkbox" /> Repair
              </label>
              <label>
                <input type="checkbox" /> Tutoring
              </label>
            </div>
            <div>
              Min Price (dollars): <input type="text" placeholder="Type Here" style={{ width: 80 }} />
              Max Price (dollars): <input type="text" placeholder="Type Here" style={{ width: 80 }} />
              <button style={{ marginLeft: 15, background: "#F58220", color: "#fff", border: "none", borderRadius: 7, padding: "4px 12px" }}>Time</button>
            </div>
            <div>
              Min Distance (miles): <input type="text" placeholder="Type Here" style={{ width: 70 }} />
              Max Distance (miles): <input type="text" placeholder="Type Here" style={{ width: 70 }} />
              Address: <input type="text" placeholder="Type Address" style={{ width: 130 }} />
            </div>
          </div>
        </section>
        <h2 style={{ color: "#F58220", textAlign: "center" }}>Browse Local Jobs needed</h2>
        <section>
          {/* Example job cards */}
          {["Lawn Care Provider Needed", "Fitness Instructor", "Market Analyst", "Project Manager"].map((job, idx) => (
            <div key={idx} style={{ border: "1px solid #eee", borderRadius: 10, padding: 22, margin: "16px 0", background: "#fff", maxWidth: 560 }}>
              <h3 style={{ margin: "6px 0", color: "#474747" }}>{job}</h3>
              <p>
                {job === "Lawn Care Provider Needed" && "In need of someone to help maintain client's lawns in Sacramento area. Pays daily. $20 an hour!!"}
                {job === "Fitness Instructor" && "Part-time position at The Well at Sac State. Must be a student. $18 an hour!"}
                {job === "Market Analyst" && "Full-time position as a market analyst at Chase Bank. Elk Grove location. Click below for more details."}
                {job === "Project Manager" && "Full-time position at Rose Remodeling. 5+ years experience needed. Full description below."}
              </p>
              <button style={{ background: "#F58220", color: "#fff", border: "none", padding: "8px 17px", borderRadius: "6px" }}>
                View Listing
              </button>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}
