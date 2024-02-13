from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem (you can use other backends as well)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        session['user_input'] = user_input
        return render_template('result.html')
    return render_template('index.html')

@app.route('/result')
def result():
    user_input = session.get('user_input')
    return render_template('result.html', user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True , host="0.0.0.0" , port=5005)
