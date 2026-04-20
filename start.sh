#This script acts as the "orchestrator" that launches both FastAPI backend and Streamlit frontend for HF spaces deployment

#!/bin/bash
# Start FastAPI (The Brain) in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for the API to start up
sleep 10

# Start Streamlit (The Face) on the port HF expects
streamlit run app.py --server.port 7860 --server.address 0.0.0.0