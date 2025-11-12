import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CreateListingPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [tags, setTags] = useState("");
  const [avail, setAvail] = useState({
    morning: false,
    afternoon: false,
    evening: false,
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    if (!title.trim() || !description.trim() || !location.trim()) {
      setError("Title, description, and location are required.");
      return;
    }
    const payload = {
      title: title.trim(),
      description: description.trim(),
      location: location.trim(),
      availability: avail,
      tags: tags.split(",").map((t) => t.trim()).filter(Boolean),
    };
    const res = await fetch("/api/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const j = await res.json().catch(() => ({ error: "Error" }));
      setError(j.error || "Failed to create.");
      return;
    }
    const created = await res.json();
    navigate(`/create-success?id=${created.id}`);
  }

  return (
    <div
      style={{
        maxWidth: 720,
        margin: "50px auto",
        padding: 24,
        background: "#fff",
        borderRadius: 12,
        boxShadow: "0 0 18px #eee",
      }}
    >
      <h2 style={{ color: "#F5821F", fontWeight: 710 }}>Create Listing</h2>
      {error ? <div style={{ color: "#b00", margin: "8px 0" }}>{error}</div> : null}
      <form onSubmit={onSubmit}>
        <label style={{ display: "block", marginTop: 12 }}>
          Title
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            style={{ width: "100%", padding: "9px", borderRadius: 7, border: "1px solid #f3ece8" }}
          />
        </label>
        <label style={{ display: "block", marginTop: 12 }}>
          Description
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            rows={5}
            style={{ width: "100%", padding: "9px", borderRadius: 7, border: "1px solid #f3ece8" }}
          />
        </label>
        <label style={{ display: "block", marginTop: 12 }}>
          Location
          <input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            required
            style={{ width: "100%", padding: "9px", borderRadius: 7, border: "1px solid #f3ece8" }}
          />
        </label>

        <div style={{ marginTop: 12 }}>
          <b>Availability</b>
          <br />
          <label>
            <input
              type="checkbox"
              checked={avail.morning}
              onChange={(e) => setAvail((v) => ({ ...v, morning: e.target.checked }))}
            />
            {" "}Morning
          </label>{" "}
          <label>
            <input
              type="checkbox"
              checked={avail.afternoon}
              onChange={(e) => setAvail((v) => ({ ...v, afternoon: e.target.checked }))}
            />
            {" "}Afternoon
          </label>{" "}
          <label>
            <input
              type="checkbox"
              checked={avail.evening}
              onChange={(e) => setAvail((v) => ({ ...v, evening: e.target.checked }))}
            />
            {" "}Evening
          </label>
        </div>

        <label style={{ display: "block", marginTop: 12 }}>
          Tags (comma separated)
          <input
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="barista, downtown"
            style={{ width: "100%", padding: "9px", borderRadius: 7, border: "1px solid #f3ece8" }}
          />
        </label>

        <button
          type="submit"
          style={{
            marginTop: 16,
            background: "#F5821F",
            color: "#fff",
            border: "none",
            padding: "10px 18px",
            borderRadius: 8,
            fontWeight: 700,
          }}
        >
          Post Job
        </button>
      </form>
    </div>
  );
}
