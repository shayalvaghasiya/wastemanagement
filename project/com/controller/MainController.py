from flask import render_template

from project import app

print('main c')


@app.route('/admin/viewDetection')
def adminViewDetection():
    try:
        return render_template('admin/viewDetection.html')
    except Exception as ex:
        print(ex)
