# Chat with Database API

An AI-powered SQL chat service that allows you to interact with your database using natural language queries. Built with FastAPI and LangChain, it supports various SQL databases, including SQLite and PostgreSQL, with or without Docker.

## Features
- **Natural Language to SQL**: Convert text-based queries into SQL commands
- **Supports Multiple Databases**: Works with SQLite, PostgreSQL, and more
- **FastAPI Backend**: High-performance API with interactive docs
- **Docker Support**: Easily deployable using Docker
- **Configurable with Environment Variables**
- **Support OpenAI and OpenAI like APIs**

---

## **1. Setup Instructions**

### **1.1 Requirements**
- Python 3.10+
- pip (Python package manager)
- SQLite or PostgreSQL (if using a database)
- Ollama API (for LLM processing, optional)
- Docker (optional for containerized deployment)

### **1.2 Installation (Without Docker)**

1. Clone the repository:
   ```sh
   git clone https://github.com/iammuhammadnoumankhan/Chat_Database.git
   cd chat-with-database
   ```

2. Create a virtual environment and activate it:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set environment variables (or create a `.env` file):
   ```sh
   export LLM_API_KEY=ollama
   export DEFAULT_DB_URI=sqlite:///Chinook.db
   export LLM_BASE_URL=http://localhost:11434/v1
   export LLM_MODEL=llama3.2:latest
   ```

5. Run the API server:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

6. Test if the API is running:
   ```sh
   curl http://localhost:8000/docs
   ```

---

## **2. Running with Docker**

### **2.1 Build the Docker Image**
```sh
sudo docker build -t chat-service .
```

### **2.2 Run the Container**
```sh
sudo docker run -d -p 8000:8000 \
  -e LLM_API_KEY=ollama \
  -e DEFAULT_DB_URI=sqlite:///Chinook.db \
  -e LLM_BASE_URL=http://localhost:11434/v1 \
  --name chat-service chat-service
```
`Note: Kindly pass `LLM_BASE_URL` url where ollama is serve e.g: "http://x.x.x.x:11434/v1". By default it is set to http://localhost:11434/v1 and pass you databse URI. By Default it is set to "DEFAULT_DB_URI=sqlite:///Chinook.db".`

### **2.3 Verify API is Running**
```sh
curl http://localhost:8000/docs
```

---

## **3. Usage Examples**

### **3.1 Use via `chat.py`**
1. Open `Chat.py` and modify `API_URL` to a url where app is running. By default : `API_URL = "http://localhost:8000/query"`

2. Install `rich` via `pip install rich`.

3. Run `python chat.py`.

`Note: Via "chat.py" you will be able to chat with app via terminal like chat assistant.`

### **3.1 Sending Queries via cURL**

#### **Without URI (uses default DB)**
```sh
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "List top 5 customers by total purchases"}'
```

#### **With Custom Database URI**
```sh
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "List top 5 customers by total purchases", "db_uri": "postgresql://user:pass@localhost:5432/mydb"}'
```

---

## **4. Environment Variables**
| Variable          | Default Value              | Description |
|------------------|--------------------------|-------------|
| LLM_API_KEY     | ollama                    | API key for LLM |
| DEFAULT_DB_URI  | sqlite:///Chinook.db      | Default database URI |
| LLM_BASE_URL    | http://localhost:11434/v1 | LLM service base URL |
| LLM_MODEL       | llama3.2:latest           | LLM model to use |

---

## **5. Logs and Debugging**
### **5.1 Checking Logs in Docker**
```sh
sudo docker logs chat-service
```

### **5.2 Running in Debug Mode (Local)**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### **5.3 Debugging Inside Docker**
```sh
sudo docker exec -it chat-service /bin/bash
# Inside container:
cat /var/log/app.log  # Or wherever logs are stored
```

---

## **6. Deployment Notes**

### **6.1 Running on a Cloud Server**
Use a cloud server like AWS EC2, DigitalOcean, or GCP, and run:
```sh
docker run -d -p 80:8000 --restart always chat-service
```

### **6.2 Running Behind Nginx Reverse Proxy**
Example Nginx config:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### **6.3 Running with Docker Compose**
Create a `docker-compose.yml`:
```yaml
version: '3.8'
services:
  chat-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LLM_API_KEY=ollama
      - DEFAULT_DB_URI=sqlite:///Chinook.db
```
Run it:
```sh
docker-compose up -d
```

---

## **7. Contributing**
1. Fork the repository
2. Create a new branch
3. Make your changes and test them
4. Submit a pull request

---

## **8. License**
This project is licensed under the MIT License.

---

## **9. Contact**
For support or feature requests, contact [Your Name] at [your.email@example.com].

