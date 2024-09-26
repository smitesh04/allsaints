import pymysql

class DbConfig():

    def __init__(self):
        self.con = pymysql.Connect(host='localhost',
                              user='root',
                              password='actowiz',
                              database='allsaints')
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)
        self.store_table = 'us_stores'
        self.data_table = 'data'

    def insert_store_table(self, item):

        query = f'''
                        INSERT INTO {self.store_table} (store_link, country, state)
                        VALUES (%s, %s, %s)
                        '''
        data = (
            item["store_link"],
            item["country"],
            item["state"]

        )

        try:
            self.cur.execute(query.format(data_table=self.store_table), data)
            self.con.commit()
            print(item)
        except Exception as e:
            print(e)

    def insert_data_table(self, item):

        query = f'''
                        INSERT INTO {self.data_table} (store_no, name, latitude, longitude, street, city, state, zip_code, county, phone, open_hours, url, provider, category, updated_date, country, status, direction_url, pagesave_path)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        '''
        data = (
            item["store_no"],
            item["name"],
            item["latitude"],
            item["longitude"],
            item["street"],
            item["city"],
            item["state"],
            item["zip_code"],
            item["county"],
            item["phone"],
            item["open_hours"],
            item["url"],
            item["provider"],
            item["category"],
            item["updated_date"],
            item["country"],
            item["status"],
            item["direction_url"],
            item["pagesave_path"]

        )

        try:
            self.cur.execute(query.format(data_table=self.data_table), data)
            self.con.commit()
            print(item)
        except Exception as e:
            print(e)

    def update_store_status(self, id):
        qr = f'''
            update {self.store_table} set status = 1 where id = {id}
        '''
        self.cur.execute(qr)
        self.con.commit()