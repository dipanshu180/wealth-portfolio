from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import warnings
import re
import logging
import traceback
from typing import Optional, Dict, Any

# Suppress LangSmith warnings
warnings.filterwarnings('ignore', category=UserWarning, module='langsmith')

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
mysql_uri = os.getenv("MYSQL_URI")

if not openai_api_key:
    logger.error("OPENAI_API_KEY missing in .env")
    raise ValueError("OPENAI_API_KEY missing in .env")
if not mysql_uri:
    logger.error("MYSQL_URI missing in .env")
    raise ValueError("MYSQL_URI missing in .env")

class SQLQueryAgent:
    """Production-ready SQL Query Agent with enhanced error handling and fallback"""
    
    def __init__(self):
        try:
            self.db = SQLDatabase.from_uri(mysql_uri)
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo", 
                temperature=0, 
                api_key=openai_api_key,
                max_tokens=1500,
                timeout=30  # Add timeout
            )
            self.agent = None
            self.schema_info = None
            self._init_schema_info()
            self._init_agent()
        except Exception as e:
            logger.error(f"Failed to initialize SQLQueryAgent: {str(e)}")
            raise Exception(f"Failed to initialize SQL agent: {str(e)}")
    
    def _init_schema_info(self):
        """Initialize and cache schema information"""
        try:
            self.schema_info = self.db.get_table_info()
            logger.info("✅ Schema information loaded successfully!")
        except Exception as e:
            logger.error(f"⚠️ Failed to load schema: {str(e)}")
            self.schema_info = None
    
    def _init_agent(self):
        """Initialize the SQL agent with proper error handling"""
        try:
            toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            tools = toolkit.get_tools()
            
            # Custom prompt for better SQL generation
            custom_prompt = PromptTemplate(
                template="""You are a SQL expert helping to query a MySQL database. 

Database Schema:
{schema}

Available tools:
{tools}

IMPORTANT RULES:
1. Always check the schema before writing queries
2. Use EXACT column names from the schema: transaction_id, client_id, stock_name, amount_invested, date_, rm_name
3. The table name is 'transactions'
4. Use proper MySQL syntax
5. Format dates as 'YYYY-MM-DD' 
6. Always provide a clear final answer
7. If you encounter an error, analyze it and try a corrected query
8. For "top N" queries, use LIMIT N
9. For sorting by amount, use ORDER BY amount_invested DESC
10. Always prioritize showing names over IDs when possible

Use this format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought:{agent_scratchpad}""",
                input_variables=["input", "agent_scratchpad"],
                partial_variables={
                    "schema": self.schema_info or "Schema not available",
                    "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
                    "tool_names": ", ".join([tool.name for tool in tools])
                }
            )
            
            # Create agent
            agent = create_react_agent(self.llm, tools, custom_prompt)
            
            # Create agent executor with better configuration
            self.agent = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,  # Increased iterations
                max_execution_time=60,  # Added timeout
                return_intermediate_steps=True
            )
            
            logger.info("SQL Agent initialized successfully!")
            
        except Exception as e:
            logger.error(f"Agent initialization failed: {str(e)}")
            self.agent = None
    
    def query(self, question: str) -> str:
        """Query the database with the given question"""
        logger.info(f"🔍 Processing question: {question}")
        
        if not question or not question.strip():
            return "Please provide a valid question."
        
        # Parse the question to extract specific requirements
        parsed_query = self._parse_question(question)
        
        # Try agent first
        if self.agent:
            try:
                response = self.agent.invoke({"input": question})
                output = response.get('output', 'No output found')
                
                # Check if the response is meaningful
                if output and len(output.strip()) > 10 and "Agent stopped" not in output:
                    return self._format_final_response(output, parsed_query)
                else:
                    logger.info("Agent response insufficient, trying fallback...")
                    
            except Exception as e:
                logger.error(f"Agent failed: {str(e)}")
                logger.info("Falling back to direct SQL generation...")
        
        # Fallback to direct SQL generation
        return self._direct_sql_query(question, parsed_query)
    
    def _parse_question(self, question: str):
        """Parse the question to extract specific requirements"""
        question_lower = question.lower()
        
        parsed = {
            'limit': None,
            'sort_by': None,
            'sort_order': 'DESC',
            'top_n': False,
            'names_only': False,
            'amount_focus': False
        }
        
        # Extract limit number
        limit_match = re.search(r'top\s+(\d+)', question_lower)
        if limit_match:
            parsed['limit'] = int(limit_match.group(1))
            parsed['top_n'] = True
        
        # Check for name-specific queries
        if 'name' in question_lower or 'who' in question_lower:
            parsed['names_only'] = True
        
        # Check for amount-focused queries
        if 'amount' in question_lower or 'investment' in question_lower or 'top' in question_lower:
            parsed['amount_focus'] = True
            parsed['sort_by'] = 'amount_invested'
        
        # Determine sort criteria
        if 'highest' in question_lower or 'top' in question_lower:
            parsed['sort_order'] = 'DESC'
        elif 'lowest' in question_lower:
            parsed['sort_order'] = 'ASC'
        
        return parsed
    
    def _direct_sql_query(self, question: str, parsed_query: dict) -> str:
        """Enhanced direct SQL query generation and execution"""
        try:
            # Generate SQL query
            sql_query = self._generate_sql_query(question, parsed_query)
            if not sql_query:
                return "Could not generate SQL query"
            
            logger.info(f"Generated SQL: {sql_query}")
            
            # Execute query with retry logic
            result = self._execute_query_with_retry(sql_query, question)
            
            # Format and return response
            return self._format_response(question, sql_query, result, parsed_query)
                
        except Exception as e:
            logger.error(f"Error in SQL handler: {str(e)}")
            return f"Error in SQL handler: {str(e)}"
    
    def _generate_sql_query(self, question: str, parsed_query: dict) -> Optional[str]:
        """Generate SQL query using LLM with enhanced parsing"""
        try:
            # Build enhanced prompt based on parsed requirements
            limit_clause = f" LIMIT {parsed_query['limit']}" if parsed_query['limit'] else ""
            order_clause = ""
            
            if parsed_query['sort_by']:
                order_clause = f" ORDER BY {parsed_query['sort_by']} {parsed_query['sort_order']}"
            
            sql_prompt = f"""
Based on this MySQL database schema:
{self.schema_info}

Generate a SQL query to answer: {question}

CRITICAL RULES:
1. Use EXACT column names: transaction_id, client_id, stock_name, amount_invested, date_, rm_name
2. Table name is: transactions
3. Use proper MySQL syntax
4. For date filtering, use date_ column with format 'YYYY-MM-DD'
5. For "top N" queries, use LIMIT N
6. For sorting by amount, use ORDER BY amount_invested DESC
7. Always prioritize showing names over IDs when possible
8. Return ONLY the SQL query, no explanation

Additional Requirements:
- Limit: {parsed_query['limit'] or 'None'}
- Sort by: {parsed_query['sort_by'] or 'None'}
- Sort order: {parsed_query['sort_order']}

SQL Query:"""
            
            response = self.llm.invoke(sql_prompt)
            sql_query = self._clean_sql_query(response.content)
            
            # Ensure LIMIT is applied if specified
            if parsed_query['limit'] and 'LIMIT' not in sql_query.upper():
                sql_query = sql_query.rstrip(';') + f" LIMIT {parsed_query['limit']};"
            
            return sql_query
            
        except Exception as e:
            logger.error(f"SQL generation error: {str(e)}")
            return None
    
    def _clean_sql_query(self, sql_query: str) -> str:
        """Clean and format SQL query"""
        # Remove code blocks
        sql_query = re.sub(r'```sql\n?', '', sql_query)
        sql_query = re.sub(r'```\n?', '', sql_query)
        
        # Remove extra whitespace
        sql_query = sql_query.strip()
        
        # Ensure semicolon at end
        if not sql_query.endswith(';'):
            sql_query += ';'
            
        return sql_query
    
    def _execute_query_with_retry(self, sql_query: str, question: str) -> str:
        """Execute query with error handling and retry logic"""
        try:
            result = self.db.run(sql_query)
            logger.info(f"Raw Result: {result}")
            return result
            
        except Exception as query_error:
            error_msg = str(query_error)
            logger.error(f"Query error: {error_msg}")
            
            # Try to fix common errors
            if "Unknown column" in error_msg:
                # Try to fix column name issues
                corrected_query = self._fix_column_names(sql_query)
                if corrected_query != sql_query:
                    logger.info(f"Retrying with corrected query: {corrected_query}")
                    try:
                        result = self.db.run(corrected_query)
                        logger.info(f"Retry Result: {result}")
                        return result
                    except Exception as retry_error:
                        logger.error(f"Retry failed: {str(retry_error)}")
            
            return f"Query execution failed: {error_msg}"
    
    def _fix_column_names(self, sql_query: str) -> str:
        """Fix common column name issues"""
        # Common column name fixes
        replacements = {
            'transactoin_id': 'transaction_id',  # Fix the typo in the database
            'amount': 'amount_invested',
            'transaction_date': 'date_',
            'date': 'date_',
            'rm': 'rm_name',
            'relationship_manager': 'rm_name'
        }
        
        corrected_query = sql_query
        for wrong, correct in replacements.items():
            corrected_query = re.sub(rf'\b{wrong}\b', correct, corrected_query, flags=re.IGNORECASE)
        
        return corrected_query
    
    def _format_response(self, question: str, sql_query: str, result: str, parsed_query: dict) -> str:
        """Format the final response with enhanced parsing"""
        if "Query execution failed" in result:
            return result
        
        try:
            # Enhanced formatting prompt
            format_prompt = f"""
Question: {question}
SQL Query: {sql_query}
Query Result: {result}

Please provide a clear, natural language answer to the original question based on these results.

Guidelines:
1. Be concise but informative
2. Format numbers with commas for readability
3. Include currency symbols (₹) where applicable
4. If result is empty, say "No data found"
5. For lists, format them nicely
6. Don't include technical SQL details in the answer
7. For "top N" queries, emphasize the ranking
8. Prioritize showing names over IDs when possible
9. For amount-focused queries, highlight the amounts clearly

Additional Context:
- This is a "top N" query: {parsed_query['top_n']}
- Names only requested: {parsed_query['names_only']}
- Amount focus: {parsed_query['amount_focus']}

Answer:"""
            
            formatted_response = self.llm.invoke(format_prompt)
            return formatted_response.content
            
        except Exception as e:
            logger.error(f"Formatting error: {str(e)}")
            return f"Result: {result}\n(Formatting error: {str(e)})"
    
    def _format_final_response(self, response: str, parsed_query: dict) -> str:
        """Format the final response from agent"""
        if parsed_query['names_only']:
            # Extract names from the response
            # This is a simple approach - in production you might want more sophisticated parsing
            return response
        
        return response

def test_agent():
    """Test the SQL agent with various queries"""
    
    # Initialize agent
    try:
        agent = SQLQueryAgent()
    except Exception as e:
        logger.error(f"Failed to initialize agent for testing: {str(e)}")
        return
    
    # Test questions
    test_questions = [
        "How many total transactions are there?",
        "What is the total amount invested across all transactions?",
        "Show me the top clients by investment amount",
        "Which stocks have been invested in?",
        "Who is the relationship manager for client C001?",
        "What transactions happened in January 2025?",
        "Show me all transactions with their details"
    ]
    
    logger.info("🚀 Testing SQL Agent with various queries...")
    
    for i, question in enumerate(test_questions, 1):
        logger.info(f"\n{'='*70}")
        logger.info(f"Test {i}: {question}")
        logger.info('='*70)
        
        try:
            response = agent.query(question)
            logger.info("Response:")
            logger.info(response)
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        
        logger.info("")  # Add spacing between tests

def debug_database():
    """Debug database connection and structure"""
    try:
        db = SQLDatabase.from_uri(mysql_uri)
        logger.info("🔍 Database Debug Info:")
        logger.info(f"Tables: {db.get_usable_table_names()}")
        logger.info(f"Schema:\n{db.get_table_info()}")
        
        # Test a simple query
        result = db.run("SELECT COUNT(*) as total FROM transactions")
        logger.info(f"Total transactions: {result}")
        
    except Exception as e:
        logger.error(f"Database debug error: {str(e)}")

# Main query function for external use
def query_sql_database(question: str) -> str:
    """Main function to query the SQL database"""
    try:
        agent = SQLQueryAgent()
        return agent.query(question)
    except Exception as e:
        logger.error(f"Error in query_sql_database: {str(e)}")
        return f"Error: {str(e)}"

def get_sql_agent():
    """Get SQL agent instance for external use"""
    try:
        return SQLQueryAgent()
    except Exception as e:
        logger.error(f"Failed to initialize SQL agent: {str(e)}")
        raise Exception(f"Failed to initialize SQL agent: {str(e)}")

if __name__ == "__main__":
    debug_database()
    logger.info("\n" + "="*80 + "\n")
    test_agent()



