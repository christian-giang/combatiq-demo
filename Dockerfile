FROM python:latest
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . /app
CMD streamlit run --server.port 8080 --server.enableXsrfProtection=false --server.enableCORS=false combatiq_demo.py 