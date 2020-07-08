import platform
import pymysql

pymysql.install_as_MySQLdb()
separator = '\\' if platform.system() == 'Windows' else '/'