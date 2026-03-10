import subprocess

def handler(request, response):
    subprocess.Popen([
        "streamlit",
        "run",
        "app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])

    return {
        "statusCode": 200,
        "body": "Streamlit server started"
    }