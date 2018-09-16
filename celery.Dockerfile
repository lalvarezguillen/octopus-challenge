FROM python:3.6
WORKDIR /home/app
COPY backend ./backend
COPY run_celery.py .
COPY requirements.dist.txt .
RUN pip install -r requirements.dist.txt
CMD ["celery", "-A", "run_celery.CELERY", "worker", "--loglevel=info"]