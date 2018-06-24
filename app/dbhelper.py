import sqlite3
import pandas as pd 
class DBHelper:
    def __init__(self, dbname="calendar.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False) 
    '''
    def setup(self):
        #tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"db.conn.execute("create table if not exists items (description text, owner text")
        self.conn.execute("create table if not exists items (description text, owner text)")
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        #self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()
    '''
    def add_item(self, user_id, event_id, start_date, end_date):
        stmt = "INSERT INTO cal (user_id, event_id, start_date, end_date) VALUES (?, ?, ?, ?)"
        args = (user_id, event_id, start_date, end_date)
        self.conn.execute(stmt, args)
        self.conn.commit()
    def delete_item(self, user_id, event_id, start_date, end_date):
        stmt = "DELETE FROM cal WHERE user_id = (?), event_id = (?), start_date = (?), end_date = (?)" 
        args = (user_id, event_id, start_date, end_date)
        self.conn.execute(stmt, args)
        self.conn.commit()
    def get_schedule(self, user_id):
        stmt = "SELECT start_date, end_date FROM cal WHERE user_id = (?)"
        args = (user_id)
        return [[x[0],x[1]] for x in self.conn.execute(stmt, args)]
    def get_free_time(self, user_id, small_limit = None , big_limit = None):
        if (small_limit == None) and (big_limit == None):
            busy_time = self.get_schedule(user_id)
            #busy_time = busy_time.sort(key=lambda x: x[0])
            free_time = [] 
            for i in range(len(busy_time)-1):
                free_time.append([busy_time[i][1], busy_time[i+1][0]])
            free_time.append([busy_time[-1][1],busy_time[0][0]])
        else: 
            busy_time = self.get_schedule(user_id)
            #busy_time = busy_time.sort(key=lambda x: x[0])
            free_time = [] 
            for i in range(len(busy_time)-1):
                l1 = pd.Timestamp(str(busy_time[i][1]))
                l2 = pd.Timestamp(str(busy_time[i+1][0]))
                if (l1 > small_limit) and (l2 < big_limit): 
                    free_time.append([busy_time[i][1], busy_time[i+1][0]])
            l1 = pd.Timestamp(str(busy_time[-1][1]))
            l2 = pd.Timestamp(str(busy_time[0][0]))
            if (l1 > small_limit) and (l2 < big_limit): 
                free_time.append([busy_time[i][1], busy_time[i+1][0]])
        return free_time
