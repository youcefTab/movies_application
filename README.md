# movies_application

# Start the application
```cd docker```

```docker-compose up --build -d```

```cd ..```
# --- USE THE BACKEND ---

# 1. Populate the database

# Start Venv and install requirements
```source backend_project/venv/bin/activate```

# Double Check which pip is being used
```which pip```

# Install requirements
```pip install -r requirements.txt```

# Export the backend environment variables
```source backend_project/dev_scripts/utils/export_db_variables.sh```

# Populate database
```python3 backend_project/movies_app/management/populate_db.py```
