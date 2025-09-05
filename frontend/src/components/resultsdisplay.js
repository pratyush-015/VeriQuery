import ClauseHighlighter from "./ClauseHighlighter";

export default function ResultsDisplay({ result, highlight }) {
  if (!result) return null;
  return (
    <div className="bg-white shadow-lg rounded-lg p-8 my-8">
      <h3 className="text-2xl font-bold mb-2 text-indigo-700">Result</h3>
      <div className="mb-3">
        <span className="font-semibold text-gray-800">Decision:</span>{" "}
        <span className={`px-2 py-1 rounded 
          ${result.decision === "approved"
            ? "bg-green-200 text-green-800"
            : "bg-red-200 text-red-800"}
        `}>{result.decision}</span>
      </div>
      {result.amount && (
        <div className="mb-3">
          <span className="font-semibold text-gray-800">Amount:</span> ₹{result.amount}
        </div>
      )}
      <div className="mb-6">
        <span className="font-semibold text-gray-800">Model Answer:</span>
        <div className="mt-1 p-3 bg-gray-100 rounded">{result.answer}</div>
      </div>
      <div>
        <span className="font-semibold text-gray-800">Justification:</span>
        <ul className="list-disc ml-6 mt-2">
          {result.justification?.map((item, idx) => (
            <li key={idx} className="mb-3">
              <div className="text-indigo-600 font-medium">
                {item.decision_component?.replace("_", " ")}
              </div>
              <ClauseHighlighter text={item.text} highlight={highlight} />
            </li>
          ))}
        </ul>
      </div>
      <details className="mt-6">
        <summary className="text-indigo-500 cursor-pointer">Show retrieved clauses</summary>
        <ul className="bg-gray-50 border mt-2 rounded p-2 max-h-56 overflow-y-auto text-xs">
          {result.source_clauses?.map((clause, idx) => (
            <li key={idx} className="mb-2">
              <ClauseHighlighter text={clause} highlight={highlight} />
            </li>
          ))}
        </ul>
      </details>
    </div>
  );
}
