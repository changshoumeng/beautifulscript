from flask import Flask, jsonify
 
app = Flask(__name__)
 
 
@app.route('/', methods=['POST','GET'])
def root():
    t = {
        'a': 1,
        'b': 2,
        'c': [3, 4, 5]
    }
    return jsonify(t)



@app.route('/v1/im/add_user_auth', methods=['POST','GET'])
def add_user_auth():
    t = {
	"ActionStatus":"ok",
	"ErrorCode":0,
	"ErrorInfo":"",
	"UserList":[
		{
			"UserID":"11",
			"NickName":"22",
			"Token":"xxxxx"
		}
	]
    }
    return  jsonify(t)
    









 
if __name__ == '__main__':
    app.debug = True
    app.run(
	host = '0.0.0.0',
        port = 80,  
        debug = True )
