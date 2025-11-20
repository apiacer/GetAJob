import React from "react";
import { Link, useLocation } from "react-router-dom";

const styles = {
  nav: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "20px 44px 10px 44px",
    background: "#fff",
    borderBottom: "1px solid #f3ece8",
    height: 68,
    fontFamily: "'Inter', Arial, sans-serif",
    position: "sticky",
    top: 0,
    zIndex: 100,
  },
  left: {
    display: "flex",
    alignItems: "center",
    gap: 16,
  },
  logoCircle: {
    width: 56,
    height: 56,
    borderRadius: "50%",
    background: "#bbe0b2",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "700",
    color: "#307054",
    fontSize: "1.25em",
    marginRight: 14,
  },
  button: {
    background: "#fff",
    color: "#F5821F",
    border: "2px solid #F5821F",
    borderRadius: 7,
    padding: "7px 17px",
    fontWeight: 600,
    cursor: "pointer",
    marginRight: 6,
    textDecoration: "none",
    fontSize: 16,
  },
  right: {
    display: "flex",
    alignItems: "center",
    gap: 18,
  },
  loginBtn: {
    background: "#F5821F",
    color: "#fff",
    border: "none",
    borderRadius: 7,
    padding: "7px 18px",
    fontWeight: 600,
    cursor: "pointer",
    fontSize: 16,
    marginLeft: 12,
    textDecoration: "none",
  }
};

export default function Layout({ children }) {
  const location = useLocation();
  return (
    <div>
      <nav style={styles.nav}>
        {/* Left side: Logo and Previous Page */}
        <div style={styles.left}>
          <Link to="/">
            <div style={styles.logoCircle}>GetAJob</div>
          </Link>
          {location.pathname !== "/" && (
            <Link to={-1} style={styles.button}>Previous Page</Link>
          )}
        </div>
        {/* Right side: Nav links */}
        <div style={styles.right}>
          <Link to="/jobs" style={styles.button}>Find Jobs</Link>
          <Link to="/search" style={styles.button}>Maps</Link>
          <Link to="/login" style={styles.loginBtn}>Log In</Link>
        </div>
      </nav>
      <main>{children}</main>
    </div>
  );
}
