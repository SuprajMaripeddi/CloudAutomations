from flask import Flask, render_template
import boto3
import pyshorteners

app = Flask(__name__)

s3 = boto3.client('s3')
bucket_name = 'cf-templates-f9dwik8ihlzx-us-east-1'
objects = s3.list_objects(Bucket=bucket_name)['Contents']

urls = []
for obj in objects:
    obj_key = obj['Key']
    presigned_url = s3.generate_presigned_url(
        'get_object', Params={'Bucket': bucket_name, 'Key': obj_key}, ExpiresIn=3600)
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(presigned_url)
    urls.append((obj_key, short_url))

@app.route('/')
def index():
    return render_template('index.html', title='Presigned URLs', urls=urls)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

