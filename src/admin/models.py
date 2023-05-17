from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
from flask_admin.form.upload import ImageUploadField

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads')



class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('auth.login'))


class SecureAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('auth.login'))


class UserModelView(SecureModelView):
    column_searchable_list = ["username", "email"]
    column_list = ["username", "email", "roles"]
    column_editable_list = ["username"]

    form_excluded_columns = ["password"]


class AuthorModelView(SecureModelView):
    column_searchable_list = ["first_name", "last_name",  "email_address"]


class PostModelView(SecureModelView):
    column_list = ['title', 'date', 'author']
    column_filters = ["author", "tags", "date"]
    
      
    form_extra_fields = {
        'image_name': ImageUploadField('Image',
                                       base_path=UPLOAD_FOLDER, 
                                       url_relative_path='uploads/',
                                       thumbnail_size=(100, 100, True))
    }
    
    def on_model_change(self, form, model, is_created):
            model.generate_slug()
            model.create()
            if form.image_name.data:
                filename = secure_filename(form.image_name.data.filename)
                form.image_name.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))


class TagModelView(SecureModelView):
    column_searchable_list = ["caption"]
   

