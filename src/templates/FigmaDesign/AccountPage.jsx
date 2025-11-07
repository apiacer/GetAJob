import React from "react";

export default function AccountPage() {
  return (
    <div style={{maxWidth:530,margin:"60px auto",padding:38,background:"#fff",borderRadius:10,boxShadow:"0 0 15px #eee"}}>
      <h2 style={{color:"#F5821F",fontWeight:700}}>Your Account</h2>
      <div style={{marginTop:28,marginBottom:13}}>
        <label>Name:<input type="text" value="Demo User" readOnly style={{width:"100%",padding:"9px",marginTop:5,borderRadius:6,border:"1px solid #f3ece8"}}/></label>
      </div>
      <div style={{marginBottom:13}}>
        <label>Email:<input type="text" value="demo@getajob.com" readOnly style={{width:"100%",padding:"9px",marginTop:5,borderRadius:6,border:"1px solid #f3ece8"}}/></label>
      </div>
      <div style={{marginBottom:13}}>
        <label>Password: <input type="password" value="••••••••" readOnly style={{width:"100%",padding:"9px",marginTop:5,borderRadius:6,border:"1px solid #f3ece8"}}/></label>
      </div>
      <a href="/leave-rating" style={{color:"#F5821F",fontWeight:700}}>Your Ratings</a>
    </div>
  );
}
