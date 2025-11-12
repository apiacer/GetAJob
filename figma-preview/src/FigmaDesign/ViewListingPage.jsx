import React, { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";

export default function ViewListingPage() {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [err, setErr] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    let stop = false;
    (async () => {
      try {
        const res = await fetch(`/api/jobs/${id}`);
        if (!res.ok) throw new Error("not found");
        const j = await res.json();
        if (!stop) setJob(j);
      } catch {
        if (!stop) setErr("Not found");
      }
    })();
    return () => {
      stop = true;
    };
  }, [id]);

  async function onDelete() {
    if (!window.confirm("Delete this listing?")) return;
    const res = await fetch(`/api/jobs/${id}`, { method: "DELETE" });
    if (res.ok) navigate("/jobs");
  }

  if (err) return <div style={{ maxWidth: 750, margin: "50px auto" }}>{err}</div>;
  if (!job) return <div style={{ maxWidth: 750, margin: "50px auto" }}>Loading…</div>;

  const a = job.availability || {};
  return (
    <div
      style={{
        maxWidth: 750,
        margin: "50px auto",
        padding: 28,
        background: "#fff",
        borderRadius: 12,
        boxShadow: "0 0 18px #eee",
      }}
    >
      <h2 style={{ color: "#F5821F", fontWeight: 710 }}>Job Listing Details</h2>
      <b style={{ fontSize: "1.25em", color: "#F5821F", marginBottom: 10, display: "block" }}>{job.title}</b>
      <div>
        <b>Location:</b> {job.location}
      </div>
      <div style={{ marginTop: 8 }}>{job.description}</div>
      <div style={{ marginTop: 8 }}>
        <b>Availability:</b> {["morning", "afternoon", "evening"].filter((k) => a[k]).join(", ") || "—"}
      </div>
      <div style={{ marginTop: 8 }}>
        <b>Tags:</b> {job.tags?.join(", ") || "—"}
      </div>

      <div style={{ marginTop: 16 }}>
        <Link to={`/edit/${job.id}`} style={{ marginRight: 16, color: "#F5821F", fontWeight: 700 }}>
          Edit
        </Link>
        <button
          onClick={onDelete}
          style={{ color: "#b00", fontWeight: 700, background: "transparent", border: "none", cursor: "pointer" }}
        >
          Delete
        </button>
      </div>

      <div style={{ marginTop: 10 }}>
        <Link to="/leave-rating" style={{ marginRight: 24, color: "#F5821F", fontWeight: 700 }}>
          Leave Rating
        </Link>
        <Link to="/messaging" style={{ marginRight: 24, color: "#F5821F", fontWeight: 700 }}>
          Message Employer
        </Link>
        <Link to="/jobs" style={{ color: "#F5821F", fontWeight: 700 }}>
          Back to Listings
        </Link>
      </div>
    </div>
  );
}
