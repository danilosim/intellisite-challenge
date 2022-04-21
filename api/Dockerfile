FROM python:3.9
WORKDIR /api
COPY requirements.txt /api/requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD python -m uvicorn --host 0.0.0.0 --port 8080 app:app --reload
