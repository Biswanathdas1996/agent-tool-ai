import React from "react";
import { Route, Routes } from "react-router-dom";
import ChatWithUnstructure from "./pages/ChatWithUnstructure";
import CodeReview from "./pages/CodeReview";
import CodeDoc from "./pages/CodeDoc";
import CodeTransformation from "./pages/CodeTransformation";
import Layout from "./layout/index";
import SimpleAlert from "./components/Alert";
import PageLoader from "./components/PageLoader";
import WelComeComp from "./components/WelcomeChatComp";
// -------------user stoty use case---------------
import UserStoryGeneration from "./pages/UserStoryGeneration";
import Backlog from "./pages/Code/Backlog";
import Upload from "./pages/Upload";
import Config from "./pages/Config";
import ImgToHtml from "./pages/ImgToHtml";
import CompareCode from "./pages/CompareCode";
import Interview from "./pages/Interview";
import GenerateSwiftData from "./pages/GenerateSwiftData";

function App() {
  return (
    <>
      <SimpleAlert />
      <Layout>
        <PageLoader />

        <Routes>
          <Route
            path="/home"
            element={
              <>
                <h2>Home</h2>
                <WelComeComp />
              </>
            }
          />

          <Route path="/data-chat" element={<ChatWithUnstructure />} />
          <Route path="/code-review" element={<CodeReview />} />
          <Route path="/code-doc" element={<CodeDoc />} />
          <Route path="/img-html" element={<ImgToHtml />} />
          <Route path="/story" element={<UserStoryGeneration />} />
          <Route path="/backlog/story" element={<UserStoryGeneration />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/backlog" element={<Backlog />} />
          <Route path="/compare-code" element={<CompareCode />} />
          <Route path="/config" element={<Config />} />
          <Route path="/interview" element={<Interview />} />
          <Route path="/generate-swift-data" element={<GenerateSwiftData />} />
          <Route path="/code-transformation" element={<CodeTransformation />} />
        </Routes>
      </Layout>
    </>
  );
}

export default App;
