# ベースイメージを指定
FROM python:3.9-slim

# 作業ディレクトリを指定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt ./
COPY app.py ./

# 必要なパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# ポートを公開
EXPOSE 5000

# アプリを実行
CMD ["python", "app.py"]
