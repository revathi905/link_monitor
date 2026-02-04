FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    fonts-liberation \
    ca-certificates \
    wget \
    && rm -rf /var/lib/apt/lists/*


# Install cron (THIS WAS MISSING BEFORE)
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

COPY checker.py /app/
COPY screenshot_checker.py /app/
COPY crontab /etc/cron.d/link-cron

RUN chmod 0644 /etc/cron.d/link-cron \
    && crontab /etc/cron.d/link-cron

RUN touch /var/log/cron.log

CMD ["cron", "-f"]

