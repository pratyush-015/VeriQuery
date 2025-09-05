import { useState } from "react";
import AnimatedButton from "./AnimatedButton";

export default function QueryForm({ onQuery }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();

  const BACKEND_URL = "http://localhost:8000";

  const submit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return setError("Type your question.");
    setError(null);
    setLoading(true);
    await onQuery(query, setError);
    setLoading(false);
  };

  

  return (
    <form onSubmit={submit} className="mb-8 bg-white rounded shadow p-6">
      <h2 className="text-xl font-bold mb-3 text-indigo-700">Ask a Question</h2>
      <input
        type="text"
        className="border border-gray-300 rounded px-4 py-2 w-full mb-4 focus:ring-2 focus:ring-indigo-300"
        placeholder='e.g. "46M, knee surgery, Pune, 3-month policy"'
        value={query}
        onChange={e => setQuery(e.target.value)}
        disabled={loading}
      />
      <AnimatedButton type="submit" disabled={loading}>
        {loading ? "Processing..." : "Submit"}
      </AnimatedButton>
      {error && <div className="text-red-500 mt-2">{error}</div>}
    </form>
  );
}
