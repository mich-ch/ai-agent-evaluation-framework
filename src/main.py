import sys
import os

# Προσθήκη του src στο python path για να βρίσκει τα modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.router import run_agent

if __name__ == "__main__":
    print("=== AI Agent CLI ===")
    print("Ask a question about the sales data (or type 'exit' to quit)")
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        try:
            response = run_agent(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\nAn error occurred: {e}")