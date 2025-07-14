import React from "react";
import { motion } from "framer-motion";
import { Toaster } from "react-hot-toast";
import ChatInterface from "./components/ChatInterface";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
      
      {/* Animated Background */}
      <div className="background-animation">
        <div className="gradient-bg"></div>
        <div className="floating-shapes">
          <div className="shape shape-1"></div>
          <div className="shape shape-2"></div>
          <div className="shape shape-3"></div>
          <div className="shape shape-4"></div>
          <div className="shape shape-5"></div>
        </div>
      </div>

      {/* Header */}
      <motion.header 
        className="header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="header-content">
          <motion.div 
            className="logo"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <div className="logo-icon">💼</div>
            <div className="logo-text">
              <h1>Valuefy</h1>
              <span>AI Portfolio Assistant</span>
            </div>
          </motion.div>
          
          <div className="header-stats">
            <div className="stat">
              <span className="stat-number">24/7</span>
              <span className="stat-label">Available</span>
            </div>
            <div className="stat">
              <span className="stat-number">AI</span>
              <span className="stat-label">Powered</span>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <motion.main 
        className="main-content"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <ChatInterface />
      </motion.main>

      {/* Footer */}
      <motion.footer 
        className="footer"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.4 }}
      >
        <div className="footer-content">
          <p>Powered by Advanced AI Technology</p>
          <div className="footer-links">
            <span>🔒 Secure</span>
            <span>⚡ Fast</span>
            <span>🎯 Accurate</span>
          </div>
        </div>
      </motion.footer>
    </div>
  );
}

export default App;
