from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from config.db import meta, engine

users = Table("users", meta,
              Column("id", Integer, primary_key=True),
              Column("name", String(255)),
              Column("email", String(255)),
              Column("password", String(255)),
              Column("created_at", DateTime),
              Column("updated_at", DateTime),
              Column("deleted_at", DateTime))

meta.create_all(engine)