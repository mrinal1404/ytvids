import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [file, setFile] = useState(null);
    const [role, setRole] = useState('');
    const [videos, setVideos] = useState([]);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            alert('Please select a file');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:5000/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setRole(response.data.role);
            setVideos(response.data.videos);
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Failed to upload resume');
        }
    };

    return (
        <div className="App">
            <h1>Resume Role Detection</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload Resume</button>

            {role && <h2>Detected Role: {role}</h2>}
            {videos.length > 0 && (
                <div>
                    <h3>Recommended Videos:</h3>
                    <ul>
                        {videos.map((video, index) => (
                            <li key={index}>
                                <a href={video.url} target="_blank" rel="noopener noreferrer">
                                    {video.title}
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