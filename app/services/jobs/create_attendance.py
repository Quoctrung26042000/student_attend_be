import logging
import pathlib
import sys
from sqlalchemy import engine_from_config, pool, create_engine, MetaData, Table, insert, select
import os

try :
    logging.basicConfig(filename="D:/student_attend_be/app/services/jobs/app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # logging.info('Path log', log_path)
    sys.path.append("D:/student_attend_be")
    # logging.info('Parrent', sys.path.append(str(pathlib.Path(__file__).resolve().parents[3])))
    logging.info('Import libary...')
    from app.core.config import get_app_settings  # isort:skip
except Exception as e :
    logging.ERROR("Error", e)

logging.info('Import libary.1123232111..')
engine = create_engine("postgresql://postgres:postgres@localhost/postgres")
metadata = MetaData()
student_table = Table('student', metadata, autoload=True, autoload_with=engine)
attendance_table = Table('attendance', metadata, autoload=True, autoload_with=engine)

logging.info('Import libary.1111111111111111..')
try :
    logging.info('Import Database...')
    with engine.connect() as connection:
        query = student_table.select()
        result = connection.execute(query)
        all_students = result.fetchall()
        for student in all_students:
            student_id = student['id']  
            insert_query = insert(attendance_table).values(student_id=student_id)
            connection.execute(insert_query)
except Exception as e :
    logging.debug('Erro', e)

logging.info('Done')
logging.shutdown()
