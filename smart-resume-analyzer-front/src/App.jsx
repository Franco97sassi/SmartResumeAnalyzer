import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [text, setText] = useState("");
  const [answer, setAnswer] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadPdf = async () => {
    if (!file) {
      alert("Seleccioná un PDF");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setAnswer("");

    try {
      const response = await axios.post(`${API_URL}/upload`, formData);
      setAnswer(`PDF indexado correctamente. Chunks: ${response.data.chunks}`);
    } catch (error) {
      setAnswer("Error al subir el PDF");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim()) {
      alert("Escribí una pregunta");
      return;
    }

    setLoading(true);
    setAnswer("");

    try {
      const response = await axios.post(`${API_URL}/ask`, {
        question,
      });

      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer("Error al preguntar");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const analyzeText = async () => {
    if (!text.trim()) {
      alert("Pegá un texto o CV");
      return;
    }

    setLoading(true);
    setAnalysis("");

    try {
      const response = await axios.post(`${API_URL}/analyze`, {
        text,
      });

      setAnalysis(response.data.analysis);
    } catch (error) {
      setAnalysis("Error al analizar texto");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <section className="card">
        <h1>Smart Resume Analyzer AI</h1>
        <p className="subtitle">
          Frontend para probar FastAPI + LangChain + Ollama + RAG
        </p>

        <div className="grid">
          <div className="panel">
            <h2>1. Subir PDF</h2>

            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <button onClick={uploadPdf} disabled={loading}>
              Subir e indexar PDF
            </button>
          </div>

          <div className="panel">
            <h2>2. Preguntar sobre PDF</h2>

            <input
              type="text"
              placeholder="Ej: ¿Qué tecnologías menciona?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />

            <button onClick={askQuestion} disabled={loading}>
              Preguntar
            </button>
          </div>
        </div>

        <div className="panel">
          <h2>3. Analizar texto o CV</h2>

          <textarea
            placeholder="Pegá acá un CV o texto técnico..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />

          <button onClick={analyzeText} disabled={loading}>
            Analizar texto
          </button>
        </div>

        {loading && <p className="loading">Procesando...</p>}

        {answer && (
          <div className="result">
            <h2>Respuesta RAG</h2>
            <pre>{answer}</pre>
          </div>
        )}

        {analysis && (
          <div className="result">
            <h2>Análisis</h2>
            <pre>{analysis}</pre>
          </div>
        )}
      </section>
    </main>
  );
}

export default App;