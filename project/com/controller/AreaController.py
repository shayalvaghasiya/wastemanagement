from flask import render_template, request, url_for, redirect

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.AreaVO import AreaVO


@app.route('/admin/loadArea', methods=['GET'])
def adminLoadArea():
    try:
        if adminLoginSession() == "admin":
            zoneDAO = ZoneDAO()
            zoneVOList = zoneDAO.viewZone()
            return render_template('admin/addArea.html', zoneVOList=zoneVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertArea', methods=['POST', 'GET'])
def adminInsertArea():
    try:

        if adminLoginSession() == "admin":
            areaName = request.form['areaName']

            areaPincode = request.form['areaPincode']

            areaDescription = request.form['areaDescription']

            area_ZoneId = request.form['area_ZoneId']

            areaVO = AreaVO()
            areaDAO = AreaDAO()

            areaVO.areaName = areaName
            areaVO.areaPincode = areaPincode
            areaVO.areaDescription = areaDescription
            areaVO.area_ZoneId = area_ZoneId

            areaDAO.insertArea(areaVO)
            return redirect(url_for('adminViewArea'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewArea')
def adminViewArea():
    try:
        if adminLoginSession() == "admin":
            areaDAO = AreaDAO()

            areaVOList = areaDAO.viewArea()

            print('areaVOList::::', areaVOList)

            return render_template('admin/viewArea.html', areaVOList=areaVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteArea', methods=['GET'])
def adminDeleteArea():
    try:
        if adminLoginSession() == "admin":
            print('in delete')
            areaDAO = AreaDAO()

            print('object created')

            areaId = request.args.get('areaId')
            print('areaId')

            print('now calling delete method')
            areaDAO.deleteArea(areaId)
            print('called method')
            return redirect(url_for('adminViewArea'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/editArea', methods=['GET'])
def adminEditArea():
    try:
        if adminLoginSession() == "admin":
            areaVO = AreaVO()
            areaDAO = AreaDAO()
            zoneDAO = ZoneDAO()

            areaId = request.args.get('areaId')

            areaVO.areaId = areaId
            print('areaVO')

            areaVOList = areaDAO.editArea(areaVO)
            print('areaList')

            zoneVOList = zoneDAO.viewZone()
            print('zoneList')

            return render_template('admin/editArea.html', zoneVOList=zoneVOList, areaVOList=areaVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateArea', methods=['POST', 'GET'])
def adminUpdateArea():
    try:
        if adminLoginSession() == "admin":
            areaName = request.form['areaName']
            areaPincode = request.form['areaPincode']
            areaDescription = request.form['areaDescription']
            area_ZoneId = request.form['area_ZoneId']
            areaId = request.form['areaId']

            areaVO = AreaVO()
            areaDAO = AreaDAO()

            areaVO.areaName = areaName
            areaVO.areaPincode = areaPincode
            areaVO.areaDescription = areaDescription
            areaVO.area_ZoneId = area_ZoneId
            areaVO.areaId = areaId

            areaDAO.updateArea(areaVO)

            print('updated')

            return redirect(url_for('adminViewArea'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
