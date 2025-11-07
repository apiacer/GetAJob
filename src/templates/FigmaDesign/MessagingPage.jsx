import React, { useState } from "react";

export default function MessagingPage() {
  const [message, setMessage] = useState("");
  return (
    <div style={{maxWidth:600,margin:"60px auto",padding:37,background:"#fff",borderRadius:10,boxShadow:"0 0 16px #eee"}}>
      <h2 style={{color:"#F5821F",fontWeight:700}}>Messages</h2>
      <div style={{marginTop:25}}>
        <div style={{background:"#fcfcfc",borderRadius:7,padding:"13px",marginBottom:18,boxShadow:"0 1px 7px #eee"}}>
          <b>Employer:</b> Hi, are you available for an interview?
        </div>
        <form>
          <input value={message} onChange={e=>setMessage(e.target.value)}
            placeholder="Type your reply..."
            style={{width:"100%",padding:"9px",borderRadius:6,border:"1px solid #f3ece8",marginBottom:9}}
          />
          <button
            type="submit"
            style={{
              background:"#F5821F",color:"#fff",border:"none",borderRadius:7,fontWeight:700,
              padding:"10px 18px",fontSize:"1.06em"
            }}>Send</button>
        </form>
      </div>
    </div>
  );
}
