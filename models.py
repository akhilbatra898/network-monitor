#!/usr/bin/python

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.orm import validates

Model = declarative_base()


class MachineStat(Model):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    cpu_usage = Column(Integer)
    memory_usage = Column(Integer)
    machine_type = Column(String)
    uptime = Column(BigInteger)
    os = Column(String)
    log_time = Column(DateTime, default=datetime.datetime.now)

    """
    @validates('cpu_usage')
    def validate_cpu_usage(self, key, value):
        assert True

    @validates('ip')
    def validate_ip(self, key, value):
        data = value.split('.')
        assert (len(data) == 4)
        for i in data:
            assert i.isdigit()
    """

def add(data):
    print data
    machine_stat = MachineStat(machine_type = data['machine_type'],
                                   os=data['os'],
                                   cpu_usage=data['cpu_usage'],
                                   memory_usage=data['memory_usage'],
                                   uptime=data['uptime'],
                                   ip=data['ip']
                                   )
    return machine_stat


def main():
    engine = create_engine('sqlite:///client_statistics.db', echo=True)
    Model.metadata.create_all(engine)

if __name__ == "__main__":
    main()

