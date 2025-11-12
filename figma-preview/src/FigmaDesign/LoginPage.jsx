import React, { useState } from "react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  return (
    <div style={{maxWidth:400,margin:"60px auto", padding:36, background:"#fff",borderRadius:8,boxShadow:"0 0 16px #eee"}}>
      <h2 style={{color:"#F5821F",fontWeight:"700",textAlign:"center"}}>Log In</h2>
      <form>
        <label style={{display:"block",marginBottom:12}}>Email
          <input value={email} onChange={e=>setEmail(e.target.value)}
            type="email" required style={{width:"100%",padding:"9px",marginTop:5,borderRadius:6,border:"1px solid #f3ece8"}}
            placeholder="you@example.com"
          />
        </label>
        <label style={{display:"block",marginBottom:18}}>Password
          <input value={password} onChange={e=>setPassword(e.target.value)}
            type="password" required style={{width:"100%",padding:"9px",marginTop:5,borderRadius:6,border:"1px solid #f3ece8"}}
            placeholder="••••••••"
          />
        </label>
        <button type="submit"
          style={{
            background:"#F5821F", color:"#fff", border:"none", borderRadius:7,
            padding:"12px 27px",fontWeight:700,fontSize:"1.04em", width:"100%",marginBottom:10
          }}>
          Log In
        </button>
        <div style={{textAlign:"center",marginTop:13}}>
          <a href="/signup" style={{color:"#F5821F"}}>Don't have an account? Sign up</a>
        </div>
      </form>
    </div>
  );
}
