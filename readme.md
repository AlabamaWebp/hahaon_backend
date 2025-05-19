# На следующем хакатоне должен быть нормальный интернет!
# Docker

    docker pull dimyrp/hahaon:v1

    docker run --name hahaon_container -p 8000:8000 dimyrp/hahaon:v1

Проект будет запущен по адресу 

    http://localhost:8000

# No Docker
Для установки необходим python 3.12

Установить все зависимости из requirements.txt (будет долго, тк нейросети)

    pip install -r requirements.txt

## Запуск

    python main.py

    http://localhost:8000
