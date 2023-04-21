import os
from peewee import AutoField, Model, CharField, IntegerField, FloatField, TextField, IntegrityError
from playhouse.db_url import connect

PG_CONN_STR = os.environ["PG_CONN_STR"]
db = connect(PG_CONN_STR)


class Episode(Model):
    id = AutoField(primary_key=True)
    path = CharField(unique=True, index=True)
    title = TextField()
    link = TextField()
    collection_name = CharField()
    duration = FloatField(null=True)

    class Meta:
        database = db  # set the database connection for the model

    @classmethod
    def upsert_episode(cls, path, title, link, collection_name):
        try:
            with db.atomic():
                episode = cls.create(
                    path=path,
                    title=title,
                    link=link,
                    collection_name=collection_name,
                )
                return episode.id
        except IntegrityError:
            episode = cls.get(path=path)
            episode.title = title
            episode.link = link
            episode.collection_name = collection_name
            episode.save()
            return episode.id


def create_table():
    db.connect()
    db.create_tables([Episode])


create_table()


if __name__ == "__main__":
    pass
