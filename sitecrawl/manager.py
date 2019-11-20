from flask_script import Manager, Server

from sitecrawl import create_app

app = create_app('testing')
manager = Manager(app)

manager.add_command("runserver",Server(
    host='0.0.0.0',
    port=11010,
    use_debugger=True,
    use_reloader=True))


if __name__ == '__main__':
    manager.run()
