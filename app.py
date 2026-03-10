import streamlit.web.cli as stcli
import sys

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "AI_Healthcare_Analytics/frontend/dashboard.py"]
    sys.exit(stcli.main())