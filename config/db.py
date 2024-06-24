from sqlalchemy import create_engine, MetaData

#configuration to connect to database
engine = create_engine("mysql+pymysql://root:password@localhost:3306/storedb")

meta = MetaData()

conn = engine.connect()