import streamlit.web.cli as stcli
import sys

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "frontend/dashboard.py"]
    sys.exit(stcli.main())