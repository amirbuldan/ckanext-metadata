import os
from flask import (Blueprint, render_template, jsonify, request, flash, url_for)
import ckan.plugins.toolkit as tk
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
from ckanext.metadata.db import Metadata
from werkzeug.utils import secure_filename

import ckan.plugins as plugins

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'public/uploads'
ALLOWED_EXTENSION = {'pdf'}

# tambah url_prefix
bp = Blueprint(
    "metadata", __name__, url_prefix="/metadata"
)

def page():
    # return "metadata blueprint test view"
    dt_metadata = tk.get_action('metadata_get_all')(context={}, data_dict={})

    return render_template('metadata/index.html', data=dt_metadata)

def create():
    # return "halaman tambah metadata"
    try:
        plugins.toolkit.check_access('metadata_create', context={}, data_dict={})
    except plugins.toolkit.NotAuthorized as err:
        print("Error : {}".format(err))
        # tampilkan halaman halaman not authorize


    return render_template('metadata/metadata_form.html')

def upload():
    # proses form upload data
    """
        flow :
        -- lakukan validasi form yang dikirim.
        if validasi berhasil: 
            -- proces upload file
            if success:
                - return file path
            else : 
                - return error
            -- lanjut proses simpan ke database, dengan value url \
                berasal dari nilai yang dikembalikan proses upload.
        else :
            - return error
    """
    if not tk.request.method=='POST':
        return jsonify({"message": "method not support"}), 400
    else :
        data = request.form
        print(request.form)
        file = request.files['file']
        url_file = request.form.get('url')
        upload_filename = ''
        print("file : {}", file)
        print("url : {}", url_file )
        print("base upload path: {}", BASE_PATH)

        if _validate_file_upload(file):
            print("validate file: {}", _validate_file_upload(file))
            upload_filename = _upload_file(file)['filename']
        # if _validate_file_upload(url_file):
        #     print("validate file: {}", _validate_file_upload(url_file))
        #     upload_filename = _upload_file(url_file)['filename']

        new_metadata = {
            "owner_org":data.get('owner_org'),
            "title" : data.get('title'),
            "desc" : data.get('desc'),
            "author" : data.get('author'),
            "file_path" : upload_filename
        }
        # request_data = tk.request

        # req = {
        #     'title': request.title,
        #     'desc': request.desc
        # }
        
        data_dict = logic.clean_dict(
            dict_fns.unflatten(
                logic.tuplize_dict(
                    logic.parse_params(tk.request.form)
                )
            )
        )

        # res = tk.get_action('metadata_create')(context={}, data_dict=data_dict)
        res = tk.get_action('metadata_create')(context={}, data_dict=new_metadata)

        print("data to upload: {}", data)

        # return jsonify({"message": "Test gagal", "request":data_dict,
        #                 "request_data": data}), 201
        return tk.redirect_to('metadata.index')

def get(id):
    metadata = tk.get_action('metadata_get')(context={}, data_dict={"id": id})

    # return jsonify({"status": "success", "message": "data ditemukan", "data": metadata}), 201
    return render_template('metadata/metadata_read.html', data=metadata)

def edit(id):
    metadata = tk.get_action('metadata_get')(context={}, data_dict={"id": id})

    return render_template('metadata/metadata_form.html', mode='edit', metadata=metadata)

def update(id):

    # cek method, method harus diganti dengan PUT
    if not tk.request.method=='POST':
        return jsonify({"message": "method not support"}), 400
    else :
        data = request.form
        # print(request.form)

        update_metadata = Metadata(
            organization_id=data.get('owner_org'),
            title=data.get('title'),
            desc=data.get('desc'),
            author=data.get('author')
        )
        # request_data = tk.request

        # req = {
        #     'title': request.title,
        #     'desc': request.desc
        # }
        
        data_dict = logic.clean_dict(
            dict_fns.unflatten(
                logic.tuplize_dict(
                    logic.parse_params(tk.request.form)
                )
            )
        )

        res = tk.get_action('metadata_update')(context={}, data_dict=data_dict)
        res = {}

        print("response: {}", res)
        # -----
        # metadata = tk.get_action('metadata_update')(context={}, data_dict)
        # return jsonify({'mode': 'update'})
        # ----

        # return jsonify({"message": "Test gagal", "request":data_dict,
        #                 "request_data": new_metadata}), 201
        return tk.redirect_to(url_for('metadata.get', id=id))


def delete(id):
    metadata = tk.get_action('metadata_delete')(context={}, data_dict={"id": id})

    # return jsonify(metadata)
    # flash(metadata)

    return tk.redirect_to('metadata.index')

def _validate_file_upload(file):
    # cek jika file ada (file.filename=='')
    # cek allowed file extension 

    if file.filename == '':
        return False
    else :
        return True

def _isallowed_file(file):
    pass

def _upload_file(file):
    # Proses upload file
    filename = secure_filename(file.filename)
    file.save(os.path.join(BASE_PATH, UPLOAD_FOLDER, filename))
    return {'status': 'success', 'filename': filename}

    

bp.add_url_rule(
    "/", endpoint="index", view_func=page)
bp.add_url_rule(
    "/<int:id>", endpoint="get", view_func=get)
bp.add_url_rule(
    "/add", 'create', view_func=create)
bp.add_url_rule(
    "/add", 'upload', view_func=upload, methods=['POST'])
bp.add_url_rule(
    "/edit/<int:id>", "edit", view_func=edit)
bp.add_url_rule(
    "/update/<int:id>", endpoint="update", view_func=update, methods=['POST','PUT'])
bp.add_url_rule(
    "/delete/<int:id>", endpoint="delete", view_func=delete, methods=['POST','DELETE'])

def get_blueprints():
    return [bp]
