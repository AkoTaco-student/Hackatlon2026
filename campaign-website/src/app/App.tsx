import { Routes, Route } from "react-router-dom";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import ScrollToTop from "@/components/layout/ScrollToTop";
import Home from "@/pages/Home";
import Issues from "@/pages/Issues";
import IssueDetail from "@/pages/IssueDetail";
import Program from "@/pages/Program";
import Team from "@/pages/Team";
import Faq from "@/pages/Faq";

export default function App() {
  return (
    <div className="min-h-screen bg-background">
      <ScrollToTop />
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/saker" element={<Issues />} />
          <Route path="/saker/:id" element={<IssueDetail />} />
          <Route path="/program" element={<Program />} />
          <Route path="/team" element={<Team />} />
          <Route path="/faq" element={<Faq />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
