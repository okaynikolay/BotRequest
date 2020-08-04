import psycopg2 

class TestReqBD():
    '''
    класс для работы бота TestRequest с базой данных
    '''
    def __init__(self, database, user, password, host, port):
        '''
        Для инициализации принимаются database, user, password, host и port, 
        для подключения к нужной бд
        '''
        con = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
        self.con = con
        self.cur = con.cursor()

    def get_admin(self):
        '''
        Метод возвращает id админа из таблицы user_ids
        '''
        cur = self.cur
        cur.execute("SELECT user_id FROM user_ids WHERE admin = True")
        admin = cur.fetchall()[0][0]
        return admin

    def get_urls(self):
        '''
        Метод возвращает list, содержащий url адреса из бд urls
        '''
        cur = self.cur
        urls = []
        cur.execute("SELECT url FROM urls")
        rows = cur.fetchall()
        for row in rows:
            urls.append(row[0])
        return urls

    def get_users(self):
        '''
        Метод возвращает list, содержащий id подписчиков бота из бд user_ids
        '''
        cur = self.cur
        users =[]
        cur.execute("SELECT user_id FROM user_ids")
        rows = cur.fetchall()
        for row in rows:
            users.append(row[0])
        return users

    def change_admin(self, new_id):
        '''
        Метод меняет админа в бд user_ids
        '''
        cur = self.cur
        cur.execute("UPDATE user_ids SET admin = False WHERE admin = True")
        cur.execute("UPDATE user_ids SET admin =True WHERE user_id = {}".format(new_id))
        self.con.commit()

    def drop_url(self, url):
        '''
        Метод удаляет введенный url из бд urls
        '''
        cur = self.cur
        cur.execute("DELETE FROM urls WHERE url = '{}'".format(url))
        self.con.commit()

    def add_url(self, url):
        '''
        Метод добавляет введенный url в бд urls
        '''
        cur = self.cur
        cur.execute("INSERT INTO urls(id, url) VALUES((SELECT MAX(id) + 1 FROM urls), '{}')".format(url))
        self.con.commit()

    def add_user(self, user):
        '''
        Метод добавляет пользователя в бд user_ids
        '''
        cur = self.cur
        cur.execute("INSERT INTO user_ids(ids, admin, user_id) VALUES((SELECT MAX(ids) + 1 FROM user_ids), False, {})".format(user))
        self.con.commit()

database = 'deb835kopu38ms'
user = 'ulpmxogeoykreg'
password = 'efa33982c38a7c5135fab2b4647914b8905d0baceb8bcf3929b04fab075bc8ab'
host = 'ec2-34-225-162-157.compute-1.amazonaws.com'
port = '5432'

test = TestReqBD(database, user, password, host, port)
print(test.get_urls())
