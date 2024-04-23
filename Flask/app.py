from flask import Flask, request, render_template ,send_file
from markupsafe import escape

app = Flask(__name__)


#index file
@app.route('/')
def index():
    return render_template('./index.html')

if __name__ == "__main__":
    app.run(host='localhost', port=5005)