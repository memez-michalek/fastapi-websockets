FROM python:3.8.6
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY . . 
EXPOSE 8000
CMD ["entrypoint.sh"]
