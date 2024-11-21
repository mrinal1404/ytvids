import React, { useState } from "react";
import axios from "axios";

function App() {
  const [resumeText, setResumeText] = useState("");
  const [role, setRole] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [videos, setVideos] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze-resume", {
        resume_text: resumeText,
        role: role,
      });
      setAnalysis(response.data.analysis);
      setVideos(response.data.videos || []);
    } catch (error) {
      console.error("Error analyzing resume:", error);
      alert("An error occurred. Please try again.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Resume Role Analyzer</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Role:</label>
          <input
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Resume Text:</label>
          <textarea
            rows="10"
            cols="50"
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            required
          />
        </div>
        <button type="submit">Analyze</button>
      </form>

      {analysis && (
        <div>
          <h2>Analysis</h2>
          <p>{analysis}</p>
        </div>
      )}

      {videos.length > 0 && (
        <div>
          <h2>Suggested YouTube Videos</h2>
          <ul>
            {videos.map((video, index) => (
              <li key={index}>
                <a href={video} target="_blank" rel="noopener noreferrer">
                  {video}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;

