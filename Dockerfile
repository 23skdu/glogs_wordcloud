FROM python:3.13.2-slim
LABEL author=23skdu@users.noreply.github.com
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt update && apt -y upgrade \
    && pip3 google-cloud-logging google-cloud-storage matplotlib wordcloudi \
    && pip3 cache purge
CMD ["python","-c", "print('works')"]
