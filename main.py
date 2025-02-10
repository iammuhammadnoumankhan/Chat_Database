from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from contextlib import asynccontextmanager

# --- Configuration Management ---
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    # LLM Configuration
    LLM_MODEL: str = "llama3.2:latest"
    LLM_BASE_URL: str = "http://localhost:11434/v1"
    LLM_API_KEY: str = "ollama"
    
    # Database Defaults
    DEFAULT_DB_URI: str = "sqlite:///Chinook.db"
    
    # Security
    MAX_CONNECTIONS: int = 100
    QUERY_TIMEOUT: int = 30

settings = Settings()

# --- Database Connection Pool ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize connection pool
    yield
    # Cleanup connections

app = FastAPI(lifespan=lifespan)

# --- Core Service Components ---
def get_llm():
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0,
        base_url=settings.LLM_BASE_URL,
        api_key=settings.LLM_API_KEY,
    )

def create_agent_executor(db_uri: str = settings.DEFAULT_DB_URI):
    try:
        db = SQLDatabase.from_uri(db_uri)
        return create_sql_agent(
            llm=get_llm(),
            db=db,
            agent_type="openai-tools",
            verbose=True,
            max_execution_time=settings.QUERY_TIMEOUT
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database connection failed: {str(e)}")

# --- Request Model ---
class QueryRequest(BaseModel):
    query: str
    db_uri: str = settings.DEFAULT_DB_URI

# --- API Endpoints ---
@app.post("/query")
async def execute_query(payload: QueryRequest):
    """
    Execute natural language query against specified database.
    
    Example Request Body:
    {
        "query": "List top 5 customers by total purchases",
        "db_uri": "postgresql://user:pass@localhost/mydb"
    }
    """
    try:
        agent = create_agent_executor(payload.db_uri)
        result = agent.invoke({"input": payload.query})
        return {"result": result['output']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/schema")
async def get_schema(db_uri: str = settings.DEFAULT_DB_URI):
    """Retrieve database schema information"""
    try:
        db = SQLDatabase.from_uri(db_uri)
        return {"schema": db.get_table_info()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
