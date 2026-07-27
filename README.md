# Setup Steps

## Installation of virtual environment

```bash
# Check pip version
pip3 list

# Create venv - fastapienv is the name of the env
python3 -m venv fastapienv

# Activate
source fastapienv/bin/activate

# Activate from within dir
source ../fastapienv/bin/activate


# Deactivate
deactivate

# See installs in venv ** note don't need pip3
pip list
```

## Install initial deps

```bash
# Newest, allows running with fastapi run <path-to-py-file>
pip install "fastapi[standard]" 
pip install "uivcorn[standard]"
```

## Projects

## General

- FastAPI spins up at url 127.0.0.1:8000/<endpoint-name>

### Books API

Serve up with script
```bash
# run in prod
fastapi run books_api/books.py
## run in dev
fastapi dev books_api/books.py

# From the root
uvicorn books_api.books:app --reload
# From within /books_api/
uvicorn books:app --reload
```

## Docs

Available at [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)


## Reference

### Package details

- uvicorn - python web server
- ruff - linting, formatting, sorting