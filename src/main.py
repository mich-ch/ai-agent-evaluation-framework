import sys
import os
import phoenix as px

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.router import run_agent
from src.tracing.phoenix_setup import setup_tracing

if __name__ == "__main__":
    # 1. Start Tracing
    tracer = setup_tracing()
    
    # 2. Launch Phoenix UI (Optional: Open browser automatically)
    # session = px.launch_app() 

    print("=== AI Agent CLI (with Observability) ===")
    print("Ask a question (or type 'exit')")
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        try:
            response = run_agent(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\nAn error occurred: {e}")