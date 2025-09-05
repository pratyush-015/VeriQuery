import { useState } from "react";
import axios from "axios";
import AnimatedButton from "./AnimatedButton";

export default function UploadForm({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();

  const handleChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  async function handleUpload() {
    if (!file) return setError("Please select a file.");
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await axios.post("http://localhost:8000/upload", formData);
      onUploadSuccess(res.data);
    } catch (err) {
      setError("Upload failed. " + (err.response?.data?.detail || err.message));
    }
    setLoading(false);
  }

  return (
    <div className="mb-8 bg-white rounded shadow p-6">
      <h2 className="text-xl font-bold mb-3 text-indigo-700">Upload Document</h2>
      <input type="file" accept=".pdf,.doc,.docx" onChange={handleChange}
        className="block mb-4" />
      <AnimatedButton onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </AnimatedButton>
      {error && <div className="text-red-500 mt-2">{error}</div>}
    </div>
  );
}
