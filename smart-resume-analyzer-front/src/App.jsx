import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [agentQuestion, setAgentQuestion] = useState("");
  const [text, setText] = useState("");
  const [answer, setAnswer] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [agentAnswer, setAgentAnswer] = useState("");
  const [history, setHistory] = useState([]);
  const [apiStatus, setApiStatus] = useState("checking");
  const [apiMessage, setApiMessage] = useState("Verificando conexión con la API...");
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [healthLoading, setHealthLoading] = useState(false);

  const checkHealth = async () => {
    setHealthLoading(true);

    try {
      const response = await axios.get(`${API_URL}/health`);
      setApiStatus("online");
      setApiMessage(
        `${response.data.application} v${response.data.version} está ${response.data.status}`,
      );
    } catch (error) {
      setApiStatus("offline");
      setApiMessage("No se pudo conectar con la API");
      console.error(error);
    } finally {
      setHealthLoading(false);
    }
  };

  useEffect(() => {
    const loadApiStatus = async () => {
      try {
        const response = await axios.get(`${API_URL}/health`);
        setApiStatus("online");
        setApiMessage(
          `${response.data.application} v${response.data.version} está ${response.data.status}`,
        );
      } catch (error) {
        setApiStatus("offline");
        setApiMessage("No se pudo conectar con la API");
        console.error(error);
      }
    };

    loadApiStatus();
  }, []);

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

  const askAgent = async () => {
    if (!agentQuestion.trim()) {
      alert("Escribí una pregunta para el agente");
      return;
    }

    setLoading(true);
    setAgentAnswer("");

    try {
      const response = await axios.post(`${API_URL}/agent`, {
        question: agentQuestion,
      });

      setAgentAnswer(response.data.answer);
    } catch (error) {
      setAgentAnswer("Error al consultar el agente");
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

  const loadHistory = async () => {
    setHistoryLoading(true);

    try {
      const response = await axios.get(`${API_URL}/history`);
      setHistory(response.data);
    } catch (error) {
      setHistory([]);
      console.error(error);
      alert("Error al cargar el historial");
    } finally {
      setHistoryLoading(false);
    }
  };

  return (
    <main className="container">
      <section className="card">
        <h1>Smart Resume Analyzer AI</h1>
         
        <div className="header">
           
 
        </div>

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
               
              Preguntar con RAG
            </button>
          </div>
        </div>

        <div className="grid">
          <div className="panel">
            <h2>3. Preguntar al agente</h2>
            <p className="panel-description">
              El agente decide si responder con RAG, análisis de CV o chat general.
            </p>

            <input
              type="text"
              placeholder="Ej: Según el documento, ¿qué experiencia tiene?"
              value={agentQuestion}
              onChange={(e) => setAgentQuestion(e.target.value)}
            />

            <button onClick={askAgent} disabled={loading}>
              Consultar agente
            </button>
          </div>

          <div className="panel">
            <h2>4. Historial</h2>
            <p className="panel-description">
              Consultas guardadas por el backend después de usar RAG.
            </p>

            <button onClick={loadHistory} disabled={historyLoading}>
              {historyLoading ? "Cargando..." : "Cargar historial"}
            </button>
          </div>
        </div>

        <div className="panel">
           <h2>5. Analizar texto o CV</h2>

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

        {agentAnswer && (
          <div className="result">
            <h2>Respuesta del agente</h2>
            <pre>{agentAnswer}</pre>
          </div>
        )}

        {analysis && (
          <div className="result">
            <h2>Análisis</h2>
            <pre>{analysis}</pre>
          </div>
        )}

        {history.length > 0 && (
          <div className="result">
            <h2>Historial</h2>
            <div className="history-list">
              {history.map((item) => (
                <article className="history-item" key={item.id}>
                  <strong>Pregunta:</strong>
                  <p>{item.question}</p>
                  <strong>Respuesta:</strong>
                  <pre>{item.answer}</pre>
                </article>
              ))}
            </div>
          </div>
        )}
      </section>
    </main>
  );
}

export default App;