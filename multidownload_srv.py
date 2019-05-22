import aiohttp
import urllib.request
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen,httpclient
import logging
import time
import sys
import traceback
import urllib.request
import tornado.web
import os
from pprint import pprint
# from kousuan_exercise_multidown import  py3_http_reg_exercise_async
import json
import requests
from tornado.options import define, options
import io



"""
python : 3.5+
"""
define("port", default=8777, type=int)

logging.basicConfig(level=logging.INFO,
                    format='asctime:        %(asctime)s \n'  # 时间
                           'filename_line:  %(filename)s_[line:%(lineno)d] \n'  # 文件名_行号
                           'level:          %(levelname)s \n'  # log级别
                           'message:        %(message)s \n',  # log信息
                    filename='/home/nd/workspace/ExerciseServer/workspace/correct_sever_wxf/log/server.log',  # sys.path[1]获取当前的工作路径
                    filemode='a')  # 如果模式为'a'，则为续写（不会抹掉之前的log）


class getanswersheetHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.get_answer_sheet_url = 'http://192.168.46.188:3699/answerSheet_generate'
        # self.get_answer_sheet_url = 'http://52.81.50.11:3699/answerSheet_generate'
        self.server_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.respond = {}
        try:
            print('---- start server with %s ----'%self.request.remote_ip)
            answer_info = self.get_argument("answer_info")
            answer_dic = json.loads(answer_info)
            exercise_id = answer_dic['identifier']
        except:
            print(traceback.format_exc())
            self.respond['error_message'] = "REQUIRE_ARGUMENT"
            self.respond['success'] = 0
            self.respond["server_time"] = self.server_time
            logging.error("getanswersheet : Ip:%s  ; respond:%s  ;error:  %s" % (self.request.remote_ip,self.respond, traceback.format_exc()))
            print('getanswersheet : Ip:%s , REQUIRE_ARGUMENT ERROR   , detail see log ,server_time : %s') % (self.request.remote_ip,self.server_time)
            self.finish(self.respond)
        try:
            with open('answer_backup.json', 'w') as f:
                f.write(answer_info)
        except:
            traceback.print_exc()

        try:
            data = {'exercise_id': exercise_id, 'answer_info': answer_info}
            res = requests.post(self.get_answer_sheet_url, data=data)
            if res.status_code == 500:
                self.respond['error_message'] = "GET_ANSWERSHEET_ERROR"
                self.respond["server_time"] = server_time
                self.respond['success'] = 0
                logging.error("getanswersheet : Ip:%s  ; respond:%s  ;error:  %s" % (self.request.remote_ip,self.respond, traceback.format_exc()))
                print('getanswersheet : Ip:%s , GET_ANSWERSHEET_ERROR   , detail see log ,server_time : %s') % (self.request.remote_ip,self.server_time)
                self.finish(self.respond)
            # print(res.status_code)
            else:
                res_json = json.loads(res.text)
                res_json['error_message'] = ""
                print('---- server done : %s ----'%self.request.remote_ip)
                self.finish(res_json)

        except:
            print(traceback.format_exc())
            self.respond['error_message'] = "SERVER_CONNECTION_REFUSED"
            self.respond["server_time"] = server_time
            self.respond['success'] = 0
            logging.error("getanswersheet : Ip:%s  ; respond:%s  ;error:  %s" % (self.request.remote_ip,self.respond, traceback.format_exc()))
            print('getanswersheet : Ip:%s , SERVER_CONNECTION_REFUSED   , detail see log ,server_time : %s') % (self.request.remote_ip,self.server_time)
            self.finish(self.respond)


class ImageurlHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        self.respond = {}
        self.normal_img_list = []
        self.unnormal_img_list = []
        self.server_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        self.exercise_url = 'http://192.168.46.188:3699/answerSheet_correct'
        # self.exercise_url = "http://52.81.50.11:3699/answerSheet_correct"
        try:
            jdata = json.loads(self.request.body.decode())
            self.callback_url = jdata["callback_url"]
            self.url_list = jdata["url_list"]
            self.requestid = jdata["session_id"]
            try:
                assert isinstance(self.url_list,list)
            except:
                self.respond['error_message'] = "PARAM_TYPE_ERROR:url_list should be list type"
                self.respond['server_time'] = self.server_time
                self.respond['success'] = 0
                self.finish(self.respond)
                print('Correct_server : Ip:%s , PARAM TYPE ERROR   , detail see log ,server_time : %s') % (self.request.remote_ip,self.server_time)
                logging.error("Correct_server : Ip:%s  ; respond:%s  ;error:  %s" % (
                    self.request.remote_ip, self.respond, traceback.format_exc()))
            try:
                assert isinstance(self.callback_url,str)
            except:
                self.respond['error_message'] = "PARAM_TYPE_ERROR:callback_url should be string type"
                self.respond['server_time'] = self.server_time
                self.respond['success'] = 0
                self.finish(self.respond)
                print('Correct_server : Ip:%s , PARAM TYPE ERROR   , detail see log ,server_time : %s' )% (self.request.remote_ip,self.server_time)
                logging.error("Correct_server : Ip:%s  ; respond:%s  ;error:  %s" % (
                    self.request.remote_ip, self.respond, traceback.format_exc()))
            try:
                assert isinstance(self.requestid, str)
            except:
                self.respond['error_message'] = "PARAM_TYPE_ERROR:reqeust_id should be string type"
                self.respond['server_time'] = self.server_time
                self.respond['success'] = 0
                self.finish(self.respond)
                print('Correct_server : Ip:%s , PARAM TYPE ERROR   , detail see log ,server_time : %s' )% (self.request.remote_ip,self.server_time)
                logging.error("Correct_server : Ip:%s  ; respond:%s  ;error:  %s" % (
                    self.request.remote_ip, self.respond, traceback.format_exc()))    

            self.respond['success'] = 1
            self.respond['error_message'] = ''
            # self.write("Your request is being processed. The result will be sent to %s" % callback_url)
            self.finish(self.respond)
            self.start_time = time.time()
            print('start_time:',self.start_time)
            tornado.ioloop.IOLoop.current().add_callback(self.processmian)
            # print('time:', time.time() - start_time)
        except:
            self.respond['error_message'] = "REQUIRE_ARGUMENT"
            self.respond['server_time'] = self.server_time
            self.respond['success'] = 0
            self.finish(self.respond)
            print('REQUIRE_ARGUMENT , detail see log ,server_time : %s'%self.server_time)
            logging.error("Correct_server : Ip:%s  ; respond:%s  ;error:  %s" % (self.request.remote_ip,self.respond, traceback.format_exc()))
            traceback.print_exc()

    @gen.coroutine
    def processmian(self):
        try:
            download_start_time = time.time()
            respond = {}
            # download img list
            print('---- start server with %s ----'%self.request.remote_ip)
            self.path = './img/%s/' % (self.requestid + '-' + str(self.server_time))
            if not os.path.exists(self.path):
                print('文件夹', self.path, '不存在，重新建立')
                os.makedirs(self.path)
            try:
                yield from self.download_main(self.path)
            except:
                pass
            download_end_time = time.time()
            print("downlaod_time",download_end_time-download_start_time)
            
            # end download

            # start correct
            total_correct_item = []
            homework_id = ''
            for url in self.url_list:
                img_name = url.split('/')[-1]
                img_path = self.path + img_name
                # print(os.path.exists(img_path))
                if os.path.exists(img_path):
                    try:
                        success, correct_item, homework_id = yield self.correct_main(img_path)
                        print('homework_id :',homework_id)
                        print('session_id :',self.requestid)
                        print('callback_url :',self.callback_url)
                        if success == 1:
                            correct_item['src_dentryid'] = url
                        total_correct_item.append(correct_item)
                        print('finish correct: %s'%img_name)
                    except:
                        respond['error_message'] = "IMAGE CORRECT ERROR"
                        respond["correct_items"] = total_correct_item
                        respond['success'] = 0
                        respond['homework_id'] = homework_id
                        traceback.print_exc()
                        self.respond = respond
                        print('IMAGE CORRECT ERROR , detail see log ,server_time : %s'%self.server_time)
                        logging.error("Correct_server : Ip:%s  ; respond:%s  ;error:  %s" % (self.request.remote_ip,self.respond, traceback.format_exc()))
                else:
                    res_url = ''
                    total_correct_item.append(res_url)

            if '' in total_correct_item or not total_correct_item:
                respond = {'success:': 0, 'correct_items': total_correct_item,
                                'error_message': "IMG_DOWNLOAD_ERROR","homework_id": homework_id,'session_id':self.requestid}
                self.respond = respond
                print('IMG_DOWNLOAD_ERROR , detail see log ,server_time : %s'%self.server_time)
                logging.error("Correct_server : Ip:%s  ; respond:%s  ;error:  %s" % (self.request.remote_ip,self.respond, traceback.format_exc()))
            else:
                respond = {'success:': 1, 'correct_items': total_correct_item, 'error_message': "",
                                "homework_id": homework_id,'session_id':self.requestid}
                self.respond = respond
                                        
            callback_respond = json.dumps(self.respond)
            client = tornado.httpclient.AsyncHTTPClient()
            answer = None
            try:
            	# yield from client.fetch(self.callback_url, method='POST', body=callback_respond)
                headers = {"Content-type":"application/json"}
                # self.callback_url = self.callback_url.replace('http://','')
                print(self.callback_url)
                print("callback_respond: ",callback_respond)

                answer = requests.post(url = self.callback_url,headers = headers,data =callback_respond)

                print(answer.text)

                # answer = yield from client.fetch(tornado.httpclient.HTTPRequest(url = self.callback_url,headers = headers,method='POST',body=callback_respond))
                # print('answer.body',answer.body)
                end_time = time.time()

                print('----- result sent to %s, server is over -----'%self.callback_url)
                print("end_time",time.time())
                print('cost_time:',time.time()-self.start_time)
                
            except Exception as e:
                print(answer)
                print(e)
                print('callback_url time out , detail see log ,server_time : %s'%self.server_time)
                logging.error("Correct_server : Ip:%s  ; respond:callback_url time out; error: %s" % (self.request.remote_ip, traceback.format_exc()))


            
            
            # print(callback_respond)
        except:
        	print(' ----- Some Error cause , detail see log , server_time : %s  -----'%self.server_time)
        	logging.error("Correct_server : Ip:%s  ; respond:%s  ;error:  %s" % (self.request.remote_ip,self.respond, traceback.format_exc()))
        # finish

    async def download_pics(self, url, path):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                pic = await response.read()  # 以Bytes方式读入非文字
                img_name = url.split('/')[-1]
                with open('%s%s' % (path, img_name),
                          'wb') as fout:  # 写入文件
                    fout.write(pic)
                    img_path = self.path + img_name
                    print('pic: ' + url.split('/')[-1] + ' done!')

    async def correct_main(self, img_path):
        file_data = {"upl_img": open(img_path, 'rb'), }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.exercise_url, data=file_data) as resp:
               response_str = await resp.text()
               response_json  = json.loads(response_str)
               if "error_msg" in response_json:
                    success = 0
                    return success, response_json['error_msg'],''
               else:
                    success = 1
                    return success, response_json['correct_item'], response_json['exercise_id']

    @gen.coroutine
    def download_main(self, path):
        yield [self.download_pics(url, path) for url in self.url_list]


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/homework_correct", ImageurlHandler), (r"/get_answerSheet", getanswersheetHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

