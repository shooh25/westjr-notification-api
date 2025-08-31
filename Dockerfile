FROM python:3.11-slim

# イメージ内に作業ディレクトリ指定
WORKDIR /app

# イメージ内の作業ディレクトリにコピー&インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ホストのファイルをイメージ内の作業ディレクトリにコピー
COPY ./app ./app

# Uvicornで起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
