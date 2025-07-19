## How to start:
1. Install modules:
``` 
pip install -r requirements.txt
```
⚠ Αυτό το project χρησιμοποιεί ενσωματωμένες βιβλιοθήκες της Python όπως τα tkinter, datetime και hashlib, οι οποίες δεν απαιτούν εγκατάσταση μέσω pip. Βεβαιωθείτε ότι η εγκατάσταση της Python περιλαμβάνει το Tkinter (συνήθως περιλαμβάνεται εξ ορισμού).


2. Clone the repository to your machine:
``` git
git clone https://github.com/panossmav/Airtable-Customer-Manager.git
```
2. Create an Airtable database with the following Tables:
	1. `Customers` with fields:
		1. `Name`: Single line text
		2. `Notes`: Single line text
		3. `Phone`: Number (integer, no decimal)
		4. `Email`: Single line text
	2. `Products` with fields:
		1. `Title`: Single line text 
		2. `Price`: Number (float, 2 decimal)
		3. `SKU`: Autonumber
		4. `Inventory`:Number(integer)
	3. `Orders` with fields:
		1. `Customer`: Single line text
		2. `Status`: Single line text
		3. `Item`: Single line text
		4. `Customer Phone`: Number (integer, no decimal)
		5. `Date / Time`: Single line text
		6. `Order ID`: Autonumber
		7.`Product SKU`: Number (integer)
	4. `App users:` with fields:
		1. `Username`: Single line text
		2. `Password`: Single line text
		3. `User Type`: Single line text
		4. `User ID`: Autonumber
		**Note: you must save a user in the `App users` table, by encrypting the password with SHA256,and setting it as admin (case sensitive) ([Encrypt here](https://emn178.github.io/online-tools/sha256.html))**
	5. `User logs:` with fields:
		1. `User`: Single line text
		2. `Action`: Single line text
		3. `Date / Time`: Single line text
	**Note that all table / column names are case sensitive**
3. Inside `funcs.py` enter your [Airtable API token](https://airtable.com/create/tokens) and base your database ID like this:
>	api_key = 'YOUR_API_TOKEN_GOES_HERE'
>	base_id = 'YOUR_BASE_ID_GOES_HERE'

4. Run `main_app.py` and login with the credentials you made in the `Users` table.

**This is a WIP project. Be cautious!.**

