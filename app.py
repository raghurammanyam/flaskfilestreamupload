from flask_restful import Api
from config import app,cwd
from controller import uploadFile
from flask_session import Session
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=cwd+"/keelaa.json"
api=Api(app)
Session(app)

api.add_resource(uploadFile,'/api/resume')


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)