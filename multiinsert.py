import logging, psycopg2, psycopg2.extras, time
from psycopg2.extensions import AsIs
from psycopg2.extras import execute_values


class Db(object):
    """
    Database handler
    """
    __config = {
        'user': 'postgres',
        'password': 'Jk7aWctVX5',
        'host': '127.0.0.1',
        'database': 'trademark'
    }

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
            print(q)
            exit()
            self.cur.execute(q)
            self.cnx.commit()
            last_row = self.cur.fetchone()
            self.logger.debug('Inserted id [%s] in table %s [%s sec]', last_row['id'], table, time.time() - start_time)
            return last_row['id']
        except psycopg2.Error as err:
            self.logger.error(err)
            self.cnx.rollback()
        return None

    def insert_dict2(self, list1, table):
        if l is None or table is None:
            logging.error('INSERT ERROR: Missing dict or table')
            return None
        keys = l[0].keys()
        columns = ', '.join(keys)
        # values = ', '.join(['%({})s'.format(k) for k in keys])
        # values = ', '.join(['%s' for k in keys])
        values = []
        for d in list1:
            values.append(list(d.values()))
        print(values)
        start_time = time.time()
        q = 'INSERT INTO {0} ({1}) values (%s) RETURNING id'.format(table, columns)
        print(q)
        try:
            execute_values(self.cur, q, values)
            # q = self.cur.mogrify(q, l)
            print(q)
            exit()
            self.cur.execute(q)
            self.cnx.commit()
            last_row = self.cur.fetchone()
            self.logger.debug('Inserted id [%s] in table %s [%s sec]', last_row['id'], table, time.time() - start_time)
            return last_row['id']
        except psycopg2.Error as err:
            self.logger.error(err)
            self.cnx.rollback()
        return None

dict1 = {'ime': 'Vasko', 'prezime': 'Kelkocev', 'v': 38}
dict2 = {'ime': 'Viki', 'prezime': 'Kelkocev', 'v': 36}
dict3 = {'ime': 'Ema', 'prezime': 'Kelkocev', 'v': 1}
l = [dict1, dict2, dict3]

dbc = Db()
dbc.insert_dict2(l, 'tabela')
