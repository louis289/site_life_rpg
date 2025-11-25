FROM python:3.12-alpine

WORKDIR /app

# dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# script d'import
COPY import_from_sheets.py .

CMD ["python", "import_from_sheets.py"]
