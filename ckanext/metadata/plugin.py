import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.metadata.views as views

from ckanext.metadata.action import create_metadata, get_all_metadata, get_metadata, delete_metadata, update_metadata
from ckanext.metadata.auth import metadata_create

class MetadataPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        # toolkit.add_resource('fanstatic','metadata')
        toolkit.add_resource('assets','metadata')
        # extra public paths
    
    # IBlueprint
    def get_blueprint(self):
        return views.get_blueprints()

    # IActions
    # @ckan.logic.side_effect_free # decorating function, available to get and post request
    def get_actions(self):
        return {
            'metadata_create': create_metadata,
            'metadata_get_all': get_all_metadata,
            'metadata_get': get_metadata,
            'metadata_update': update_metadata,
            'metadata_delete': delete_metadata
        }
    
    # IAuthFunctions
    def get_auth_functions(self):
        return {'metadata_create': metadata_create}

class MetadataResourcePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IUploader)

    def get_uploader(upload_to, old_filename=None):
        metadata_resource = MetadataResource(upload_to, old_filename)

        return  metadata_resource


class MetadataResource:
    def __init__(self, upload_to, old_filename=None):
        self.UPLOAD_TO = upload_to

    def update_data_dict(data_dict, url_field, clear_field):
        pass

    def upload(max_size):
        return 'dummy: file berhasil diupload'
    