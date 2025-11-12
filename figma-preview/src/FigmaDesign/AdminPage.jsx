import React from "react";

export default function AdminPage() {
  return (
    <div style={{maxWidth:660,margin:"60px auto",padding:40,background:"#fff",borderRadius:11,boxShadow:"0 0 18px #eee"}}>
      <h2 style={{color:"#F5821F",fontWeight:800}}>Admin Panel</h2>
      <div style={{marginTop:25}}>
        <b style={{color:"#F5821F"}}>Manage Listings</b>
        <div>
          <a href="/jobs" style={{color:"#F5821F",fontWeight:700,marginRight:13}}>All Listings</a>
          <a href="/create-listing" style={{color:"#F5821F",fontWeight:700}}>Create Listing</a>
        </div>
      </div>
      <div style={{marginTop:32}}>
        <b style={{color:"#F5821F"}}>Manage Users</b>
        <div>
          <span>User management features go here.</span>
        </div>
      </div>
    </div>
  );
}
