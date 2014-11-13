import sys
sys.path.insert(0, 'E:\Development\libraries')
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request


app = Flask(__name__)
@app.route('/')
def start():
		
	return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)