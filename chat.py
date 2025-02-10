import requests
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

# Initialize Rich Console
console = Console()

# API Configuration
API_URL = "http://localhost:8000/query"

def send_query(query: str):
    """Send a query to the FastAPI chat API and display results beautifully."""
    payload = {"query": query}
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("result", "No result returned")
    except requests.exceptions.RequestException as e:
        return f"[bold red]Error:[/bold red] {str(e)}"

def display_result(result: str):
    """Display the result using Rich's table or panel."""
    console.print(Panel(result, title="Query Result", border_style="blue"))

def main():
    """Main loop for user interaction."""
    console.print(Panel("Welcome to the SQL Chat Agent!", title="Chat Interface", border_style="green"))
    
    while True:
        query = Prompt.ask("[bold cyan]Enter your SQL query (or type 'exit' to quit)[/bold cyan]")
        if query.lower() in ["exit", "quit"]:
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break
        
        console.print("\n[bold magenta]Sending query...[/bold magenta]")
        result = send_query(query)
        display_result(result)
        console.print("\n[bold green]Done! Enter a new query or type 'exit' to quit.[/bold green]")

if __name__ == "__main__":
    main()
