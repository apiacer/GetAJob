import React from "react";

// Example avatars, swap with real images later.
const testimonials = [
  {
    text: "I never found a job so quick",
    name: "Herky",
    role: "Contractor",
    avatar: "🧑"
  },
  {
    text: "I love the design of this site!",
    name: "Benjamin Franklin",
    role: "Client",
    avatar: "🧔"
  },
  {
    text: "So much better than Indeed",
    name: "Mike Tyson",
    role: "Client",
    avatar: "🧑"
  }
];

export default function LandingPage() {
  return (
    <div style={{
      fontFamily: "'Inter', Arial, sans-serif",
      background: "#fff",
      color: "#333",
      padding: "0 0 60px 0"
    }}>
      <div style={{
        margin: "0 auto",
        maxWidth: 970,
        background: "#fff",
        boxShadow: "0 0 30px #eee",
        borderRadius: 8,
        padding: "35px 36px 38px 36px",
        marginTop: 40
      }}>
        <div style={{
          textAlign: "center",
          margin: "15px 0 8px 0",
          color: "#F5821F",
          fontWeight: 800,
          fontSize: "3.4rem"
        }}>GetAJob</div>
        <div style={{
          textAlign: "center",
          color: "#F5821F",
          fontWeight: 500,
          fontSize: "1.3rem"
        }}>Your user friendly job finder</div>
        <div style={{
          textAlign: "center",
          marginTop: 30,
          marginBottom: 15,
          color: "#F5821F",
          fontWeight: 700,
          fontSize: "1.35rem"
        }}>
          Only one step away from finding your future
        </div>
        <div style={{textAlign:"center", marginBottom:40}}>
          <a
            href="/jobs"
            style={{
              background: "#F5821F",
              color: "#fff",
              borderRadius: 6,
              fontWeight: 700,
              fontSize: "1.13rem",
              padding: "15px 34px",
              boxShadow: "0 3px 18px #ffeed6",
              textDecoration: "none"
            }}
          >Get Started</a>
        </div>
        {/* Purpose Section */}
        <div style={{
          color: "#F5821F",
          fontWeight: 700,
          fontSize: "1.5rem",
          marginBottom: 10
        }}>Our Purpose</div>
        <div style={{
          display:"flex",gap:32,justifyContent:"space-between",marginBottom:15
        }}>
          <div style={{
            flex:1,background:"#fcfcfc",borderRadius:8,
            padding:"24px 19px 10px 19px",boxShadow:"0 2px 15px #eee",
            display:"flex",flexDirection:"column",alignItems:"center",minHeight:230
          }}>
            <div style={{
              width:"96px", height:"80px", background:"#f7f2ee",
              borderRadius:8, marginBottom:18
            }}>
              {/* Community illustration */}
              <span role="img" aria-label="community" style={{fontSize:"3em",position:"relative",top:"12px",left:"20px"}}>🧑‍🤝‍🧑</span>
            </div>
            <div style={{color:"#F5821F", fontWeight:700, fontSize:"1.06rem",marginBottom:7}}>
              Helping our community find jobs
            </div>
            <div style={{fontSize:"1rem",marginBottom:0,textAlign:"center",color:"#363636"}}>
              Nowadays finding job opportunities is difficult, that's where we come in. Our goal is help others find employment, whether it be odd jobs or tenured positions, we have it.
            </div>
          </div>
          <div style={{
            flex:1,background:"#fcfcfc",borderRadius:8,
            padding:"24px 19px 10px 19px",boxShadow:"0 2px 15px #eee",
            display:"flex",flexDirection:"column",alignItems:"center",minHeight:230
          }}>
            <div style={{
              width:"96px", height:"80px", background:"#f7f2ee",
              borderRadius:8, marginBottom:18
            }}>
              <span role="img" aria-label="audience" style={{fontSize:"3em",position:"relative",top:"12px",left:"20px"}}>👥</span>
            </div>
            <div style={{color:"#F5821F", fontWeight:700, fontSize:"1.06rem",marginBottom:7}}>
              Our Audience
            </div>
            <div style={{fontSize:"1rem",marginBottom:0,textAlign:"center",color:"#363636"}}>
              No matter who you are or where you are, everyone is welcome to use our website. We welcome everyone no matter the situation.
            </div>
          </div>
          <div style={{
            flex:1,background:"#fcfcfc",borderRadius:8,
            padding:"24px 19px 10px 19px",boxShadow:"0 2px 15px #eee",
            display:"flex",flexDirection:"column",alignItems:"center",minHeight:230
          }}>
            <div style={{
              width:"96px", height:"80px", background:"#f7f2ee",
              borderRadius:8, marginBottom:18
            }}>
              <span role="img" aria-label="features" style={{fontSize:"3em",position:"relative",top:"12px",left:"20px"}}>💼</span>
            </div>
            <div style={{color:"#F5821F", fontWeight:700, fontSize:"1.06rem",marginBottom:7}}>
              What We Can Do
            </div>
            <div style={{fontSize:"1rem",marginBottom:0,textAlign:"center",color:"#363636"}}>
              Enjoy our filtered search, mapping features, easy-2-use interface, fast application and more!
            </div>
          </div>
        </div>
        {/* Testimonials */}
        <div style={{display:"flex",gap:22,marginTop:18,justifyContent:"center"}}>
          {testimonials.map(testi => (
            <div key={testi.name}
              style={{
                background:"#fff",borderRadius:7,boxShadow:"0 1px 7px #eee",
                padding:"15px 20px",fontSize:"1.07rem",minWidth:210,
                textAlign:"center",display:"flex",flexDirection:"column",alignItems:"center"
              }}>
              <div style={{fontStyle:"italic",marginBottom:6}}>“{testi.text}”</div>
              <div style={{display:"flex", alignItems:"center", gap:8,marginTop:3}}>
                <div style={{fontSize:"1.4em"}}>{testi.avatar}</div>
                <div style={{fontWeight:"700"}}>{testi.name}</div>
              </div>
              <div style={{fontSize:"0.97rem",color:"#666"}}>{testi.role}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
