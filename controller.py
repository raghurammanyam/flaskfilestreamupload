from flask_restful import Resource
from flask import request,make_response
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import zipfile
# from gcloudstream import GCSObjectStreamUpload
from google.cloud import storage
from gcpstorage import gbucket
from gmultipart import gmulti
import json
cwd =os.getcwd()




class uploadFile(Resource):
    def __init__(self):
        pass
    def post(self):
      #  print(request.__dict__)
        file = request.files['file']
        abc=cwd+'/'+str(datetime.now())
        target_dir = os.makedirs(abc)
        print(cwd,target_dir)
        namedfile=file.filename

        save_path = os.path.join(cwd, secure_filename(file.filename))
        current_chunk = int(request.form['dzchunkindex'])

        # If the file already exists it's ok if we are appending to it,
        # but not if it's new file that would overwrite the existing one
        if os.path.exists(save_path) and current_chunk == 0:
            # 400 and 500s will tell dropzone that an error occurred and show an error
            return make_response(('File already exists', 400))

        try:
            with open(save_path, 'ab') as f:
                f.seek(int(request.form['dzchunkbyteoffset']))
                f.write(file.stream.read())
        except OSError:
            print("lmdaslmlm")
            # log.exception will include the traceback so we can see what's wrong 
            # log.exception('Could not write to file')
            return make_response(("Not sure why,"
                                " but we couldn't write the file to disk", 500))

        total_chunks = int(request.form['dztotalchunkcount'])

        if current_chunk + 1 == total_chunks:
            # This was the last chunk, the file should be complete and the size we expect
            if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
                
                print(f"File {file.filename} was completed, "
                         f"but has a size mismatch."
                         f"Was {os.path.getsize(save_path)} but we"
                         f" expected {request.form['dztotalfilesize']} ")
                return make_response(('Size mismatch', 500))
            else:
                print(file.filename)
                # log.info(f'File {file.filename} has been uploaded successfully')
        else:
            # log.debug(f'Chunk {current_chunk + 1} of {total_chunks} '
            #         f'for file {file.filename} complete')
            print(f'Chunk {current_chunk + 1} of {total_chunks} '
                     f'for file {file.filename} complete')
        print("Chunk upload successful")
        with zipfile.ZipFile(save_path,"r") as zip_ref:
            zip_ref.extractall(abc)
        for x in os.listdir(abc):
            for y in os.listdir(abc+'/'+x):
                back=gmulti(abc+'/'+x+'/'+y,y)
                print(back)
                
        return make_response(("Chunk upload successful", 200))

