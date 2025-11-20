import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import LandingPage from "./LandingPage";
import SignedInLandingPage from "./SignedInLandingPage";
import LoginPage from "./LoginPage";
import SignupPage from "./SignupPage";
import JobListingPage from "./JobListingPage";
import JobSearchPage from "./JobSearchPage";
import ViewListingPage from "./ViewListingPage";
import AccountPage from "./AccountPage";
import AdminPage from "./AdminPage";
import CreateListingPage from "./CreateListingPage";
import NotificationPage from "./NotificationPage";
import MessagingPage from "./MessagingPage";
import LeaveRatingPage from "./LeaveRatingPage";

export default function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/home" element={<SignedInLandingPage />} />
          <Route path="/jobs" element={<JobListingPage />} />
          <Route path="/search" element={<JobSearchPage />} />
          <Route path="/job/:id" element={<ViewListingPage />} />
          <Route path="/account" element={<AccountPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/create-listing" element={<CreateListingPage />} />
          <Route path="/notifications" element={<NotificationPage />} />
          <Route path="/messaging" element={<MessagingPage />} />
          <Route path="/leave-rating" element={<LeaveRatingPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}
