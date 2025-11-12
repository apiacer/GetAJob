import React from "react";

export default function SignedInLandingPage() {
  return (
    <div style={{maxWidth: 900, margin: "40px auto", padding: 32}}>
      <h1 style={{color:"#F5821F", fontWeight:800, fontSize:"2.1rem", marginTop:0}}>Welcome Back to GetAJob!</h1>
      <p style={{fontSize:"1.2rem",marginTop:18}}>Here’s your dashboard overview. Jump to:</p>
      <ul style={{marginTop:18,fontSize:"1.12rem"}}>
        <li><a href="/jobs" style={{color:"#F5821F"}}>Job Listings</a></li>
        <li><a href="/create-listing" style={{color:"#F5821F"}}>Create Listing</a></li>
        <li><a href="/notifications" style={{color:"#F5821F"}}>Notifications</a></li>
        <li><a href="/messaging" style={{color:"#F5821F"}}>Messages</a></li>
        <li><a href="/account" style={{color:"#F5821F"}}>Account</a></li>
        <li><a href="/admin" style={{color:"#F5821F"}}>Admin Panel (if admin)</a></li>
      </ul>
    </div>
  );
}
