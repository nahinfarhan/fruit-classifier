#!/bin/bash
python app.py &
streamlit run app_ui.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true