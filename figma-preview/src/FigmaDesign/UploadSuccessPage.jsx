import React from "react";
import { Link, useSearchParams } from "react-router-dom";

export default function UploadSuccessPage(){
  const [params] = useSearchParams();
  const id = params.get("id");
  return (
    <div style={{maxWidth:600, margin:"60px auto", padding:28, background:"#fff", borderRadius:12, boxShadow:"0 0 18px #eee", textAlign:"center"}}>
      <h2 style={{color:"#2b7a2b"}}>Job posted successfully</h2>
      {id ? <p>Listing ID: <b>{id}</b></p> : null}
      <p>
        <Link to="/jobs" style={{color:"#F5821F", fontWeight:700}}>Back to Listings</Link>{" · "}
        {id ? <Link to={`/job/${id}`} style={{color:"#F5821F", fontWeight:700}}>View Listing</Link> : null}
      </p>
    </div>
  );
}
