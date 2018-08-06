import logging, psycopg2, psycopg2.extras, time
from psycopg2.extensions import AsIs
from psycopg2.extras import execute_values

from settings import __config


class Db(object):
    """
    Database handler
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.cnx = psycopg2.connect(**self.__config)
            self.cur = self.cnx.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            self.cur.execute("SET SEARCH_PATH = %s" % 'trademark_app_python')
            self.cnx.commit()
            # self.logger.info('Connected to database')
        except psycopg2.Error as err:
            self.logger.error(err)

    def file_check(self, file):
        zip_filename = file['url'].split('/')[-1]
        xml_filename = zip_filename.replace('zip', 'xml')
        q = "SELECT id, status, filename, date_string FROM trademark_fileinfo WHERE url = %s or filename = %s"
        self.cur.execute(q, (file['url'], xml_filename))
        return self.cur.fetchone()

    def file_insert(self, file, xml_filename):
        q = "INSERT INTO trademark_fileinfo (filename, filesize, url, date_string) VALUES (%s, %s, %s, %s) RETURNING id"
        try:
            start_time = time.time()
            self.cur.execute(q, (xml_filename, file['size'], file['url'], file['date_string']))
            last_row = self.cur.fetchone()
            self.cnx.commit()
            self.logger.debug('Inserted file_info in database [%s sec]', time.time() - start_time)
            return last_row['id']
        except psycopg2.Error as err:
            self.logger.error(err)
            self.cnx.rollback()
        return None

    def file_update_status(self, id, status):
        q = "UPDATE trademark_fileinfo SET status = %s, modified = now() WHERE id = %s RETURNING id, status"
        try:
            self.cur.execute(q, (status, id))
            rowcount = self.cur.rowcount
            self.cnx.commit()
            self.logger.debug('Updated status for file_info in database')
            return rowcount
        except psycopg2.Error as err:
            self.logger.error(err)
        return None

    def serial_get(self, serial_number, file_id):
        q = "SELECT cf.id, cf.created, filename, cf.status FROM trademark_app_case_files cf " \
            "INNER JOIN trademark_fileinfo fi on fi.id = cf.file_id WHERE serial_number = %s"
        self.cur.execute(q, (serial_number,))
        return self.cur.fetchone()

    def case_file_update_status(self, serial_number, status):
        if serial_number is None or status is None:
            logging.error('UPDATE ERROR: Missing serial_number or status')
            return None
        q = "UPDATE trademark_app_case_files SET status = %s, modified = now() WHERE serial_number = %s RETURNING id"
        try:
            self.cur.execute(q, (status, serial_number))
            rowcount = self.cur.rowcount
            self.cnx.commit()
            self.logger.debug('Updated status for case_files in database')
            return rowcount
        except psycopg2.Error as err:
            self.logger.error(err)
        return None

    def delete_serial(self, serial_number, table):
        if serial_number is None or table is None:
            logging.error('DELETE ERROR: Missing serial_number or table')
            return None
        q = 'DELETE FROM %s WHERE serial_number = %s'
        start_time = time.time()
        try:
            q = self.cur.mogrify(q, (AsIs(table), serial_number))
            self.cur.execute(q)
            rowcount = self.cur.rowcount
            self.cnx.commit()
            self.logger.warning('Deleted serial_number %s from table %s [%s sec]', serial_number, table, time.time() - start_time)
            return rowcount
        except psycopg2.Error as err:
            self.logger.error(err)
            self.cnx.rollback()
        return None

    def insert_listdict(self, lst, table):
        if len(lst) == 0 :
            return None
        keys = lst[0].keys()
        columns = ', '.join(keys)
        values = []
        for d in lst:
            values.append(list(d.values()))
        start_time = time.time()
        q = 'INSERT INTO {0} ({1}) values %s RETURNING id'.format(table, columns)
        try:
            execute_values(self.cur, q, values)
            rowcount = self.cur.rowcount
            # self.cur.execute(q)
            self.cnx.commit()
            self.logger.debug('Inserted %s rows in table %s [%s sec]', rowcount, table, time.time() - start_time)
            return rowcount
        except psycopg2.Error as err:
            self.logger.error(err)
            self.cnx.rollback()
        return None

    def insert_dict(self, d, table):
        if d is None or table is None:
            logging.error('INSERT ERROR: Missing dict or table')
            return None
        keys = d.keys()
        columns = ', '.join(keys)
        values = ', '.join(['%({})s'.format(k) for k in keys])
        start_time = time.time()
        q = 'INSERT INTO {0} ({1}) values ({2}) RETURNING id'.format(table, columns, values)
        try:
            q = self.cur.mogrify(q, d)
            self.cur.execute(q)
            self.cnx.commit()
            last_row = self.cur.fetchone()
            self.logger.debug('Inserted id [%s] in table %s [%s sec]', last_row['id'], table, time.time() - start_time)
            return last_row['id']
        except psycopg2.Error as err:
            self.logger.error(err)
            self.cnx.rollback()
        return None
