import React from "react";

export default function JobListingPage() {
  return (
    <div style={{maxWidth:960, margin:"50px auto",padding:24}}>
      <h2 style={{color:"#F5821F",fontWeight:710,fontSize:"1.65rem"}}>Job Listings</h2>
      <div style={{marginTop:25,marginBottom:8}}>
        <input type="text" placeholder="Search jobs..." style={{
          width:"70%",padding:"9px 15px",borderRadius:7,border:"1px solid #f3ece8",fontSize:"1.05em"
        }}/> 
        <a href="/create-listing" style={{
          marginLeft:25,background:"#F5821F",color:"#fff",padding:"10px 18px",
          borderRadius:8,textDecoration:"none",fontWeight:700
        }}>Create Listing</a>
      </div>
      <div style={{marginTop:30}}>
        {/* Sample jobs */}
        {[1,2,3,4].map(id=>(
          <a key={id} href={`/job/${id}`} style={{
            display:"block",background:"#fff",padding:"18px 17px",borderRadius:8,
            boxShadow:"0 1px 8px #eee",marginBottom:19,textDecoration:"none",color:"#214"
          }}>
            <b style={{color:"#F5821F"}}>Job Title #{id}</b>
            <div style={{marginTop:5}}>Short description for job #{id}...</div>
          </a>
        ))}
      </div>
    </div>
  );
}
