export default function ClauseHighlighter({ text, highlight }) {
  if (!highlight) return <span>{text}</span>;
  const idx = text.toLowerCase().indexOf(highlight.toLowerCase());
  if (idx === -1) return <span>{text}</span>;
  return (
    <span>
      {text.substring(0, idx)}
      <mark className="bg-yellow-200 font-semibold">{text.substring(idx, idx + highlight.length)}</mark>
      {text.substring(idx + highlight.length)}
    </span>
  );
}
