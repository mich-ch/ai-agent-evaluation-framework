import sys
import os
import pandas as pd
import json
from phoenix.experiments import run_experiment
import phoenix as px

# Setup paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agent.router import run_agent, client # Χρειαζόμαστε πρόσβαση για να τρέξουμε τον Agent
from src.evaluation.data_config import TEST_DATASET
from src.evaluation.evaluators import evaluate_clarity, evaluate_code_runnability, evaluate_sql_correctness
from src.tracing.phoenix_setup import setup_tracing

# 1. Setup
setup_tracing()
px_client = px.Client()

test_df = pd.DataFrame(TEST_DATASET)

def extract_metadata_from_history(messages):
    """
    Βοηθητική συνάρτηση που ψάχνει στο ιστορικό για να βρει τι SQL ή Python έγραψε ο Agent.
    """
    metadata = {
        "generated_sql": None,
        "generated_python_code": None
    }
    
    for msg in messages:
        if isinstance(msg, dict):
            # Έλεγχος αν είναι μήνυμα tool output
            if msg.get("role") == "tool":
                content = str(msg.get("content", ""))
                
                # Πρόχειρος έλεγχος αν είναι SQL result (συνήθως DataFrame string)
                # Σημείωση: Στο Lab 3 χρησιμοποιούν traces, εδώ κάνουμε parsing για απλότητα
                pass

        # Ψάχνουμε στα μηνύματα του Assistant για tool_calls
        if msg.get("tool_calls"):
            for tc in msg["tool_calls"]:
                fn_name = tc.function.name
                args = json.loads(tc.function.arguments)
                
                # Αν κάλεσε το visualization, άρα παρήγαγε κώδικα;
                # Όχι ακριβώς, ο κώδικας παράγεται εσωτερικά στο tool.
                # Γι' αυτό το demo, θα κάνουμε extract αν το τελικό output περιέχει κώδικα
                pass
                
    return metadata

def agent_task(input_data):
    """
    Το Task τώρα επιστρέφει Structured Output για να το δουν οι Evaluators.
    """
    question = input_data['question']
    
    # Τρέχουμε τον Agent κανονικά
    # ΠΡΟΣΟΧΗ: Εδώ κάνουμε ένα μικρό hack. Το run_agent επιστρέφει μόνο string.
    # Σε ένα full production system, το run_agent θα επέστρεφε (response, metadata).
    # Εδώ θα αρκεστούμε στο τελικό κείμενο και θα κάνουμε assumptions για το demo.
    
    final_response = run_agent(question)
    
    # Προσπαθούμε να μαντέψουμε αν υπάρχει κώδικας στην απάντηση (αν ο agent τον εμφάνισε)
    # ή αν μπορούμε να τον βρούμε. 
    # ΣΗΜΕΙΩΣΗ: Για να δουλέψει τέλεια το Code Evaluator, θα έπρεπε να αλλάξουμε 
    # το src/agent/router.py να επιστρέφει ΟΛΟ το history.
    
    output_payload = {
        "final_response": final_response,
        # Στο συγκεκριμένο setup, δεν έχουμε εύκολη πρόσβαση στο ενδιάμεσο SQL/Python 
        # χωρίς να αλλάξουμε το router.py. 
        # Θα βάλουμε placeholders που θα μπορούσαμε να γεμίσουμε αν αλλάζαμε το Router.
        "generated_sql": None, 
        "generated_python_code": None
    }
    
    # Αν η απάντηση περιέχει κώδικα (markdown), τον βάζουμε στο payload
    if "```python" in final_response:
        output_payload["generated_python_code"] = final_response
    if "SELECT" in final_response and "FROM" in final_response:
        output_payload["generated_sql"] = final_response
        
    return output_payload

if __name__ == "__main__":
    print("🚀 Starting Professional Evaluation Experiment...")
    
    now_str = pd.Timestamp.now().strftime("%Y-%m-%d-%H-%M")
    
    dataset = px_client.upload_dataset(
        dataframe=test_df,
        dataset_name=f"sales-eval-{now_str}",
        input_keys=["question"]
    )
    
    experiment = run_experiment(
        dataset=dataset,
        task=agent_task,
        evaluators=[
            evaluate_clarity,
            evaluate_code_runnability, 
            evaluate_sql_correctness
        ],
        experiment_name=f"Full-Agent-Eval-{now_str}"
    )
    
    print("\n✅ Experiment Completed!")
    print("📊 View results at: http://localhost:6006 (Experiments Tab)")