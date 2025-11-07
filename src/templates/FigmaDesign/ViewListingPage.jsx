import React from "react";
import { useParams } from "react-router-dom";

export default function ViewListingPage() {
  const { id } = useParams();
  return (
    <div style={{maxWidth:750,margin:"50px auto",padding:28,background:"#fff",borderRadius:12,boxShadow:"0 0 18px #eee"}}>
      <h2 style={{color:"#F5821F",fontWeight:710}}>Job Listing Details</h2>
      <b style={{fontSize:"1.25em",color:"#F5821F",marginBottom:10, display: "block"}}>Job Title #{id}</b>
      <div style={{marginBottom:12}}>Full description for job #{id}... (location, salary, etc.)</div>
      <div>
        <a href="/leave-rating" style={{marginRight:24,color:"#F5821F",fontWeight:700}}>Leave Rating</a>
        <a href="/messaging" style={{marginRight:24,color:"#F5821F",fontWeight:700}}>Message Employer</a>
        <a href="/jobs" style={{color:"#F5821F",fontWeight:700}}>Back to Listings</a>
      </div>
    </div>
  );
}
