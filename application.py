# application.py
from Program.app_factory import create_app

application = create_app()  # The 'application' variable must match the WSGI callable name expected by AWS

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8000, debug=True)
