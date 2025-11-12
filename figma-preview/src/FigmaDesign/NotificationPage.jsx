import React from "react";

export default function NotificationPage() {
  return (
    <div style={{maxWidth:660,margin:"60px auto",padding:37,background:"#fff",borderRadius:10,boxShadow:"0 0 14px #eee"}}>
      <h2 style={{color:"#F5821F",fontWeight:700}}>Notifications</h2>
      <div style={{marginTop:30}}>
        <div style={{background:"#fcfcfc",borderRadius:7,padding:"14px 18px",marginBottom:13,boxShadow:"0 1px 7px #eee"}}>
          You have a new message about your application to Job #2.
        </div>
        <div style={{background:"#fcfcfc",borderRadius:7,padding:"14px 18px",marginBottom:13,boxShadow:"0 1px 7px #eee"}}>
          Your job listing #11 was approved.
        </div>
      </div>
    </div>
  );
}
