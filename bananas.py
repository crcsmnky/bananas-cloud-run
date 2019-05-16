import logging
import os
import sys

from flask import Flask, current_app, request, render_template, flash, redirect
from google.cloud import vision, storage
from slugify import slugify

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'a341056a4bc4ce3d0ae8d303a244fa46'

app.config.update({
    'PLATFORM': os.environ.get('PLATFORM', 'Cloud'),
    'WELCOME': os.environ.get('WELCOME', 'GDG Cloud Austin'),
    'BUCKET': os.environ.get('BUCKET', '[BUCKET_NAME]')
})

EXTENSIONS = set(['png', 'gif', 'jpg', 'tiff'])

def allowed(name):
    return '.' in name and \
        name.rsplit('.', 1)[1].lower() in EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def bananas():
    labels = None
    imagesrc = None

    if request.method == 'POST':
        if 'image' not in request.files:
            flash('Missing image data', 'danger')
            return redirect(request.url)

        image = request.files['image']

        if image.filename == '':
            flash('Missing image', 'danger')
            return  redirect(request.url)

        if image and allowed(image.filename):
            sclient = storage.Client()
            bucket = sclient.get_bucket(current_app.config['BUCKET'])
            path = slugify(current_app.config['PLATFORM'])
            
            imgblob = bucket.blob('{}/{}'.format(path, image.filename))
            imgblob.upload_from_file(image)
            imgblob.make_public()

            vclient = vision.ImageAnnotatorClient()
            response = vclient.label_detection({
                'source': {'image_uri': imgblob.public_url}
            })

            imagesrc = imgblob.public_url
            labels = list(response.label_annotations)
            
            for l in labels:
                if l.description == 'Banana':
                    flash('Found a banana!', 'warning')
        else:
            flash('Unsupported image type', 'danger')
            return redirect(request.url)

    return render_template('home.html', 
        platform=current_app.config['PLATFORM'],
        welcome=current_app.config['WELCOME'],
        labels=labels, imagesrc=imagesrc)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
