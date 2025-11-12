import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./FigmaDesign/Layout.jsx";
import LandingPage from "./FigmaDesign/LandingPage.jsx";
import JobListingPage from "./FigmaDesign/JobListingPage.jsx";
import LoginPage from "./FigmaDesign/LoginPage.jsx";
import MapsPage from "./FigmaDesign/JobSearchPage.jsx";
import ViewListingPage from "./FigmaDesign/ViewListingPage.jsx";
import LeaveRatingPage from "./FigmaDesign/LeaveRatingPage.jsx";
import MessagingPage from "./FigmaDesign/MessagingPage.jsx";
import CreateListingPage from "./FigmaDesign/CreateListingPage.jsx";
import NotificationPage from "./FigmaDesign/NotificationPage.jsx";
import SignupPage from "./FigmaDesign/SignupPage.jsx";
import SignedInLandingPage from "./FigmaDesign/SignedInLandingPage.jsx";
import AdminPage from "./FigmaDesign/AdminPage.jsx";
import AccountPage from "./FigmaDesign/AccountPage.jsx";
import JobSearchPage from "./FigmaDesign/JobSearchPage.jsx";
import EditListingPage from "./FigmaDesign/EditListingPage.jsx";
import UploadSuccessPage from "./FigmaDesign/UploadSuccessPage.jsx";


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/jobs" element={<JobListingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/search" element={<MapsPage />} />
          <Route path="/job/:id" element={<ViewListingPage />} />
          <Route path="/leave-rating" element={<LeaveRatingPage />} />
          <Route path="/messaging" element={<MessagingPage />} />
          <Route path="/create-listing" element={<CreateListingPage />} />
          <Route path="/notifications" element={<NotificationPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/dashboard" element={<SignedInLandingPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/account" element={<AccountPage />} />
          <Route path="/job-search" element={<JobSearchPage />} />
          <Route path="/jobs" element={<JobListingPage />} />
          <Route path="/job/:id" element={<ViewListingPage />} />
          <Route path="/edit/:id" element={<EditListingPage />} />
          <Route path="/create-listing" element={<CreateListingPage />} />
          <Route path="/create-success" element={<UploadSuccessPage />} />
        </Route>
        <Route path="*" element={<div>Not Found</div>} />
      </Routes>
    </BrowserRouter>
  );
}
