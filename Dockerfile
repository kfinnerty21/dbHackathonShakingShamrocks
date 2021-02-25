FROM python:3.7-slim
WORKDIR /app
COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD data /app/data/
ADD services /app/services
ENTRYPOINT ["python"]
CMD ["/app/app.py"]