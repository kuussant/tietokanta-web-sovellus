# tietokanta-web-sovellus-harjoitustyo
## "Mini Reddit" -app

### Main functionalities
Users can create subforums
Users can follow subforums and create discussions within
Users can comment on discussions
Users can delete their comments, discussions, subforums or accounts

### Usage
The app runs on a local psql database.

For this and encrypted passwords a .env file must be created in the root folder.

Example .env file

```
DATABASE_URL=postgresql+psycopg2://
SECRET_KEY='96c16a15df9d4cae935a89dce8578013'
```

Copy DATABASE_URL=postgresql+psycopg2:// as-is into your .env file.

You can generate your own SECRET_KEY with the following python3 commands:
```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
'18fd24bf6a2ad4dac04a33963db1c42f'
```

To add the schema.sql file to your local database type:
```
(venv) $ psql < schema.sql
```