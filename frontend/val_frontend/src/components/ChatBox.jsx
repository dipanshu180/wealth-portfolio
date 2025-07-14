import React, { useState, useEffect } from "react";
import axios from "axios";

const ChatBox = () => {
  console.log("ChatBox component rendering...");
  
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [retryCount, setRetryCount] = useState(0);

  // Get API URL from environment or use default
  const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
  
  console.log("API_BASE_URL:", API_BASE_URL);

  const handleAsk = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setResponse("");
    setError("");

    try {
      const res = await axios.post(`${API_BASE_URL}/ask`, {
        question,
      }, {
        timeout: 30000, // 30 second timeout
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (res.data.error) {
        setError("❌ Error: " + res.data.error);
        setResponse("");
      } else {
        setResponse(res.data.answer || "No response received.");
        setError("");
        setRetryCount(0); // Reset retry count on success
      }
    } catch (err) {
      console.error("API Error:", err);
      
      if (err.response) {
        // Server responded with error status
        const status = err.response.status;
        let errorMessage = `🚨 Server error (${status})`;
        
        if (status === 400) {
          errorMessage += ": Invalid request. Please check your question format.";
        } else if (status === 500) {
          errorMessage += ": Internal server error. Please try again later.";
        } else if (status === 503) {
          errorMessage += ": Service temporarily unavailable. Please try again.";
        } else {
          errorMessage += `: ${err.response.data?.error || err.message}`;
        }
        
        setError(errorMessage);
      } else if (err.request) {
        // Network error
        if (retryCount < 3) {
          setRetryCount(prev => prev + 1);
          setError(`🚨 Network error (Attempt ${retryCount + 1}/3): Retrying...`);
          
          // Retry after 2 seconds
          setTimeout(() => {
            handleAsk();
          }, 2000);
          return;
        } else {
          setError("🚨 Network error: Unable to connect to server. Please check your internet connection and try again.");
        }
      } else {
        // Other error
        setError("🚨 Error: " + err.message);
      }
      
      setResponse("");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  const clearAll = () => {
    setQuestion("");
    setResponse("");
    setError("");
    setRetryCount(0);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>💼 Portfolio AI Assistant</h1>
      <p style={styles.subtitle}>Ask your investment queries in natural language.</p>

      <div style={styles.inputContainer}>
        <textarea
          rows={4}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder='Example: "Top 5 investors in Real Estate?" or "Show me transactions above ₹10,000"'
          style={styles.textarea}
          disabled={loading}
        />

        <div style={styles.buttonContainer}>
          <button 
            onClick={handleAsk} 
            disabled={loading || !question.trim()} 
            style={{
              ...styles.button,
              opacity: loading || !question.trim() ? 0.6 : 1
            }}
          >
            {loading ? "Thinking..." : "Ask the Bot"}
          </button>
          
          <button 
            onClick={clearAll} 
            style={styles.clearButton}
            disabled={loading}
          >
            Clear
          </button>
        </div>
      </div>

      {error && (
        <div style={styles.errorBox}>
          <strong>⚠️ Error:</strong>
          <div style={styles.errorText}>{error}</div>
        </div>
      )}

      {response && (
        <div style={styles.responseBox}>
          <strong>🧠 Answer:</strong>
          <pre style={styles.codeBlock}>{response}</pre>
        </div>
      )}

      {loading && (
        <div style={styles.loadingBox}>
          <div style={styles.spinner}></div>
          <span>Processing your query...</span>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: "2rem",
    maxWidth: "800px",
    margin: "auto",
    background: "#f9fafb",
    borderRadius: "12px",
    boxShadow: "0 10px 20px rgba(0,0,0,0.08)",
    minHeight: "100vh",
  },
  title: {
    fontSize: "2rem",
    fontWeight: "bold",
    background: "linear-gradient(90deg, #2563eb, #9333ea)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    textAlign: "center",
    marginBottom: "0.5rem",
  },
  subtitle: {
    fontSize: "1rem",
    color: "#4b5563",
    marginBottom: "2rem",
    textAlign: "center",
  },
  inputContainer: {
    marginBottom: "1.5rem",
  },
  textarea: {
    width: "100%",
    padding: "1rem",
    fontSize: "1rem",
    border: "1px solid #d1d5db",
    borderRadius: "8px",
    outline: "none",
    marginBottom: "1rem",
    fontFamily: "inherit",
    resize: "vertical",
    minHeight: "100px",
  },
  buttonContainer: {
    display: "flex",
    gap: "1rem",
    justifyContent: "center",
  },
  button: {
    background: "#2563eb",
    color: "white",
    padding: "0.75rem 1.5rem",
    fontSize: "1rem",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "all 0.3s",
    fontWeight: "600",
  },
  clearButton: {
    background: "#6b7280",
    color: "white",
    padding: "0.75rem 1.5rem",
    fontSize: "1rem",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "all 0.3s",
  },
  errorBox: {
    marginTop: "1.5rem",
    background: "#fef2f2",
    padding: "1rem",
    borderRadius: "8px",
    border: "1px solid #fecaca",
    color: "#dc2626",
  },
  errorText: {
    marginTop: "0.5rem",
    whiteSpace: "pre-wrap",
    fontSize: "0.9rem",
  },
  responseBox: {
    marginTop: "1.5rem",
    background: "#e0f2fe",
    padding: "1rem",
    borderRadius: "8px",
    border: "1px solid #bae6fd",
    whiteSpace: "pre-wrap",
  },
  codeBlock: {
    fontFamily: "monospace",
    fontSize: "1rem",
    marginTop: "0.5rem",
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
  },
  loadingBox: {
    marginTop: "1.5rem",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "0.5rem",
    padding: "1rem",
    background: "#f3f4f6",
    borderRadius: "8px",
  },
  spinner: {
    width: "20px",
    height: "20px",
    border: "2px solid #e5e7eb",
    borderTop: "2px solid #2563eb",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
};

// Add CSS animation for spinner
const style = document.createElement('style');
style.textContent = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);

export default ChatBox;
