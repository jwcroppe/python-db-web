# A simple Flask-based application that opens an SSH tunnel to a remote
# server over which MySQL (version 3.23) connections are made. The application
# queries for some users and displays some basic information about them.
#
# The following environment variables can be defined to customize the runtime:
#   SSH_REMOTE_SERVER: remote endpoint address for the SSH tunnel
#   SSH_REMOTE_PORT: remote endpoint port for the SSH tunnel (default: 22)
#   SSH_REMOTE_USER_NAME: user name on the remote SSH server (default: root)
#   SSH_REMOTE_PASSWORD: password for the user on the remote SSH server (default: s3cur3Pa5sw0rd)
#   SSH_TUNNEL_LOCAL_PORT: local port to be used for the SSH tunnel (default: 3306)
#   FLASK_HOST: host name on the local server for the Flask server (default: 0.0.0.0)
#   FLASK_PORT: port on the local server for the Flask server (default: 5000)
#   ENTITY_NAME: name of the event to display when the page is rendered (default: IBM Systems Tech U Attendees)

from configdb import connection_kwargs
from flask import Flask, render_template
from sshtunnel import SSHTunnelForwarder

import MySQLdb
import os

app = Flask(__name__)
server = SSHTunnelForwarder(
    (os.environ.get("SSH_REMOTE_SERVER"),
     int(os.environ.get("SSH_REMOTE_PORT", "22"))),
    ssh_username=os.environ.get("SSH_REMOTE_USER_NAME", "root"),
    ssh_password=os.environ.get("SSH_REMOTE_PASSWORD", "s3cur3Pa5sw0rd"),
    set_keepalive=5.0,
    remote_bind_address=("localhost", 3306),
    local_bind_address=("127.0.0.1",
                        int(os.environ.get("SSH_TUNNEL_LOCAL_PORT", "3306")))
)
entity_name = os.environ.get("ENTITY_NAME", "IBM Systems Tech U Attendees")


server.start()


class Database:
    driver = MySQLdb
    connect_args = ()
    connect_kw_args = connection_kwargs({})

    def _connect(self):
        return self.driver.connect(*self.connect_args, **self.connect_kw_args)

    def list_employees(self):
        con = None
        result = None

        try:
            con = self._connect()
            cur = con.cursor()
            cur.execute(
                "SELECT first_name, last_name, gender FROM employees LIMIT 50")
            result = map(lambda x: {
                         'first_name': x[0], 'last_name': x[1], 'gender': x[2]}, cur.fetchall())
        finally:
            if con is not None:
                con.close()

        return result


@app.route('/')
def employees():

    def db_query():
        db = Database()
        emps = db.list_employees()

        return emps

    res = db_query()

    return render_template("employees.html", result=res, entity_name=entity_name,
                           content_type="application/json")


if __name__ == "__main__":
    app.run(host=os.environ.get("FLASK_HOST", "0.0.0.0"),
            port=int(os.environ.get("FLASK_PORT", 5000)))
