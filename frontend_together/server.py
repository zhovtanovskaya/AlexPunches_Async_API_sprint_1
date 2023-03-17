from flask import Flask, render_template, request

app = Flask(__name__,
            static_url_path='/static/',
            static_folder='static',
            template_folder='templates',
            )

@app.route('/<room_id>')
def sample(room_id):
    if bearer := request.headers.get('Authorization'):
        token = bearer.split()[1]
    else:
        token = request.args.get('token')
    return render_template('index.html', room_id=room_id, token=token)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
