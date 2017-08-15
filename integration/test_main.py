
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .. import server_main
from .. import models


def test_app():
    start_time = datetime.datetime.now()
    models.main()
    data_from_script = server_main.main()
    engine = create_engine('sqlite:///client_statistics.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    client = data_from_script[0]
    db_data = session.query(models.MachineStat).order_by(models.MachineStat.log_time).all()
    db_client = db_data[-1]
    print db_client.ip
    print client.attrib['ip']
    print db_client.ip
    assert client.attrib['ip'] == db_client.ip
    assert start_time < db_client.log_time
    assert db_client.cpu_usage > 0


if __name__ == "__main__":
    test_app()

