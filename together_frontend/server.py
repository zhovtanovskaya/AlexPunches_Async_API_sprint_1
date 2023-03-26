from flask import Flask, render_template, request

from config import config

app = Flask(__name__,
            static_url_path='/assets/',
            static_folder='assets',
            template_folder='templates',
            )


@app.route('/ws/<room_id>')
def sample(room_id: str):
    if bearer := request.headers.get('Authorization'):
        token = bearer.split()[1]
    else:
        token = request.args.get('token')
    return render_template(
        'index.html',
        room_id=room_id,
        token=token,
        ws_host=config.cloud_host,
        ws_port=config.cloud_port,
    )


if __name__ == '__main__':
    app.run(host=config.frontend_host, port=config.frontend_port)
