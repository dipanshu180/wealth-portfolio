import mysql.connector
import logging
import os
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def connect_mysql():
    """Connect to MySQL with environment variables and error handling"""
    try:
        # Get database configuration from environment variables
        host = os.getenv("MYSQL_HOST", "localhost")
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "Dip@1234")
        database = os.getenv("MYSQL_DATABASE", "valuefy")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        
        logger.info(f"Connecting to MySQL: {host}:{port}/{database}")
        
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            autocommit=True,
            connection_timeout=10,
            pool_size=5,
            pool_name="valuefy_pool"
        )
        
        logger.info("MySQL connection successful")
        return conn
        
    except mysql.connector.Error as e:
        logger.error(f"MySQL connection error: {str(e)}")
        raise Exception(f"Failed to connect to MySQL: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error connecting to MySQL: {str(e)}")
        raise Exception(f"MySQL connection failed: {str(e)}")

def test_mysql():
    """Test MySQL connection and basic operations"""
    try:
        logger.info("Testing MySQL connection...")
        conn = connect_mysql()
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) FROM transactions")
        count = cursor.fetchone()[0]
        logger.info(f"Total transactions in database: {count}")
        
        # Test sample data
        cursor.execute("SELECT * FROM transactions LIMIT 3")
        rows = cursor.fetchall()
        for row in rows:
            logger.info(f"Sample transaction: {row}")
            
        cursor.close()
        conn.close()
        logger.info("MySQL test completed successfully")
        
    except Exception as e:
        logger.error(f"MySQL test failed: {str(e)}")
        raise

def get_mysql_connection():
    """Get a MySQL connection with error handling"""
    try:
        return connect_mysql()
    except Exception as e:
        logger.error(f"Failed to get MySQL connection: {str(e)}")
        raise

# if __name__ == "__main__":
#     test_mysql()