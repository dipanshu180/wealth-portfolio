import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, AreaChart, Area
} from "recharts";
import { 
  BarChart3, PieChart as PieChartIcon, TrendingUp, Users, 
  DollarSign, Target, Activity, Download, Eye, Filter, Table
} from "lucide-react";
import "./DataVisualization.css";

const DataVisualization = ({ data, queryType, isLoading }) => {
  const [activeTab, setActiveTab] = useState('chart');
  const [chartType, setChartType] = useState('bar');

  // Sample data for demonstration
  const sampleData = {
    portfolioAnalysis: [
      { name: 'Amitabh Bachchan', value: 45000000, risk: 'High', manager: 'Sarah Smith' },
      { name: 'Shah Rukh Khan', value: 38000000, risk: 'High', manager: 'Mike Johnson' },
      { name: 'Virat Kohli', value: 32000000, risk: 'Medium', manager: 'Sarah Smith' },
      { name: 'MS Dhoni', value: 28000000, risk: 'Medium', manager: 'Lisa Chen' },
      { name: 'Sachin Tendulkar', value: 25000000, risk: 'Low', manager: 'Mike Johnson' }
    ],
    managerPerformance: [
      { name: 'Sarah Smith', clients: 8, totalValue: 85000000, avgValue: 10625000 },
      { name: 'Mike Johnson', clients: 12, totalValue: 120000000, avgValue: 10000000 },
      { name: 'Lisa Chen', clients: 6, totalValue: 75000000, avgValue: 12500000 },
      { name: 'David Lee', clients: 10, totalValue: 95000000, avgValue: 9500000 }
    ],
    riskDistribution: [
      { name: 'High Risk', value: 45, color: '#ef4444' },
      { name: 'Medium Risk', value: 35, color: '#f59e0b' },
      { name: 'Low Risk', value: 20, color: '#10b981' }
    ],
    investmentTrends: [
      { month: 'Jan', realEstate: 40, stocks: 35, bonds: 25 },
      { month: 'Feb', realEstate: 42, stocks: 38, bonds: 20 },
      { month: 'Mar', realEstate: 45, stocks: 40, bonds: 15 },
      { month: 'Apr', realEstate: 48, stocks: 42, bonds: 10 },
      { month: 'May', realEstate: 50, stocks: 45, bonds: 5 }
    ]
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatLargeNumber = (value) => {
    if (value >= 10000000) {
      return `${(value / 10000000).toFixed(1)} Cr`;
    } else if (value >= 100000) {
      return `${(value / 100000).toFixed(1)} L`;
    }
    return value.toLocaleString();
  };

  const renderChart = () => {
    let chartData = [];
    let chartConfig = {};

    switch (queryType) {
      case 'topPortfolios':
        chartData = sampleData.portfolioAnalysis.slice(0, 5);
        chartConfig = {
          dataKey: 'value',
          nameKey: 'name',
          title: 'Top 5 Investors by Portfolio Value',
          format: formatCurrency
        };
        break;
      case 'managerBreakdown':
        chartData = sampleData.managerPerformance;
        chartConfig = {
          dataKey: 'totalValue',
          nameKey: 'name',
          title: 'Portfolio Values by Relationship Manager',
          format: formatCurrency
        };
        break;
      case 'riskDistribution':
        chartData = sampleData.riskDistribution;
        chartConfig = {
          dataKey: 'value',
          nameKey: 'name',
          title: 'Risk Distribution',
          format: (value) => `${value}%`
        };
        break;
      case 'investmentTrends':
        chartData = sampleData.investmentTrends;
        chartConfig = {
          dataKey: 'realEstate',
          nameKey: 'month',
          title: 'Investment Trends',
          format: (value) => `${value}%`
        };
        break;
      default:
        chartData = sampleData.portfolioAnalysis;
        chartConfig = {
          dataKey: 'value',
          nameKey: 'name',
          title: 'Portfolio Analysis',
          format: formatCurrency
        };
    }

    switch (chartType) {
      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey={chartConfig.nameKey} 
                stroke="rgba(255,255,255,0.7)"
                fontSize={12}
              />
              <YAxis 
                stroke="rgba(255,255,255,0.7)"
                fontSize={12}
                tickFormatter={chartConfig.format}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(0,0,0,0.9)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '8px',
                  color: '#ffffff'
                }}
                formatter={(value) => [chartConfig.format(value), 'Value']}
              />
              <Legend />
              <Bar dataKey={chartConfig.dataKey} fill="#667eea" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={120}
                fill="#8884d8"
                dataKey={chartConfig.dataKey}
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color || COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(0,0,0,0.9)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '8px',
                  color: '#ffffff'
                }}
                formatter={(value) => [chartConfig.format(value), 'Value']}
              />
            </PieChart>
          </ResponsiveContainer>
        );

      case 'line':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey={chartConfig.nameKey} 
                stroke="rgba(255,255,255,0.7)"
                fontSize={12}
              />
              <YAxis 
                stroke="rgba(255,255,255,0.7)"
                fontSize={12}
                tickFormatter={chartConfig.format}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(0,0,0,0.9)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '8px',
                  color: '#ffffff'
                }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="realEstate" 
                stroke="#667eea" 
                strokeWidth={3}
                dot={{ fill: '#667eea', strokeWidth: 2, r: 6 }}
              />
              <Line 
                type="monotone" 
                dataKey="stocks" 
                stroke="#10b981" 
                strokeWidth={3}
                dot={{ fill: '#10b981', strokeWidth: 2, r: 6 }}
              />
              <Line 
                type="monotone" 
                dataKey="bonds" 
                stroke="#f59e0b" 
                strokeWidth={3}
                dot={{ fill: '#f59e0b', strokeWidth: 2, r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'area':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey={chartConfig.nameKey} 
                stroke="rgba(255,255,255,0.7)"
                fontSize={12}
              />
              <YAxis 
                stroke="rgba(255,255,255,0.7)"
                fontSize={12}
                tickFormatter={chartConfig.format}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(0,0,0,0.9)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '8px',
                  color: '#ffffff'
                }}
              />
              <Legend />
              <Area 
                type="monotone" 
                dataKey={chartConfig.dataKey} 
                stroke="#667eea" 
                fill="#667eea" 
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        );

      default:
        return null;
    }
  };

  const renderTable = () => {
    let tableData = [];
    let columns = [];

    switch (queryType) {
      case 'topPortfolios':
        tableData = sampleData.portfolioAnalysis.slice(0, 5);
        columns = [
          { header: 'Investor Name', accessor: 'name' },
          { header: 'Portfolio Value', accessor: 'value', format: formatCurrency },
          { header: 'Risk Appetite', accessor: 'risk' },
          { header: 'Relationship Manager', accessor: 'manager' }
        ];
        break;
      case 'managerBreakdown':
        tableData = sampleData.managerPerformance;
        columns = [
          { header: 'Manager Name', accessor: 'name' },
          { header: 'Total Clients', accessor: 'clients' },
          { header: 'Total Value', accessor: 'totalValue', format: formatCurrency },
          { header: 'Average Value', accessor: 'avgValue', format: formatCurrency }
        ];
        break;
      default:
        tableData = sampleData.portfolioAnalysis;
        columns = [
          { header: 'Investor Name', accessor: 'name' },
          { header: 'Portfolio Value', accessor: 'value', format: formatCurrency },
          { header: 'Risk Appetite', accessor: 'risk' },
          { header: 'Relationship Manager', accessor: 'manager' }
        ];
    }

    return (
      <div className="table-container">
        <div className="custom-table">
          <table>
            <thead>
              <tr>
                {columns.map((column, index) => (
                  <th key={index} className="table-header">
                    {column.header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.map((row, rowIndex) => (
                <tr key={rowIndex} className="table-row">
                  {columns.map((column, colIndex) => (
                    <td key={colIndex} className="table-cell">
                      {column.format ? column.format(row[column.accessor]) : row[column.accessor]}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  const renderStats = () => {
    const stats = [
      { 
        title: 'Total Portfolio Value', 
        value: '₹2.5 Cr', 
        icon: DollarSign, 
        color: '#10b981',
        change: '+12.5%'
      },
      { 
        title: 'Active Clients', 
        value: '156', 
        icon: Users, 
        color: '#667eea',
        change: '+8.2%'
      },
      { 
        title: 'Top Manager', 
        value: 'Sarah Smith', 
        icon: Target, 
        color: '#f59e0b',
        change: '₹85 Cr'
      },
      { 
        title: 'Avg Portfolio', 
        value: '₹1.6 Cr', 
        icon: Activity, 
        color: '#ef4444',
        change: '+15.3%'
      }
    ];

    return (
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <motion.div
            key={index}
            className="stat-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="stat-icon" style={{ backgroundColor: stat.color + '20' }}>
              <stat.icon size={24} color={stat.color} />
            </div>
            <div className="stat-content">
              <h3 className="stat-title">{stat.title}</h3>
              <p className="stat-value">{stat.value}</p>
              <span className="stat-change" style={{ color: stat.color }}>
                {stat.change}
              </span>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  if (isLoading) {
    return (
      <motion.div 
        className="visualization-loading"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div className="loading-spinner"></div>
        <p>Generating visualizations...</p>
      </motion.div>
    );
  }

  return (
    <motion.div 
      className="data-visualization"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="viz-header">
        <div className="viz-title">
          <BarChart3 size={24} />
          <h2>Data Visualization</h2>
        </div>
        <div className="viz-controls">
          <select 
            value={chartType} 
            onChange={(e) => setChartType(e.target.value)}
            className="chart-type-select"
          >
            <option value="bar">Bar Chart</option>
            <option value="pie">Pie Chart</option>
            <option value="line">Line Chart</option>
            <option value="area">Area Chart</option>
          </select>
          <button className="export-btn">
            <Download size={16} />
            Export
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-section">
        {renderStats()}
      </div>

      {/* Tabs */}
      <div className="viz-tabs">
        <button 
          className={`tab-btn ${activeTab === 'chart' ? 'active' : ''}`}
          onClick={() => setActiveTab('chart')}
        >
          <BarChart3 size={16} />
          Chart
        </button>
        <button 
          className={`tab-btn ${activeTab === 'table' ? 'active' : ''}`}
          onClick={() => setActiveTab('table')}
        >
          <Table size={16} />
          Table
        </button>
        <button 
          className={`tab-btn ${activeTab === 'insights' ? 'active' : ''}`}
          onClick={() => setActiveTab('insights')}
        >
          <Eye size={16} />
          Insights
        </button>
      </div>

      {/* Content */}
      <div className="viz-content">
        <AnimatePresence mode="wait">
          {activeTab === 'chart' && (
            <motion.div
              key="chart"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="chart-container"
            >
              {renderChart()}
            </motion.div>
          )}

          {activeTab === 'table' && (
            <motion.div
              key="table"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="table-container"
            >
              {renderTable()}
            </motion.div>
          )}

          {activeTab === 'insights' && (
            <motion.div
              key="insights"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="insights-container"
            >
              <div className="insight-card">
                <h3>Key Insights</h3>
                <ul>
                  <li>Top 5 portfolios account for 35% of total AUM</li>
                  <li>Sarah Smith manages the highest value portfolios</li>
                  <li>High-risk clients show 15% better returns</li>
                  <li>Real estate investments are trending upward</li>
                </ul>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default DataVisualization; 