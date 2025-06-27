import React, { useState } from 'react';

function App() {
  const [keywords, setKeywords] = useState('');
  const [alerts, setAlerts] = useState([]);

  const fetchAlerts = async () => {
    const res = await fetch(`https://veille-backend.onrender.com/veille?mots_cles=${keywords}`);
    const data = await res.json();
    setAlerts(data);
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Veille Municipale</h1>
      <input
        className="border px-2 py-1 w-full mb-4"
        placeholder="Entrez des mots-clés (ex: piste cyclable, Saint-Pierre)"
        value={keywords}
        onChange={(e) => setKeywords(e.target.value)}
      />
      <button onClick={fetchAlerts} className="bg-blue-500 text-white px-4 py-2 rounded">Lancer la veille</button>

      <div className="mt-6 space-y-4">
        {alerts.map((a, i) => (
          <div key={i} className="border p-4 rounded shadow">
            <div className="text-sm text-gray-600">{a.date} | {a.source} | {a.auteur}</div>
            <div className="mt-2">{a.contenu}</div>
            <a href={a.lien} target="_blank" rel="noreferrer" className="text-blue-600 underline text-sm">Voir la source</a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;