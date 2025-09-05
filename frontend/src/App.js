import { useState } from "react";
import UploadForm from "./components/uploadform";
import QueryForm from "./components/queryform";
import ResultsDisplay from "./components/resultsdisplay";
import axios from "axios";

export default function App() {
  const [uploadInfo, setUploadInfo] = useState(null);
  const [result, setResult] = useState(null);

  async function handleQuery(query, setError) {
    try {
      const res = await axios.post("http://localhost:8000/query", { question: query });
      setResult(res.data);
      setError && setError(null);
    } catch (error) {
      setError("Query failed: " + (error.response?.data?.detail || error.message));
      setResult(null);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-tr from-indigo-100 via-purple-50 to-pink-100 py-12 px-2">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-extrabold text-indigo-700 mb-1">VeriQuery</h1>
          <p className="text-lg text-gray-600">LLM-powered Semantic Document QA and Explainable Answers</p>
        </div>
        <UploadForm onUploadSuccess={setUploadInfo} />
        <QueryForm onQuery={handleQuery} />
        <ResultsDisplay result={result} />
        <footer className="mt-12 text-center text-gray-400 text-xs">&copy; 2025 VeriQuery</footer>
      </div>
    </div>
  );
}
