import React, { useState } from "react";

export default function LeaveRatingPage() {
  const [rating, setRating] = useState(4);
  const [comment, setComment] = useState("");
  return (
    <div style={{maxWidth:440,margin:"60px auto",padding:34,background:"#fff",borderRadius:10,boxShadow:"0 0 14px #eee"}}>
      <h2 style={{color:"#F5821F",fontWeight:700}}>Leave a Rating</h2>
      <form>
        <label>Rating:<br/>
          {[1,2,3,4,5].map(num=>(
            <span key={num} style={{fontSize:"2em",marginRight:7,cursor:"pointer"}}
              onClick={()=>setRating(num)}>
              {num <= rating ? "★" : "☆"}
            </span>
          ))}
        </label>
        <textarea
          value={comment}
          onChange={e=>setComment(e.target.value)}
          placeholder="Add a comment..."
          style={{width:"100%",height:"70px",marginTop:12,padding:"9px",borderRadius:7,border:"1px solid #f3ece8"}}
        />
        <button type="submit"
          style={{
            background:"#F5821F", color:"#fff", border:"none", borderRadius:7,
            padding:"12px 27px",fontWeight:700,fontSize:"1.07em", width:"100%",marginTop:15
          }}>
          Submit Rating
        </button>
      </form>
    </div>
  );
}
