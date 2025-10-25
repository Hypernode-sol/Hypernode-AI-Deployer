FROM python:3.11-slim

WORKDIR /workspace
COPY api/requirements.txt /workspace/api/requirements.txt
RUN pip install --no-cache-dir -r /workspace/api/requirements.txt

COPY . /workspace
EXPOSE 8080
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
