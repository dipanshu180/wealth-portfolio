# Natural Language Query System

## Overview
 Natural Language Query System is a full-stack investment management platform that leverages both SQL (MySQL) and MongoDB databases. The backend is built with Python (FastAPI), and the frontend is developed using React (Vite). This project demonstrates integration with real, production-like databases for robust data management and analytics.

---

## Features
- Manage and analyze investment transactions
- Dual-database support: MySQL (for structured data) and MongoDB (for flexible, unstructured data)
- Modern React frontend
- FastAPI backend

---

## Folder Structure
```
valuefy/
  backend/      # FastAPI backend, database connectors, agents
  frontend/     # React frontend (Vite)
```

---

## Prerequisites
- Python 3.11+
  React Js
- MySQL Server
- MongoDB Server

---

## Database Setup

### 1. MySQL (SQL) Setup

#### Create Database and Table
```sql
CREATE DATABASE valuefy;
USE valuefy;

DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    transactoin_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id VARCHAR(30),
    stock_name VARCHAR(50),
    amount_invested FLOAT,
    date_ DATE,
    rm_name VARCHAR(50)
);
```

#### Insert Sample Data
```sql
INSERT INTO transactions (client_id, stock_name, amount_invested, date_, rm_name) VALUES
('C001', 'TCS', 1500000, '2025-01-01', 'Ravi Sharma'),
('C001', 'INFY', 900000, '2025-06-20', 'Ravi Sharma'),
('C001', 'RELIANCE', 600000, '2025-05-10', 'Ravi Sharma'),
('C002', 'HDFC', 2500000, '2025-02-10', 'Sneha Mehta'),
('C002', 'Bonds', 500000, '2025-04-12', 'Sneha Mehta'),
('C003', 'BTC', 1200000, '2025-03-15', 'Ravi Sharma'),
('C003', 'WIPRO', 1000000, '2025-04-01', 'Ravi Sharma'),
('C003', 'ETH', 700000, '2025-07-05', 'Ravi Sharma'),
('C004', 'FD', 500000, '2024-11-25', 'Amit Verma'),
('C004', 'GOLD', 300000, '2025-01-25', 'Amit Verma'),
('C005', 'RELIANCE', 1800000, '2025-04-01', 'Simran Kaur'),
('C005', 'ETH', 800000, '2025-05-01', 'Simran Kaur'),
('C006', 'BTC', 1400000, '2025-03-10', 'Simran Kaur'),
('C006', 'NFT Project X', 650000, '2025-05-15', 'Simran Kaur'),
('C007', 'FD', 700000, '2024-12-01', 'Amit Verma'),
('C007', 'Gold', 200000, '2025-06-15', 'Amit Verma'),
('C008', 'TCS', 1600000, '2025-06-01', 'Sneha Mehta'),
('C009', 'INFY', 2100000, '2025-06-05', 'Ravi Sharma'),
('C009', 'CryptoX', 950000, '2025-07-10', 'Ravi Sharma'),
('C010', 'Mutual Fund A', 1300000, '2025-03-12', 'Simran Kaur'),
('C011', 'Real Estate Project X', 2500000, '2025-01-20', 'Ravi Sharma'),
('C012', 'Gold', 900000, '2025-04-05', 'Amit Verma'),
('C013', 'ETH', 1000000, '2025-05-10', 'Ravi Sharma'),
('C014', 'FD', 600000, '2025-04-12', 'Amit Verma'),
('C015', 'Mutual Fund B', 1100000, '2025-04-22', 'Sneha Mehta'),
('C016', 'WIPRO', 1400000, '2025-05-30', 'Sneha Mehta'),
('C017', 'NFT Project Z', 1700000, '2025-07-01', 'Ravi Sharma'),
('C017', 'BTC', 1200000, '2025-07-09', 'Ravi Sharma'),
('C018', 'Gold', 800000, '2025-02-05', 'Amit Verma'),
('C019', 'Bonds', 600000, '2025-03-28', 'Sneha Mehta'),
('C020', 'BTC', 1600000, '2025-06-25', 'Ravi Sharma'),
('C020', 'TCS', 700000, '2025-07-01', 'Ravi Sharma'),
('C003', 'CryptoX', 450000, '2025-07-12', 'Ravi Sharma'),
('C006', 'NFT Project Y', 560000, '2025-07-13', 'Simran Kaur'),
('C009', 'RELIANCE', 820000, '2025-07-10', 'Ravi Sharma'),
('C001', 'BTC', 780000, '2025-07-05', 'Ravi Sharma'),
('C020', 'WIPRO', 870000, '2025-06-28', 'Ravi Sharma'),
('C005', 'INFY', 610000, '2025-07-11', 'Simran Kaur'),
('C017', 'NFT Project Z', 400000, '2025-07-10', 'Ravi Sharma'),
('C014', 'FD', 220000, '2025-06-20', 'Amit Verma'),
('C011', 'Real Estate Project Y', 1750000, '2025-07-01', 'Ravi Sharma'),
('C016', 'CryptoX', 950000, '2025-07-12', 'Sneha Mehta');
```

---

### 2. MongoDB Setup

#### Sample Document Structure
```json
{
  "client_id": "C001",
  "portfolio": [
    { "asset": "TCS", "type": "Stock", "amount": 1500000, "date": "2025-01-01" },
    { "asset": "INFY", "type": "Stock", "amount": 900000, "date": "2025-06-20" }
  ],
  "rm_name": "Ravi Sharma"
}
```

#### Example: Insert 25 Sample Documents
```js
use valuefy;
db.clients.insertMany([
  { "client_id": "C001", "portfolio": [ { "asset": "TCS", "type": "Stock", "amount": 1500000, "date": "2025-01-01" }, { "asset": "INFY", "type": "Stock", "amount": 900000, "date": "2025-06-20" } ], "rm_name": "Ravi Sharma" },
  { "client_id": "C002", "portfolio": [ { "asset": "HDFC", "type": "Stock", "amount": 2500000, "date": "2025-02-10" }, { "asset": "Bonds", "type": "Bond", "amount": 500000, "date": "2025-04-12" } ], "rm_name": "Sneha Mehta" },
  { "client_id": "C003", "portfolio": [ { "asset": "BTC", "type": "Crypto", "amount": 1200000, "date": "2025-03-15" }, { "asset": "WIPRO", "type": "Stock", "amount": 1000000, "date": "2025-04-01" }, { "asset": "ETH", "type": "Crypto", "amount": 700000, "date": "2025-07-05" } ], "rm_name": "Ravi Sharma" },
  { "client_id": "C004", "portfolio": [ { "asset": "FD", "type": "Fixed Deposit", "amount": 500000, "date": "2024-11-25" }, { "asset": "GOLD", "type": "Commodity", "amount": 300000, "date": "2025-01-25" } ], "rm_name": "Amit Verma" },
  { "client_id": "C005", "portfolio": [ { "asset": "RELIANCE", "type": "Stock", "amount": 1800000, "date": "2025-04-01" }, { "asset": "ETH", "type": "Crypto", "amount": 800000, "date": "2025-05-01" } ], "rm_name": "Simran Kaur" },
  { "client_id": "C006", "portfolio": [ { "asset": "BTC", "type": "Crypto", "amount": 1400000, "date": "2025-03-10" }, { "asset": "NFT Project X", "type": "NFT", "amount": 650000, "date": "2025-05-15" } ], "rm_name": "Simran Kaur" },
  { "client_id": "C007", "portfolio": [ { "asset": "FD", "type": "Fixed Deposit", "amount": 700000, "date": "2024-12-01" }, { "asset": "Gold", "type": "Commodity", "amount": 200000, "date": "2025-06-15" } ], "rm_name": "Amit Verma" },
  { "client_id": "C008", "portfolio": [ { "asset": "TCS", "type": "Stock", "amount": 1600000, "date": "2025-06-01" } ], "rm_name": "Sneha Mehta" },
  { "client_id": "C009", "portfolio": [ { "asset": "INFY", "type": "Stock", "amount": 2100000, "date": "2025-06-05" }, { "asset": "CryptoX", "type": "Crypto", "amount": 950000, "date": "2025-07-10" } ], "rm_name": "Ravi Sharma" },
  { "client_id": "C010", "portfolio": [ { "asset": "Mutual Fund A", "type": "Mutual Fund", "amount": 1300000, "date": "2025-03-12" } ], "rm_name": "Simran Kaur" },
  { "client_id": "C011", "portfolio": [ { "asset": "Real Estate Project X", "type": "Real Estate", "amount": 2500000, "date": "2025-01-20" } ], "rm_name": "Ravi Sharma" },
  { "client_id": "C012", "portfolio": [ { "asset": "Gold", "type": "Commodity", "amount": 900000, "date": "2025-04-05" } ], "rm_name": "Amit Verma" },
  { "client_id": "C013", "portfolio": [ { "asset": "ETH", "type": "Crypto", "amount": 1000000, "date": "2025-05-10" } ], "rm_name": "Ravi Sharma" },
  { "client_id": "C014", "portfolio": [ { "asset": "FD", "type": "Fixed Deposit", "amount": 600000, "date": "2025-04-12" }, { "asset": "FD", "type": "Fixed Deposit", "amount": 220000, "date": "2025-06-20" } ], "rm_name": "Amit Verma" },
  { "client_id": "C015", "portfolio": [ { "asset": "Mutual Fund B", "type": "Mutual Fund", "amount": 1100000, "date": "2025-04-22" } ], "rm_name": "Sneha Mehta" },
  { "client_id": "C016", "portfolio": [ { "asset": "WIPRO", "type": "Stock", "amount": 1400000, "date": "2025-05-30" }, { "asset": "CryptoX", "type": "Crypto", "amount": 950000, "date": "2025-07-12" } ], "rm_name": "Sneha Mehta" },
  { "client_id": "C017", "portfolio": [ { "asset": "NFT Project Z", "type": "NFT", "amount": 1700000, "date": "2025-07-01" }, { "asset": "BTC", "type": "Crypto", "amount": 1200000, "date": "2025-07-09" }, { "asset": "NFT Project Z", "type": "NFT", "amount": 400000, "date": "2025-07-10" } ], "rm_name": "Ravi Sharma" },
  { "client_id": "C018", "portfolio": [ { "asset": "Gold", "type": "Commodity", "amount": 800000, "date": "2025-02-05" } ], "rm_name": "Amit Verma" },
  { "client_id": "C019", "portfolio": [ { "asset": "Bonds", "type": "Bond", "amount": 600000, "date": "2025-03-28" } ], "rm_name": "Sneha Mehta" },
  { "client_id": "C020", "portfolio": [ { "asset": "BTC", "type": "Crypto", "amount": 1600000, "date": "2025-06-25" }, { "asset": "TCS", "type": "Stock", "amount": 700000, "date": "2025-07-01" }, { "asset": "WIPRO", "type": "Stock", "amount": 870000, "date": "2025-06-28" } ], "rm_name": "Ravi Sharma" },
  { "client_id": "C021", "portfolio": [ { "asset": "ETH", "type": "Crypto", "amount": 500000, "date": "2025-07-15" } ], "rm_name": "Simran Kaur" },
  { "client_id": "C022", "portfolio": [ { "asset": "Mutual Fund C", "type": "Mutual Fund", "amount": 1200000, "date": "2025-06-10" } ], "rm_name": "Sneha Mehta" },
  { "client_id": "C023", "portfolio": [ { "asset": "Real Estate Project Y", "type": "Real Estate", "amount": 1750000, "date": "2025-07-01" } ], "rm_name": "Ravi Sharma" },
  { "client_id": "C024", "portfolio": [ { "asset": "CryptoX", "type": "Crypto", "amount": 450000, "date": "2025-07-12" } ], "rm_name": "Ravi Sharma" },
  { "client_id": "C025", "portfolio": [ { "asset": "NFT Project Y", "type": "NFT", "amount": 560000, "date": "2025-07-13" } ], "rm_name": "Simran Kaur" }
]);
```

---

## Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. (Optional) Create and activate a virtual environment:
   ```sh
   python -m venv myenv
   myenv\Scripts\activate  # On Windows
   # or
   source myenv/bin/activate  # On Mac/Linux
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure your `.env` file for database credentials (see `.env.example` if available).
5. Run the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```

---

## Frontend Setup (React + Vite)

1. Navigate to the frontend directory:
   ```sh
   cd frontend/val_frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```

---

## Usage
- Access the frontend at `http://localhost:5173` (default Vite port)
- FastAPI backend runs at `http://localhost:8000` by default
- Ensure both SQL and MongoDB servers are running and accessible

---

## Notes
- **Security:** Do not commit sensitive credentials. Use `.env` files and add them to `.gitignore`.
- **.gitignore:** Make sure to exclude `myenv/`, `node_modules/`, and `.env` files from version control.
- **Data:** The provided SQL and MongoDB data are for demonstration. Adjust as needed for production.

---

## Example Business Queries & Answers

### 1. What are the top five portfolios of our wealth members?

#### SQL (MySQL)
```sql
SELECT client_id, SUM(amount_invested) AS total_portfolio_value
FROM transactions
GROUP BY client_id
ORDER BY total_portfolio_value DESC
LIMIT 5;
```
**Answer (sample):**
| client_id | total_portfolio_value |
|-----------|----------------------|
| C011      | 4250000              |
| C002      | 3000000              |
| C017      | 3300000              |
| C009      | 3870000              |
| C001      | 3780000              |

#### MongoDB
```js
db.clients.aggregate([
  { $unwind: "$portfolio" },
  { $group: { _id: "$client_id", total_portfolio_value: { $sum: "$portfolio.amount" } } },
  { $sort: { total_portfolio_value: -1 } },
  { $limit: 5 }
]);
```
**Answer:**
Returns the top 5 clients with the highest total portfolio value.

---

### 2. Give me the breakup of portfolio values per relationship manager.

#### SQL (MySQL)
```sql
SELECT rm_name, SUM(amount_invested) AS total_value
FROM transactions
GROUP BY rm_name;
```
**Answer (sample):**
| rm_name      | total_value |
|--------------|------------|
| Ravi Sharma  | 15000000   |
| Sneha Mehta  | 9000000    |
| Amit Verma   | 6000000    |
| Simran Kaur  | 8000000    |

#### MongoDB
```js
db.clients.aggregate([
  { $unwind: "$portfolio" },
  { $group: { _id: "$rm_name", total_value: { $sum: "$portfolio.amount" } } }
]);
```
**Answer:**
Returns the total portfolio value managed by each relationship manager.

---

### 3. Tell me the top relationship managers in my firm

#### SQL (MySQL)
```sql
SELECT rm_name, SUM(amount_invested) AS total_value
FROM transactions
GROUP BY rm_name
ORDER BY total_value DESC
LIMIT 3;
```
**Answer (sample):**
| rm_name      | total_value |
|--------------|------------|
| Ravi Sharma  | 15000000   |
| Sneha Mehta  | 9000000    |
| Simran Kaur  | 8000000    |

#### MongoDB
```js
db.clients.aggregate([
  { $unwind: "$portfolio" },
  { $group: { _id: "$rm_name", total_value: { $sum: "$portfolio.amount" } } },
  { $sort: { total_value: -1 } },
  { $limit: 3 }
]);
```
**Answer:**
Returns the top 3 relationship managers by total portfolio value managed.

---

### 4. Which clients are the highest holders of [specific stock]?

#### SQL (MySQL)
```sql
SELECT client_id, SUM(amount_invested) AS total_invested
FROM transactions
WHERE stock_name = 'TCS' -- Replace 'TCS' with the desired stock
GROUP BY client_id
ORDER BY total_invested DESC
LIMIT 5;
```
**Answer (sample for TCS):**
| client_id | total_invested |
|-----------|----------------|
| C001      | 1500000        |
| C008      | 1600000        |
| C020      | 700000         |

#### MongoDB
```js
db.clients.aggregate([
  { $unwind: "$portfolio" },
  { $match: { "portfolio.asset": "TCS" } }, // Replace 'TCS' as needed
  { $group: { _id: "$client_id", total_invested: { $sum: "$portfolio.amount" } } },
  { $sort: { total_invested: -1 } },
  { $limit: 5 }
]);
```
**Answer:**
Returns the top 5 clients with the highest investment in the specified stock.

---


