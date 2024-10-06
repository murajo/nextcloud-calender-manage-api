FROM python:3.12

# Replace these with your own NextCloud details
# These are placeholders and should be overwritten in your environment setup
ENV NEXTCLOUD_URL='https://<your_nextcloud_domain>/remote.php/dav'
ENV NEXTCLOUD_USERNAME='<your_nextcloud_username>'
ENV NEXTCLOUD_PASSWORD='<your_nextcloud_password>'
# Set to 'True' if using a valid SSL certificate
ENV VERIFY_SSL='False' 

WORKDIR /app

COPY src/ ./src/
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/app.py"]
