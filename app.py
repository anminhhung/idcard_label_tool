from flask import Flask, render_template, jsonify, request, Response, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS

import time 
import traceback
import os 
import random
import logging
import cv2
import string
import zipfile
import shutil
import json

from configparser import SafeConfigParser
from utils import rcode
from src import label_converter as lconvter

#####LOAD CONFIG####
config = SafeConfigParser()
config.read("config/superlabel.cfg")
LOG_PATH = str(config.get('main', 'LOG_PATH'))
SERVER_IP = str(config.get('main', 'SERVER_IP'))
SERVER_PORT = int(config.get('main', 'SERVER_PORT'))
UPLOAD_FOLDER = str(config.get('main', 'UPLOAD_FOLDER'))
CONVERT_LABEL_FOLDER = str(config.get('main', 'CONVERT_LABEL_FOLDER'))
RESULT_FOLDER = str(config.get('main', 'RESULT_FOLDER'))
#######################################
#####CREATE LOGGER#####
logging.basicConfig(filename=os.path.join(LOG_PATH, str(time.time())+".log"), filemode="w", level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)
logger = logging.getLogger(__name__)
#######################################

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
api = Api(app)

#######################################
class sendResult(Resource):
    def post(self):
        ###################
        #####
        print("send_result")
        ###################
        try:
            start_time = time.time()
            result = None
            try:
                json_data = request.get_json(force=True)
                version = json_data['version']
                fname = json_data['fname']
                idnum = json_data['idnum']
                idname = json_data['idname']
                iddob = json_data['iddob']
                idhome = json_data['idhome']
                idaddress = json_data['idaddress']

                print("fname: {}, idnum: {}, idname: {}, iddob: {}, idhome: {}, idaddress: {}".format(fname, idnum, idname, iddob, idhome, idaddress))
            except Exception as e:
                print(str(e))
                print(str(traceback.print_exc()))
                return_result = {'code': '609', 'status': rcode.code_609}
                return;            
            ####################
            data = {'fname': fname, 
                    'idnum': idnum,
                    'idname': idname,
                    'iddob': iddob,
                    'idhome': idhome,
                    'idaddress': idaddress}
                    
            with open(os.path.join(RESULT_FOLDER, ''.join(fname.split('.')[:-1])+".json"), "w") as jf:
                json.dump(data, jf)
            ####################
            return_result = {'status': 'done', 'code': '1000'}
        except Exception as e:
            logger.error(str(e))
            logger.error(str(traceback.print_exc()))
            return_result = {'code': '1001', 'status': rcode.code_1001}
        finally:
            return jsonify(return_result)

class getImgName(Resource):
    def get(self):
        #####
        print("get_img_name")
        ###################
        try:
            start_time = time.time()
            result = None
            try:
                version = request.args.get('version')
                mode = request.args.get('mode')
                index = int(request.args.get('index'))
                print("version: {}, mode: {}, index: {}".format(version, mode, index))
            except Exception as e:
                print(str(e))
                print(str(traceback.print_exc()))
                return_result = {'code': '609', 'status': rcode.code_609}
                return;            
            ####################
            file_list = os.listdir(UPLOAD_FOLDER)
            print("list_image: ", file_list)
            len_file_list = len(file_list)
            if mode == 'index':
                if index >= len_file_list:
                    fname = file_list[0]
                    index = -1
                    print("fname with mode = index: ", fname)
                    print("index with mode = index: ", index)
                else:
                    fname = file_list[index]
                    print("fname with mode = index: ", fname)
                    print("index with mode = index: ", index)
            else:
                # fname = random.choice(file_list)
                index = random.randint(0, len_file_list-1)
                fname = file_list[index]

                print("fname with mode = fname: ", fname)
            
            return_result = {'code': '1000', 'status': rcode.code_1000, 'data':{'fname': fname, 'index': index}}
        except Exception as e:
            logger.error(str(e))
            logger.error(str(traceback.print_exc()))
            return_result = {'code': '1001', 'status': rcode.code_1001}
        finally:
            return jsonify(return_result)

class getLabel(Resource):
    def get(self):
        #####
        print("get_label")
        ###################
        try:
            start_time = time.time()
            result = None
            try:
                version = request.args.get('version')
                fname = str(request.args.get('fname'))
                print(version, fname)
            except Exception as e:
                print(str(e))
                print(str(traceback.print_exc()))
                return_result = {'code': '609', 'status': rcode.code_609}
                return;            
            ####################
            if os.path.isfile(os.path.join(RESULT_FOLDER, ''.join(fname.split('.')[:-1])+".json")):
                with open(os.path.join(RESULT_FOLDER, ''.join(fname.split('.')[:-1])+".json"), "r") as jf:
                    jdata = json.loads(jf.read())

                idnum = jdata['idnum']
                idname = jdata['idname']
                iddob = jdata['iddob']
                idhome = jdata['idhome']
                idaddress = jdata['idaddress']

                my_data = {
                    'fname': fname, 
                    'idnum': idnum,
                    'idname': idname,
                    'iddob': iddob,
                    'idhome': idhome,
                    'idaddress': idaddress
                }

                return_result = {'code': '1000', 'status': rcode.code_1000, 'data': my_data}
            else:
                return_result = {'code': '1201', 'status': rcode.code_1201}
        except Exception as e:
            logger.error(str(e))
            logger.error(str(traceback.print_exc()))
            return_result = {'code': '1001', 'status': rcode.code_1001}
        finally:
            return jsonify(return_result)

class convertLabel(Resource):
    def get(self):
        #####
        print("get_label")
        ###################
        try:
            start_time = time.time()
            result = None
            try:
                fname = str(request.args.get('fname'))
            except Exception as e:
                print(str(e))
                print(str(traceback.print_exc()))
                return_result = {'code': '609', 'status': rcode.code_609}
                return;            
            ####################
            file_out_path = os.path.join(CONVERT_LABEL_FOLDER, 'output', fname+"_out.zip")
            if not os.path.exists(file_out_path):
                return jsonify({'code': '1201', 'status': rcode.code_1201})
            else:
                return send_from_directory(os.path.join(CONVERT_LABEL_FOLDER, 'output'), fname+"_out.zip")
        except Exception as e:
            logger.error(str(e))
            logger.error(str(traceback.print_exc()))
            return jsonify({'code': '1001', 'status': rcode.code_1001})
            
    def post(self):
        ###################
        #####
        print("convert_label")
        ###################
        try:
            start_time = time.time()
            try:
                file_image = request.files.get('file_image',None)
                file_label = request.files.get('file_label',None)
                json_data = json.loads(request.form.get('data'))
                mode = json_data['mode']
                print("mode", mode)
            except Exception as e:
                print(str(e))
                print(str(traceback.print_exc()))
                return_result = {'code': '609', 'status': rcode.code_609}
                return;            
            ####################
            fname = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
            file_image_path = os.path.join(CONVERT_LABEL_FOLDER, "upload", fname+"_image.zip")
            file_label_path = os.path.join(CONVERT_LABEL_FOLDER, "upload", fname+"_label.zip")
            file_out_path = os.path.join(CONVERT_LABEL_FOLDER, 'output', fname+"_out.zip")
            folder_image_path = os.path.join(CONVERT_LABEL_FOLDER, "extract", fname+"_image")
            folder_label_path = os.path.join(CONVERT_LABEL_FOLDER, "extract", fname+"_label")
            folder_out_path = os.path.join(CONVERT_LABEL_FOLDER, "output", fname+"_out")
            file_image.save(file_image_path)
            file_label.save(file_label_path)
            os.mkdir(folder_image_path)
            os.mkdir(folder_label_path)
            os.mkdir(folder_out_path)
            #####process
            print("extracting")
            with zipfile.ZipFile(file_image_path, 'r') as zip_ref:
                zip_ref.extractall(folder_image_path)
            with zipfile.ZipFile(file_label_path, 'r') as zip_ref:
                zip_ref.extractall(folder_label_path)
            #####convert
            print("converting")
            lconvter.pascalvoc_yolo(folder_image_path, folder_label_path, folder_out_path)
            shutil.make_archive(file_out_path.split(".zip")[0], 'zip', folder_out_path)
            #####
            print("remove data")
            os.remove(file_image_path)
            os.remove(file_label_path)
            shutil.rmtree(folder_image_path)
            shutil.rmtree(folder_label_path)
            shutil.rmtree(folder_out_path)
            ####
            os.chmod(file_out_path, 777)
            ####################
            return_result = {'status': 'done', 'code': '1000', 'data': {'fname': fname}}
        except Exception as e:
            logger.error(str(e))
            logger.error(str(traceback.print_exc()))
            return_result = {'code': '1001', 'status': rcode.code_1001}
        finally:
            return jsonify(return_result)

#####################################
####### Add API ##############
api.add_resource(getImgName, '/get_img_name')
api.add_resource(sendResult, '/send_result')
api.add_resource(getLabel, '/get_label')
api.add_resource(convertLabel, '/convert_label')

###################################
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/idcard')
def vew_idcard():
    return render_template('idcard.html')

@app.route('/get_ori_img')
def get_ori_img():
    print("showed image")
    filename = request.args.get('filename')
    img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
#    img = cv2.resize(img, (750, 250)) 
    ret, jpeg = cv2.imencode('.jpg', img)
    return  Response((b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tostring() + b'\r\n\r\n'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/label_converter')
def label_converter():
    print('label_converter')
    return render_template('label_converter.html')

if __name__ == "__main__":
    app.run(host=SERVER_IP, port=SERVER_PORT, debug=True)