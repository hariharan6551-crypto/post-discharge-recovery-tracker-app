import os

folders = [
    "backend",
    "frontend",
    "data",
    "reports",
    "models",
    "charts"
]

files = [
    "app.py",
    "requirements.txt",
    "README.md",
    "backend/ai_agent.py",
    "backend/sql_engine.py",
    "backend/chart_generator.py",
    "backend/ml_model.py"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file in files:
    open(file, "a").close()

print("Project structure created successfully!")