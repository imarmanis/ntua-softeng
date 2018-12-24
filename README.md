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

### Configurations

Tα βασικά στο config.py.

Στο instance/config.py (μένει εκτός git) βάζει ο καθένας τα δικά του, θα κάνουν override το config.py.

Πχ το instance/config.py για mysql:
```python
import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                          'mysql+pymysql://root:root@localhost:3306/restapi'
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
