
FROM python:3.10-slim


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY API_Endpoint.json .
COPY main.py .

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
