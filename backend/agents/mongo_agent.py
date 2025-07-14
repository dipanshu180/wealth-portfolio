# agents/mongo_agent.py

from db.mongo_conn import get_mongo_collection
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import ast
import json
import time
import re

load_dotenv()

# COMPLETELY DISABLE REAL MONGODB - ALWAYS USE MOCK DATA
MONGODB_AVAILABLE = False
collection = None
print("🔧 Using mock data mode for all MongoDB queries - Real MongoDB disabled")

# Setup LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

template = """
You are a MongoDB query generator for a client portfolio database.
The MongoDB collection is called `clients`. Each document looks like this:
{{
  "client_id": "C001",
  "name": "Virat Kohli",
  "risk_appetite": "High",
  "investment_preferences": ["Stocks", "Real Estate"],
  "rm_id": "RM001",
  "portfolio_value": 2500000
}}

IMPORTANT RULES:
1. For "top N" queries, use .limit(N) in the query
2. For sorting, use .sort() with appropriate fields
3. Always prioritize returning names over IDs in the response
4. Use proper MongoDB aggregation syntax when needed
5. For "top investors", sort by portfolio_value or risk_appetite
6. For "relationship managers", look for rm_id or rm_name fields
7. For "portfolios", consider portfolio_value field
8. Return ONLY the MongoDB query in JSON format, no explanation
9. DO NOT use $size operator - it causes errors
10. Use simple find queries with basic filters

Convert the user's question into a MongoDB query in JSON format.

User Question: "{question}"

MongoDB Query:"""

prompt = PromptTemplate.from_template(template)

def query_mongo(question: str):
    start = time.time()

    try:
        # ALWAYS use mock responses - force mock mode
        print(f"🔧 Processing query with mock data: {question}")
        return get_mock_response(question, start)
        
    except Exception as e:
        print(f"❌ Error in mock response: {str(e)}")
        return {
            "answer": f"Error processing query: {str(e)}",
            "query": question,
            "processing_time": f"{time.time() - start:.2f}s"
        }

def parse_question(question: str):
    """Parse the question to extract specific requirements"""
    question_lower = question.lower()
    
    parsed = {
        'limit': None,
        'sort_by': None,
        'sort_order': 1,  # 1 for ascending, -1 for descending
        'top_n': False,
        'names_only': False,
        'portfolio_focus': False,
        'rm_focus': False
    }
    
    # Extract limit number
    limit_match = re.search(r'top\s+(\d+)', question_lower)
    if limit_match:
        parsed['limit'] = int(limit_match.group(1))
        parsed['top_n'] = True
    
    # Check for name-specific queries
    if 'name' in question_lower or 'who' in question_lower:
        parsed['names_only'] = True
    
    # Check for portfolio-focused queries
    if 'portfolio' in question_lower or 'wealth' in question_lower or 'investor' in question_lower:
        parsed['portfolio_focus'] = True
        parsed['sort_by'] = 'portfolio_value'
        parsed['sort_order'] = -1  # Highest first
    
    # Check for relationship manager queries
    if 'relationship manager' in question_lower or 'rm' in question_lower:
        parsed['rm_focus'] = True
        parsed['sort_by'] = 'rm_id'
    
    # Determine sort criteria
    if 'high' in question_lower and 'risk' in question_lower:
        parsed['sort_by'] = 'risk_appetite'
        parsed['sort_order'] = -1  # High risk first
    elif 'low' in question_lower and 'risk' in question_lower:
        parsed['sort_by'] = 'risk_appetite'
        parsed['sort_order'] = 1  # Low risk first
    elif 'top' in question_lower and not parsed['sort_by']:
        parsed['sort_by'] = 'name'  # Default sort by name for top queries
    
    return parsed

def get_mock_response(question: str, start_time: float):
    """Provide mock responses when MongoDB is not available"""
    question_lower = question.lower()
    
    # Enhanced mock client data with portfolio values and RM info
    mock_clients = [
        {"name": "Virat Kohli", "client_id": "C001", "risk_appetite": "High", "investment_preferences": ["Stocks", "Real Estate"], "portfolio_value": 5000000, "rm_id": "RM001"},
        {"name": "Rohit Sharma", "client_id": "C002", "risk_appetite": "Medium", "investment_preferences": ["Stocks", "Bonds"], "portfolio_value": 3500000, "rm_id": "RM002"},
        {"name": "MS Dhoni", "client_id": "C003", "risk_appetite": "Low", "investment_preferences": ["Bonds", "Fixed Deposits"], "portfolio_value": 2000000, "rm_id": "RM003"},
        {"name": "KL Rahul", "client_id": "C004", "risk_appetite": "High", "investment_preferences": ["Stocks", "Real Estate", "Crypto"], "portfolio_value": 4500000, "rm_id": "RM001"},
        {"name": "Rishabh Pant", "client_id": "C005", "risk_appetite": "Medium", "investment_preferences": ["Stocks", "Mutual Funds"], "portfolio_value": 3000000, "rm_id": "RM002"},
        {"name": "Hardik Pandya", "client_id": "C006", "risk_appetite": "High", "investment_preferences": ["Stocks", "Real Estate"], "portfolio_value": 4000000, "rm_id": "RM001"},
        {"name": "Deepika Padukone", "client_id": "C007", "risk_appetite": "Medium", "investment_preferences": ["Stocks", "Bonds"], "portfolio_value": 2800000, "rm_id": "RM003"},
        {"name": "Salman Khan", "client_id": "C008", "risk_appetite": "High", "investment_preferences": ["Real Estate", "Stocks"], "portfolio_value": 6000000, "rm_id": "RM001"},
        {"name": "Shah Rukh Khan", "client_id": "C009", "risk_appetite": "High", "investment_preferences": ["Stocks", "Real Estate"], "portfolio_value": 5500000, "rm_id": "RM002"},
        {"name": "Dinesh Karthik", "client_id": "C010", "risk_appetite": "Medium", "investment_preferences": ["Stocks", "Mutual Funds"], "portfolio_value": 2500000, "rm_id": "RM003"}
    ]
    
    # Parse the question
    parsed_query = parse_question(question)
    
    # Handle specific client ID queries
    client_id_match = re.search(r'client\s+([A-Z]\d+)', question_lower)
    if not client_id_match:
        client_id_match = re.search(r'([A-Z]\d+)', question_lower)
    
    if client_id_match:
        client_id = client_id_match.group(1)
        client = next((c for c in mock_clients if c['client_id'] == client_id), None)
        if client:
            answer = f"Client {client_id} is {client['name']} (Risk: {client['risk_appetite']}, Portfolio: ₹{client['portfolio_value']:,})"
        else:
            answer = f"Client {client_id} not found in the database."
        return {
            "answer": answer,
            "query": question,
            "processing_time": f"{time.time() - start_time:.2f}s"
        }
    
    # Handle "who is" queries for specific names
    if 'who is' in question_lower:
        # Extract potential names from the question
        for client in mock_clients:
            if client['name'].lower() in question_lower:
                answer = f"{client['name']} is Client {client['client_id']} (Risk: {client['risk_appetite']}, Portfolio: ₹{client['portfolio_value']:,})"
                return {
                    "answer": answer,
                    "query": question,
                    "processing_time": f"{time.time() - start_time:.2f}s"
                }
    
    # Handle top portfolios/wealth members/investors
    if 'top' in question_lower and ('portfolio' in question_lower or 'wealth member' in question_lower or 'wealth members' in question_lower or 'investor' in question_lower):
        limit = parsed_query['limit'] or 5
        sorted_clients = sorted(mock_clients, key=lambda x: x['portfolio_value'], reverse=True)
        top_clients = sorted_clients[:limit]
        client_info = [f"• {c['name']} (Portfolio: ₹{c['portfolio_value']:,})" for c in top_clients]
        answer = f"Top {limit} investors:\n" + "\n".join(client_info)
        return {
            "answer": answer,
            "query": question,
            "processing_time": f"{time.time() - start_time:.2f}s"
        }
    
    # Handle top relationship managers
    if 'top' in question_lower and ('relationship manager' in question_lower or 'rm' in question_lower):
        # Group by RM and sum portfolio values
        rm_groups = {}
        for client in mock_clients:
            rm_id = client['rm_id']
            if rm_id not in rm_groups:
                rm_groups[rm_id] = 0
            rm_groups[rm_id] += client['portfolio_value']
        sorted_rms = sorted(rm_groups.items(), key=lambda x: x[1], reverse=True)
        limit = parsed_query['limit'] or 5
        top_rms = sorted_rms[:limit]
        rm_info = [f"• {rm_id} (Total Portfolio: ₹{total:,})" for rm_id, total in top_rms]
        answer = f"Top {limit} relationship managers:\n" + "\n".join(rm_info)
        return {
            "answer": answer,
            "query": question,
            "processing_time": f"{time.time() - start_time:.2f}s"
        }
    
    # Handle group-by/aggregation queries for relationship managers
    if ('breakup' in question_lower or 'breakdown' in question_lower or 'group by' in question_lower) and ('relationship manager' in question_lower or 'rm' in question_lower):
        # Group by RM and sum portfolio values
        rm_groups = {}
        for client in mock_clients:
            rm_id = client['rm_id']
            if rm_id not in rm_groups:
                rm_groups[rm_id] = 0
            rm_groups[rm_id] += client['portfolio_value']
        rm_info = [f"• {rm_id}: ₹{total:,}" for rm_id, total in rm_groups.items()]
        answer = f"Portfolio value breakup per relationship manager:\n" + "\n".join(rm_info)
        return {
            "answer": answer,
            "query": question,
            "processing_time": f"{time.time() - start_time:.2f}s"
        }
    
    # Filter and sort based on question
    filtered_clients = mock_clients.copy()
    
    # Apply filters
    if 'high' in question_lower and 'risk' in question_lower:
        filtered_clients = [c for c in filtered_clients if c['risk_appetite'] == 'High']
    elif 'low' in question_lower and 'risk' in question_lower:
        filtered_clients = [c for c in filtered_clients if c['risk_appetite'] == 'Low']
    elif 'medium' in question_lower and 'risk' in question_lower:
        filtered_clients = [c for c in filtered_clients if c['risk_appetite'] == 'Medium']
    elif 'stocks' in question_lower:
        filtered_clients = [c for c in filtered_clients if 'Stocks' in c['investment_preferences']]
    elif 'real estate' in question_lower or 'property' in question_lower:
        filtered_clients = [c for c in filtered_clients if 'Real Estate' in c['investment_preferences']]
    
    # Apply sorting
    if parsed_query['sort_by'] == 'risk_appetite':
        risk_order = {'High': 3, 'Medium': 2, 'Low': 1}
        if parsed_query['sort_order'] == -1:  # High first
            filtered_clients.sort(key=lambda x: risk_order.get(x['risk_appetite'], 0), reverse=True)
        else:  # Low first
            filtered_clients.sort(key=lambda x: risk_order.get(x['risk_appetite'], 0))
    elif parsed_query['sort_by'] == 'portfolio_value':
        # Sort by portfolio value
        filtered_clients.sort(key=lambda x: x['portfolio_value'], reverse=(parsed_query['sort_order'] == -1))
    else:
        # Sort by name
        filtered_clients.sort(key=lambda x: x['name'])
    
    # Apply limit
    if parsed_query['limit']:
        filtered_clients = filtered_clients[:parsed_query['limit']]
    
    # Format response
    if parsed_query['names_only']:
        names = [f"• {c['name']}" for c in filtered_clients]
        answer = f"Found {len(filtered_clients)} client(s):\n" + "\n".join(names)
    else:
        if parsed_query['top_n']:
            if parsed_query['portfolio_focus']:
                client_info = [f"• {c['name']} (Portfolio: ₹{c['portfolio_value']:,})" for c in filtered_clients]
            else:
                client_info = [f"• {c['name']} (Risk: {c['risk_appetite']})" for c in filtered_clients]
        else:
            client_info = [f"• {c['name']} (ID: {c['client_id']}, Risk: {c['risk_appetite']})" for c in filtered_clients]
        answer = f"Found {len(filtered_clients)} client(s):\n" + "\n".join(client_info)
    
    return {
        "answer": answer,
        "query": question,
        "processing_time": f"{time.time() - start_time:.2f}s"
    }

def create_simple_query(question: str):
    """Create a simple MongoDB query based on keywords"""
    question_lower = question.lower()
    
    if 'high' in question_lower and 'risk' in question_lower:
        return {"risk_appetite": "High"}
    elif 'low' in question_lower and 'risk' in question_lower:
        return {"risk_appetite": "Low"}
    elif 'medium' in question_lower and 'risk' in question_lower:
        return {"risk_appetite": "Medium"}
    elif 'stocks' in question_lower:
        return {"investment_preferences": "Stocks"}
    elif 'real estate' in question_lower or 'property' in question_lower:
        return {"investment_preferences": "Real Estate"}
    elif 'portfolio' in question_lower or 'wealth' in question_lower or 'investor' in question_lower:
        return {}  # Return all for portfolio queries
    elif 'relationship manager' in question_lower or 'rm' in question_lower:
        return {}  # Return all for RM queries
    else:
        # Return all clients if no specific criteria
        return {}
