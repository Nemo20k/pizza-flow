FROM python:latest
WORKDIR '/pizza-flow'
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
