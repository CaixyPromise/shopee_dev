from flask import Flask

app = Flask(__name__, static_folder='./static',
                      template_folder = './template')

app.config['UPLOAD_FOLDER'] = './file'
app.config['JSON_AS_ASCII'] = False