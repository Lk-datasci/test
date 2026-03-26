FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
RUN chmod 755 /app/app.py
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 7860
CMD ["python", "app.py"]
