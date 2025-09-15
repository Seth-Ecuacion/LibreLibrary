
# Project Setup Guide

This guide will help you set up your Python environment, install dependencies, configure secrets, and provide links to useful documentation.

---

## 1. Create a Python Environment

It's recommended to use a virtual environment to manage dependencies.

### Using `venv`:

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Using `conda`:

```bash
# Create a conda environment named 'myenv' with Python 3.11
conda create -n myenv python=3.11

# Activate the environment
conda activate myenv
```

---

## 2. Install Dependencies

Once your environment is activated, install the required libraries:

```bash
pip install -r requirements.txt
```

This will install all the necessary packages listed in `requirements.txt`.

---

## 3. Configure Secrets

Your project may require sensitive information like API keys or database credentials. You can store these safely using `.env` or Streamlit's `secrets.toml`.

### Using `.env`:

1. Create a file named `.env` in your project root.
2. Add your secrets like this:

```env
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
GROQ_API_KEY=your_api_key
```

3. Access them in Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
api_key = os.getenv("GROQ_API_KEY")
```

### Using Streamlit `secrets.toml`:

1. Create a file at `.streamlit/secrets.toml`.
2. Add your secrets like this:

```toml
[snowflake]
user = "your_username"
password = "your_password"

[groq]
api_key = "your_api_key"
```

3. Access them in Python:

```python
import streamlit as st

user = st.secrets["snowflake"]["user"]
password = st.secrets["snowflake"]["password"]
api_key = st.secrets["groq"]["api_key"]
```

---

## 4. Documentation Links

- [Streamlit Documentation](https://docs.streamlit.io)  
- [Snowflake Documentation](https://docs.snowflake.com)  
- [Groq Documentation](https://www.groq.com/docs)

---

## 5. Run Your Streamlit App

```bash
streamlit run your_app.py
```

---

This should get you up and running quickly!
