import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User, Sparkles, Zap, RefreshCw, MessageCircle, TrendingUp, Users } from "lucide-react";
import axios from "axios";
import toast from "react-hot-toast";
import DataVisualization from "./DataVisualization";
import "./ChatInterface.css";

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [showVisualization, setShowVisualization] = useState(false);
  const [visualizationData, setVisualizationData] = useState(null);
  const [queryType, setQueryType] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Enhanced query suggestions
  const suggestions = [
    "Show me the top 5 investors",
    "Who are the high risk clients?",
    "Top 3 transactions by amount",
    "Clients who invest in stocks",
    "Highest investment amounts",
    "Show me the names of all clients"
  ];

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: "user",
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/ask`, {
        question: inputValue
      }, {
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json',
        }
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.answer || "No response received.",
        sender: "bot",
        timestamp: new Date(),
        processingTime: response.data.processing_time
      };

      setMessages(prev => [...prev, botMessage]);
      
      // Enhanced visualization detection
      const query = inputValue.toLowerCase();
      let newQueryType = '';
      
      // Improved detection logic
      if (query.includes('top') && (query.includes('investor') || query.includes('client') || query.includes('portfolio'))) {
        newQueryType = 'topPortfolios';
        setShowVisualization(true);
        toast.success("📊 Portfolio analysis visualization available!");
      } else if (query.includes('top') && (query.includes('transaction') || query.includes('amount') || query.includes('investment'))) {
        newQueryType = 'topTransactions';
        setShowVisualization(true);
        toast.success("📈 Transaction analysis visualization available!");
      } else if (query.includes('risk') && (query.includes('distribution') || query.includes('appetite'))) {
        newQueryType = 'riskDistribution';
        setShowVisualization(true);
        toast.success("🎯 Risk analysis visualization available!");
      } else if (query.includes('name') || query.includes('who') || query.includes('client')) {
        newQueryType = 'clientList';
        setShowVisualization(true);
        toast.success("👥 Client information visualization available!");
      } else if (query.includes('trend') || query.includes('investment') || query.includes('performance')) {
        newQueryType = 'investmentTrends';
        setShowVisualization(true);
        toast.success("📈 Investment trends visualization available!");
      } else if (query.includes('amount') || query.includes('transaction')) {
        newQueryType = 'transactionAnalysis';
        setShowVisualization(true);
        toast.success("💰 Transaction analysis visualization available!");
      }
      
      setQueryType(newQueryType);
      setVisualizationData(response.data);
      
      // Provide specific feedback based on query type
      if (query.includes('top') && /\d+/.test(query)) {
        const number = query.match(/\d+/)[0];
        toast.success(`✅ Found top ${number} results as requested!`);
      } else if (query.includes('name') || query.includes('who')) {
        toast.success("✅ Names prioritized in results!");
      }
      
    } catch (error) {
      console.error("API Error:", error);
      
      let errorMessage = "An error occurred while processing your request.";
      if (error.response) {
        errorMessage = `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = "Network error: Unable to connect to server.";
      }

      const errorBotMessage = {
        id: Date.now() + 1,
        text: errorMessage,
        sender: "bot",
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorBotMessage]);
      toast.error("Failed to get response");
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputValue(suggestion);
    inputRef.current?.focus();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setShowVisualization(false);
    setVisualizationData(null);
    setQueryType('');
    toast.success("Chat cleared!");
  };

  return (
    <motion.div 
      className="chat-interface"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Chat Container */}
      <div className="chat-container glass">
        {/* Chat Header */}
        <div className="chat-header">
          <div className="chat-header-content">
            <div className="chat-title">
              <Bot className="chat-icon" />
              <div>
                <h2>AI Portfolio Assistant</h2>
                <span>Ask me anything about your portfolio data</span>
              </div>
            </div>
            <motion.button
              className="clear-btn"
              onClick={clearChat}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              disabled={messages.length === 0}
            >
              <RefreshCw size={16} />
              Clear
            </motion.button>
          </div>
        </div>

        {/* Messages Area */}
        <div className="messages-area">
          <AnimatePresence>
            {messages.length === 0 && (
              <motion.div 
                className="welcome-message"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <Sparkles className="welcome-icon" />
                <h3>Welcome to Valuefy AI!</h3>
                <p>I'm here to help you analyze your portfolio data. Ask me anything about your clients, portfolios, and investments.</p>
                
                {/* Enhanced suggestions */}
                <div className="suggestions-container">
                  <h4>💡 Try these queries:</h4>
                  <div className="suggestions-grid">
                    {suggestions.map((suggestion, index) => (
                      <motion.button
                        key={index}
                        className="suggestion-btn"
                        onClick={() => handleSuggestionClick(suggestion)}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        {suggestion}
                      </motion.button>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {messages.map((message, index) => (
              <motion.div
                key={message.id}
                className={`message ${message.sender}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="message-avatar">
                  {message.sender === 'user' ? <User size={16} /> : <Bot size={16} />}
                </div>
                <div className="message-content">
                  <div className="message-text">
                    {message.isError ? (
                      <div className="error-message">
                        <span>⚠️ {message.text}</span>
                      </div>
                    ) : (
                      <pre>{message.text}</pre>
                    )}
                  </div>
                  <div className="message-meta">
                    <span className="message-time">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                    {message.processingTime && (
                      <span className="processing-time">
                        <Zap size={12} />
                        {message.processingTime}
                      </span>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}

            {isTyping && (
              <motion.div
                className="message bot typing"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className="message-avatar">
                  <Bot size={16} />
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="input-area">
          <div className="input-container">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about your portfolio data... (e.g., 'top 5 investors', 'show me names')"
              disabled={isLoading}
              rows={1}
              className="message-input"
            />
            <motion.button
              className="send-btn"
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {isLoading ? (
                <div className="loading-spinner" />
              ) : (
                <Send size={18} />
              )}
            </motion.button>
          </div>
        </div>
      </div>

      {/* Data Visualization */}
      {showVisualization && (
        <motion.div
          className="visualization-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <DataVisualization 
            data={visualizationData}
            queryType={queryType}
            isLoading={isLoading}
          />
        </motion.div>
      )}
    </motion.div>
  );
};

export default ChatInterface; 