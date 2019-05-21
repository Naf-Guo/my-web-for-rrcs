from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from RRCS import cal_rrcs



# configuration
DEBUG = True

# instatiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# sanity check route


@app.route('/rrcs-cal', methods=['POST'])
def rrcs_cal():
	file = request.files['file']
	print(request.form.get('gpcrdb_id'))
	chain = request.form.get('chain')
	filename = file.filename
	gpcrdb_id = request.form.get('gpcrdb_id')
	lines = read_pdb(file, chain)
	rrcs_result = cal_rrcs(lines, gpcrdb_id, filename)
	for line in rrcs_result:
		print(line)
	return jsonify({'rrcs_result': rrcs_result})



def read_pdb(file, chainS):
	atoms = []
	lines = file.readlines()
	for line in lines:
		lin = str(line, encoding='utf-8')
		if lin[0:4] == 'ATOM':
			chain = lin[21:22]
			if chain == chainS and lin[12:16].strip()[0] != 'H':
				lin1 = lin
				atoms.append(lin1[:])
	return atoms



if __name__ == '__main__':
	app.run()
