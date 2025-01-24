import os
import ckan.plugins.toolkit as toolkit
from ckan.model import Session
from ckanext.metadata.db import Metadata

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'public/uploads'
ALLOWED_EXTENSION = {'pdf'}

def create_metadata(context, data_dict):
    ''' create new metdata entry'''

    # Validate Input
    # toolkit.check_access('metadata_create', context, data_dict)

    # Create new metadata object
    new_metadata = Metadata(
        organization_id = data_dict['owner_org'],
        title = data_dict['title'],
        desc = data_dict['desc'],
        author = data_dict['author'],
        file_path = data_dict['file_path']
    )

    Session.add(new_metadata)
    Session.commit()
    return {'message': 'Metadata created successfully', 'id': new_metadata.id}

    


def get_all_metadata(context, data_dict):
    '''Retrieve all metadata'''
    # toolkit.check_access('metadata_show_all', context, data_dict)

    print("context : {}", context)

    # metadata_id = data_dict['id']
    metadata = Session.query(Metadata).all()
    print(metadata)

    # handle metadata jika data kosong
    # if not metadata:
    #     raise toolkit.ObjectNotFound('Metadata not found')

    # return {}
    metadata_obj = []

    for metadata_item in metadata:
        metadata_obj.append({
            "id": metadata_item.id,
            "title": metadata_item.title,
            "desc": metadata_item.desc,
            "author": metadata_item.author,
            "created": metadata_item.created
        })
    
    # return {
    #     'organization_id': metadata[0].organization_id,
    #     'title': metadata[0].title,
    #     'desc': metadata[0].desc,
    #     'author': metadata[0].author
    # }

    return { "data": metadata_obj }

def get_metadata(context, data_dict):
    '''Retrieve metadata by ID'''
    metadata = Session.query(Metadata).filter_by(id=data_dict['id']).first()

    print("metadata: {}", metadata)

    if not metadata:
        raise toolkit.ObjectNotFound('Metadata not found')
    
    return {
        'id': metadata.id,
        'organization_id': metadata.organization_id,
        'title': metadata.title,
        'desc': metadata.desc,
        'author': metadata.author,
        'file_path': metadata.file_path
    }

def update_metadata(context, data_dict):
    ''' Update metadata by ID '''
    metadata_id = data_dict['id']

    metadata_updated = {
        'organization_id': data_dict['owner_org'],
        'title': data_dict['title'],
        'desc': data_dict['desc'],
        'author': data_dict['author']
    }

    Session.query(Metadata).filter(Metadata.id==metadata_id).\
        update(metadata_updated)

    Session.commit()

    return {'status': 'success', 'message': 'Metadata updated successfully'}

def delete_metadata(context, data_dict):
    ''' Delete metadata by ID '''
    metadata_id = data_dict['id']
    metadata = Session.query(Metadata).filter_by(id=metadata_id).first()

    if not metadata : 
        raise toolkit.ObjectNotFound('Metadata Not Found')

    _delete_file(metadata.file_path)
    Session.delete(metadata)
    Session.commit()

    return { 'message': 'Metadata deleted successfully' }

def _delete_file(filename):
    # proses delete file
    try:
        os.remove(os.path.join(BASE_PATH, UPLOAD_FOLDER, filename))
    except:
        print('Error : Something wrong!')
        return False
    return True