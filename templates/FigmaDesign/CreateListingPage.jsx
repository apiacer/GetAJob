import React, { useState } from "react";

export default function CreateListingPage() {
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  return (
    <div style={{maxWidth:530,margin:"60px auto",padding:38,background:"#fff",borderRadius:10,boxShadow:"0 0 16px #eee"}}>
      <h2 style={{color:"#F5821F",fontWeight:700}}>Create Job Listing</h2>
      <form>
        <label style={{display:"block",marginBottom:13}}>Title
          <input value={title} onChange={e=>setTitle(e.target.value)}
            required style={{width:"100%",padding:"9px",marginTop:5,borderRadius:6,border:"1px solid #f3ece8"}}
            placeholder="Enter job title"
          />
        </label>
        <label style={{display:"block",marginBottom:23}}>Description
          <textarea value={desc} onChange={e=>setDesc(e.target.value)}
            required style={{width:"100%",height:"90px",padding:"9px",marginTop:5,borderRadius:6,border:"1px solid #f3ece8"}}
            placeholder="Describe the job..."
          />
        </label>
        <button type="submit"
          style={{
            background:"#F5821F", color:"#fff", border:"none", borderRadius:7,
            padding:"12px 27px",fontWeight:700,fontSize:"1.04em", width:"100%",marginBottom:10
          }}>
          Create Listing
        </button>
      </form>
    </div>
  );
}
