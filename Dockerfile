FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
COPY . .
EXPOSE 99
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]