import os
import phoenix as px
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Παγκόσμια μεταβλητή για τον tracer
tracer = None

def setup_tracing():
    """
    Αρχικοποιεί το Phoenix server και συνδέει το OpenAI για αυτόματη καταγραφή (instrumentation).
    """
    global tracer
    
    # 1. Εκκίνηση του Phoenix (θα τρέχει τοπικά)
    # Σημείωση: Σε production θα συνδεόμασταν σε απομακρυσμένο server.
    os.environ["PHOENIX_PROJECT_NAME"] = "ai-agent-evaluation-v1"
    
    # Το register επιστρέφει το tracer_provider που στέλνει τα δεδομένα στο Phoenix
    tracer_provider = register(
        project_name="ai-agent-evaluation-v1",
        endpoint="http://localhost:6006/v1/traces" # Default port
    )
    
    # 2. Αυτόματη καταγραφή όλων των κλήσεων προς OpenAI
    OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
    
    # 3. Δημιουργία του Tracer αντικειμένου που θα χρησιμοποιούμε στα tools
    tracer = trace.get_tracer(__name__)
    
    print("\n✅ Phoenix Tracing Initialized!")
    print("📊 View Traces at: http://localhost:6006\n")
    
    return tracer

def get_tracer():
    """Επιστρέφει τον tracer για χρήση σε άλλα αρχεία"""
    if tracer is None:
        return trace.get_tracer(__name__)
    return tracer