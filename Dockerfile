FROM python:3.13.2-slim
LABEL author=23skdu@users.noreply.github.com
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt update && apt -y upgrade \
    && apt install -y python3-dev gcc build-essential && apt-get clean \
    && pip3 install google-cloud-logging google-cloud-storage matplotlib wordcloud \
    && pip3 cache purge
CMD ["python","-c", "print('works')"]
