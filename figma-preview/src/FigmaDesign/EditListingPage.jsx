import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

export default function EditListingPage(){
const { id } = useParams();
const nav = useNavigate();
const [title, setTitle] = useState("");
const [description, setDescription] = useState("");
const [location, setLocation] = useState("");
const [tags, setTags] = useState("");
const [avail, setAvail] = useState({ morning:false, afternoon:false, evening:false });
const [error, setError] = useState("");

useEffect(()=>{
    (async ()=>{
    const r = await fetch(`/api/jobs/${id}`);
    if(!r.ok) { setError("Not found"); return; }
    const j = await r.json();
    setTitle(j.title || "");
    setDescription(j.description || "");
    setLocation(j.location || "");
    setAvail(j.availability || {morning:false,afternoon:false,evening:false});
    setTags((j.tags||[]).join(", "));
    })();
},[id]);

async function onSubmit(e){
    e.preventDefault();
    setError("");
    const payload = {
    title, description, location,
    availability: avail,
    tags: tags.split(",").map(t=>t.trim()).filter(Boolean)
    };
    const r = await fetch(`/api/jobs/${id}`, {
    method:"PUT",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify(payload)
    });
    if(!r.ok){ setError("Update failed"); return; }
    nav(`/job/${id}`);
}

return (
    <div style={{maxWidth:720, margin:"50px auto", padding:24, background:"#fff", borderRadius:12, boxShadow:"0 0 18px #eee"}}>
    <h2 style={{color:"#F5821F",fontWeight:710}}>Edit Listing</h2>
    {error ? <div style={{color:"#b00"}}>{error}</div> : null}
    <form onSubmit={onSubmit}>
        <label style={{display:"block", marginTop:12}}>Title
        <input value={title} onChange={e=>setTitle(e.target.value)}
                style={{width:"100%", padding:"9px", borderRadius:7, border:"1px solid #f3ece8"}} />
        </label>
        <label style={{display:"block", marginTop:12}}>Description
        <textarea value={description} onChange={e=>setDescription(e.target.value)} rows={5}
                    style={{width:"100%", padding:"9px", borderRadius:7, border:"1px solid #f3ece8"}} />
        </label>
        <label style={{display:"block", marginTop:12}}>Location
        <input value={location} onChange={e=>setLocation(e.target.value)}
                style={{width:"100%", padding:"9px", borderRadius:7, border:"1px solid #f3ece8"}} />
        </label>

        <div style={{marginTop:12}}>
        <b>Availability</b><br/>
        <label><input type="checkbox" checked={avail.morning} onChange={e=>setAvail(v=>({...v, morning:e.target.checked}))}/> Morning</label>{" "}
        <label><input type="checkbox" checked={avail.afternoon} onChange={e=>setAvail(v=>({...v, afternoon:e.target.checked}))}/> Afternoon</label>{" "}
        <label><input type="checkbox" checked={avail.evening} onChange={e=>setAvail(v=>({...v, evening:e.target.checked}))}/> Evening</label>
        </div>

        <label style={{display:"block", marginTop:12}}>Tags (comma separated)
        <input value={tags} onChange={e=>setTags(e.target.value)}
                style={{width:"100%", padding:"9px", borderRadius:7, border:"1px solid #f3ece8"}} />
        </label>

        <button type="submit" style={{marginTop:16, background:"#F5821F", color:"#fff", border:"none", padding:"10px 18px", borderRadius:8, fontWeight:700}}>
        Save Changes
        </button>
    </form>
    </div>
);
}
