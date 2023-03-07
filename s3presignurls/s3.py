import boto3
from flask import Flask, render_template

app = Flask(__name__)
s3 = boto3.client('s3')
bucket_name = 'cf-templates-f9dwik8ihlzx-us-east-1'

@app.route('/')
def index():
    objects = s3.list_objects(Bucket=bucket_name)
    urls = []
    for obj in objects['Contents']:
        obj_key = obj['Key']
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': obj_key
            },
            ExpiresIn=3600
        )
        urls.append((obj_key, presigned_url))
    return render_template('index.html', urls=urls)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
