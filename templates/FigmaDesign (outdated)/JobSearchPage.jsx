import React from "react";

export default function JobSearchPage() {
  return (
    <div style={{maxWidth:900,margin:"50px auto",padding:24}}>
      <h2 style={{color:"#F5821F",fontWeight:710}}>Search/Map Jobs</h2>
      <p>Filter jobs by location, type, and more.</p>
      <div style={{marginTop:20,background:"#fcfcfc",padding:18,borderRadius:8}}>
        <input type="text" placeholder="Search by keyword..." style={{width:"100%",padding:"9px",marginBottom:12,borderRadius:6,border:"1px solid #f3ece8"}}/>
        <div style={{marginTop:12,display:"flex",gap:16}}>
          <input type="text" placeholder="Location" style={{flex:1,padding:"8px",borderRadius:6,border:"1px solid #f3ece8"}}/>
          <input type="text" placeholder="Job Type" style={{flex:1,padding:"8px",borderRadius:6,border:"1px solid #f3ece8"}}/>
        </div>
      </div>
      <div style={{marginTop:36}}>
        {/* Results */}
        {[101,102,103].map(id=>(
          <a key={id} href={`/job/${id}`} style={{
            display:"block",background:"#fff",padding:"18px 17px",borderRadius:8,
            boxShadow:"0 1px 8px #eee",marginBottom:19,textDecoration:"none",color:"#214"
          }}>
            <b style={{color:"#F5821F"}}>Job Title #{id}</b>
            <div style={{marginTop:5}}>Map/location info for job #{id}</div>
          </a>
        ))}
      </div>
    </div>
  );
}
