FROM python:3.12

WORKDIR /code
RUN apt-get update && apt-get install -y libgl1
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./main.py .
COPY ./browser ./browser

# CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
