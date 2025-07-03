FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV LANGRAPH_STUDIO_URL=${STUDIO_URL}
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]