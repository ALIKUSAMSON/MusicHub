from flask_uploads import UploadSet, IMAGES, configure_uploads


images = UploadSet('images', IMAGES)

configure_uploads(app, images)
