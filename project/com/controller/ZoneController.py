from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.ZoneVO import ZoneVO

print('zone controller')


@app.route('/admin/loadZone')
def adminLoadZone():
    try:
        if adminLoginSession() == "admin":
            return render_template('admin/addZone.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertZone', methods=['POST', 'GET'])
def adminInsertZone():
    try:
        if adminLoginSession() == "admin":
            zoneName = request.form['zoneName']
            zoneVO = ZoneVO()
            zoneDAO = ZoneDAO()

            zoneVO.zoneName = zoneName
            zoneDAO.insertZone(zoneVO)

            return redirect(url_for('adminViewZone'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewZone', methods=['GET'])
def adminViewZone():
    try:
        if adminLoginSession() == "admin":
            zoneDAO = ZoneDAO()
            zoneVOList = zoneDAO.viewZone()
            print("__________________", zoneVOList)
            return render_template('admin/viewZone.html', zoneVOList=zoneVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteZone', methods=['GET'])
def adminDeleteZone():
    try:
        if adminLoginSession() == "admin":
            zoneVO = ZoneVO()
            zoneDAO = ZoneDAO()

            zoneId = request.args.get('zoneId')

            zoneVO.zoneId = zoneId
            print(zoneVO)

            zoneDAO.deleteZone(zoneVO)
            return redirect(url_for('adminViewZone'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editZone', methods=['GET'])
def adminEditZone():
    try:
        if adminLoginSession() == "admin":
            zoneVO = ZoneVO()

            zoneDAO = ZoneDAO()

            zoneId = request.args.get('zoneId')

            zoneVO.zoneId = zoneId

            zoneVOList = zoneDAO.editZone(zoneVO)

            print("=======zoneVOList=======", zoneVOList)

            print("=======type of zoneVOList=======", type(zoneVOList))

            return render_template('admin/editZone.html', zoneVOList=zoneVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateZone', methods=['POST', 'GET'])
def adminUpdateZone():
    try:
        if adminLoginSession() == "admin":
            zoneId = request.form['zoneId']
            zoneName = request.form['zoneName']

            zoneVO = ZoneVO()
            zoneDAO = ZoneDAO()

            zoneVO.zoneId = zoneId
            zoneVO.zoneName = zoneName

            zoneDAO.updateZone(zoneVO)

            return redirect(url_for('adminViewZone'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
