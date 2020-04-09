import atexit
import shutil

from api import app


@atexit.register
def delete_files():
    """
    Cleans up the temporary upload-folder
    :return:
    """
    shutil.rmtree(app.config['UPLOAD_FOLDER'])


if __name__ == '__main__':
    from api import routes
    app.run()
