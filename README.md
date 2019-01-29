# ntua-softeng
## SoftEng NTUA 2018-2019 Project
### Oμάδα FooBar
[//]: # (Αλφαβητικά, επώνυμο)

Επώνυμο | Όνομα | Αριθμός Μητρώου
--- | --- | ---
Μαρμάνης | Ιάσων | 03114088
Μουζάκης | Ανάργυρος-Γεώργιος | 03114103
Μουζάκης | Νικόλαος | 03114008
Ξενάκης | Φώτιος  | 03114104
Ξεφτέρης | Μιχάλης | 03114006

## Flask backend
`cd backend/`

### Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Κάθε επόμενη φορά
`source venv/bin/activate`

### DB

Μετά από αλλαγή στο σχήμα της βάσης:
```bash
flask db migrate -m "Added foobar table" : δημιουργεί το script που θα αλλάξει τη βάση
flask db upgrade : upgrade τη βάση στο πιο πρόσφατο σχήμα
```


#### DBMS

Για geospatial db με υποστήριξη ORM (geoalchemy) χρειαζόμαστε PostgreSQL με το PostGIS extension.

##### Παράδειγμα εγκατάστασης με docker
```bash
docker volume create pg_data
docker run --name postgis -e POSTGRES_PASSWORD=root -e POSTGRES_USER=root -e POSTGRES_DB=restapi -v pg_data:/var/lib/postgresql/data -p 5432:5432 -d mdillon/postgis
```

Σε κάθε επόμενη έναρξη :
```bash
docker start postgis
```

### Configurations

Tα βασικά στο config.py.

Στο instance/config.py (μένει εκτός git) βάζει ο καθένας τα δικά του, θα κάνουν override το config.py.

Πχ το instance/config.py για postgreSQ:
```python
import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://root:root@localhost:5432/restapi'
SQLALCHEMY_ECHO = True
```
Πρέπει να υπάρχει έστω και κενό.

### Dotfiles
.flaskenv : FLASK_APP, PORT etc

.env : μένει εκτός git, κάνει override το .flaskenv

Πχ αν δεν θέλω debug mode : FLASK_DEBUG=False στο .env

### Run
`flask run`

Για δοκιμή των HTTP methods υπάρχει το Postman

### HTTPS

Στο secret/ πρέπει να υπάρχουν τα αρχεία {cert, key}.pem για
το self-signed certificate και το private key.
Δημιουργία πχ με:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

## Επέκταση στο API
- `POST {baseURL}/register`

Δημιουργία νέου χρήστη με ρόλο Εθελοντή. Το username πρέπει να μην ανήκει σε
κανέναν υπάρχοντα χρήστη. Δεν γίνεται αυτόματα σύνδεση του νέου χρήστη.
Υποστηριζόμενες παράμετροι ακριβώς όπως και για το login (στο request body):

Όνομα | Περιγραφή
----- | ---------
username | String. Υποχρεωτικό. Το username του νέου χρήστη.
password | String. Υποχρεωτικό. Το password του νέου χρήστη. 
