FROM python:3.11-slim
WORKDIR /app
COPY api/app.py .
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
