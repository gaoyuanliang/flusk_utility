##############
import time
import logging
import argsparser
from flask_restplus import *
from flask import *

ns = Namespace('jessica', description='')
args = argsparser.prepare_args()

parser = ns.parser()
parser.add_argument('text', type=str, location='json')

req_fields = {'text': fields.String(\
	example = u"this is an input text")\
	}
jessica_api_req = ns.model('jessica', req_fields)

attribute = ns.model('', \
	{'entity': fields.String,\
	'score': fields.Float})

rsp_fields = {\
	'attribute': fields.List(\
	fields.Nested(attribute)),\
	'error':fields.String,\
	'running_time':fields.Float\
	}

jessica_api_rsp = ns.model('jessica', rsp_fields)

@ns.route('/predict')
class jessica_api(Resource):
	def __init__(self, *args, **kwargs):
		super(jessica_api, self).__init__(*args, **kwargs)
	@ns.marshal_with(jessica_api_rsp)
	@ns.expect(jessica_api_req)
	def post(self):		
		start = time.time()
		try:			
			args = parser.parse_args()		
			output = {}
			output['attribute'] = [{'entity':args['text'],\
						     'score':0.978}]
			output['error'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output = {}
			output['error'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output
##############
