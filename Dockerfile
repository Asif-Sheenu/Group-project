FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip


RUN pip install --no-cache-dir torch==2.7.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

RUN grep -v "^torch" requirements.txt > req.txt && \
    pip install --no-cache-dir -r req.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]