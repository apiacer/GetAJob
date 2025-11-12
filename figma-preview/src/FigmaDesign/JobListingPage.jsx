import React, { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";

export default function JobListingPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [jobs, setJobs] = useState([]);
  const [q, setQ] = useState(searchParams.get("q") || "");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    const fetchJobs = async () => {
      setLoading(true);
      try {
        const query = q ? `?q=${encodeURIComponent(q)}` : "";
        const res = await fetch(`/api/jobs${query}`, { signal: controller.signal });
        const data = await res.json();
        setJobs(Array.isArray(data) ? data : []);
      } catch {
        // swallow errors (component might unmount)
      }
      setLoading(false);
    };
    fetchJobs();
    return () => controller.abort();
  }, [q]);

  function onSearchSubmit(e) {
    e.preventDefault();
    const next = new URLSearchParams();
    if (q) next.set("q", q);
    setSearchParams(next, { replace: true });
  }

  return (
    <div style={{ maxWidth: 960, margin: "50px auto", padding: 24 }}>
      <h2 style={{ color: "#F5821F", fontWeight: 710, fontSize: "1.65rem" }}>Job Listings</h2>

      <form onSubmit={onSearchSubmit} style={{ marginTop: 25, marginBottom: 8 }}>
        <input
          type="text"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search jobs..."
          style={{
            width: "70%",
            padding: "9px 15px",
            borderRadius: 7,
            border: "1px solid #f3ece8",
            fontSize: "1.05em",
          }}
        />
        <button type="submit" style={{ marginLeft: 12 }}>
          Search
        </button>
        <Link
          to="/create-listing"
          style={{
            marginLeft: 25,
            background: "#F5821F",
            color: "#fff",
            padding: "10px 18px",
            borderRadius: 8,
            textDecoration: "none",
            fontWeight: 700,
          }}
        >
          Create Listing
        </Link>
      </form>

      {loading ? <div>Loading…</div> : null}

      <div style={{ marginTop: 20 }}>
        {jobs.map((j) => (
          <Link
            key={j.id}
            to={`/job/${j.id}`}
            style={{
              display: "block",
              background: "#fff",
              padding: "18px 17px",
              borderRadius: 8,
              boxShadow: "0 1px 8px #eee",
              marginBottom: 19,
              textDecoration: "none",
              color: "#214",
            }}
          >
            <b style={{ color: "#F5821F" }}>{j.title}</b>
            <div style={{ marginTop: 5 }}>{j.location} · {j.tags?.join(", ")}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
