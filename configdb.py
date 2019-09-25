"""Configure database connection."""

from os import environ, path

curr_path = path.dirname(__file__)
conf_file = environ.get('EMPDB', 'default.cnf')
conf_path = path.join(curr_path, conf_file)
connect_kwargs = dict(
    read_default_file = conf_path,
    read_default_group = "MySQLdb-emp",
)

def connection_kwargs(kwargs):
    db_kwargs = connect_kwargs.copy()
    db_kwargs.update(kwargs)
    return db_kwargs