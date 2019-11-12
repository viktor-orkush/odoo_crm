import pickle
import xmlrpc.client
import time
from datetime import datetime
from config import url, db, username, password
from telegram_bot_api import send_message


def get_closed_pipelines(last_time):
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    closed_pipelines = models.execute_kw(db, uid, password,
                             'crm.lead', 'search_read', [[['stage_id', '=', 4], ['date_closed', '>', last_time]]],
                             {'fields': ['name', 'date_closed', 'stage_id']})
    return closed_pipelines


def get_time_for_last_closed_pipeline():
    with open('saved_var.pkl', 'rb') as file:
        try:
            time_last_closed_pipeline = pickle.load(file)
        except EOFError:
            time_last_closed_pipeline = datetime(2010, 1, 1).strftime("%Y-%b-%d %H:%M:%S")
    return time_last_closed_pipeline


def put_time_for_last_closed_pipeline(time_last_closed_pipeline):
    with open('saved_var.pkl', 'wb') as file:
        pickle.dump(time_last_closed_pipeline, file)


def write_logfile(log_text):
    with open('log_closed_pipeline.txt', 'w+', encoding='utf-8') as file:
        file.write(log_text)


def look_for_new_closed_pipelines(time_last_closed_pipeline):
    closed_pipelines = get_closed_pipelines(time_last_closed_pipeline)
    if closed_pipelines:
        for pipeline in closed_pipelines:
            message = 'Сделка "{}" завершена успешно {}'.\
                    format(pipeline['name'], datetime.strptime(pipeline['date_closed'], '%Y-%m-%d %H:%M:%S'))

            if pipeline['date_closed'] > time_last_closed_pipeline:
                put_time_for_last_closed_pipeline(pipeline['date_closed'])
                time_last_closed_pipeline = pipeline['date_closed']
            write_logfile(message+'\n')
            send_message(message)


if __name__ == "__main__":
    while True:
        look_for_new_closed_pipelines(get_time_for_last_closed_pipeline())
        time.sleep(2)

