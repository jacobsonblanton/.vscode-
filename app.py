# File to run web app 

from ticket_system_2 import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)