1. Please pip install the following libraries ("pip install" for Windows, "pip3 install" for Mac): 
flask
flask_postgresql 
flask_wtf
psycopg2 
email_validator 
itsdangerous==2.0.1 (compatible version)
flask_bootstrap

2. Database and mail info are stored in env variables, I can share them if requested.

3. The following script should be executed to insert cars into db:
INSERT INTO app.car_base (id, model, license_plate, color,kilometers, car_picture, city) VALUES
	 ('Škoda Octavia', 'VIN12345', 'Blue',100,'octavia.jpg','Praha'),
	 ('Škoda Superb', 'VIN12346', 'Black',50,'superb.jpg','Brno'),
	 ('Volkswagen Golf', 'VIN12347', 'White',150,'golf.jpg','Ostrava'),
	 ('Volkswagen Passat', 'VIN012348', 'Grey',90,'passat.jpg','Praha'),
	 ('Peugeot 308', 'VIN012349', 'Red',200,'308.jpg','Praha'),
	 ('Renault Clio', 'VIN012350', 'Yellow',30,'clio.jpg','Ostrava'),
	 ('Ford Focus', 'VIN012351', 'Silver',300,'focus.jpg','Brno'),
	 ('Mercedes-Benz C-Class', 'VIN012352', 'Black',50,'cclass.jpg','Brno'),
	 ('Audi A4', 'VIN012353', 'Blue',75,'a4.jpg','Praha'),
	 ('BMW 3 Series', 'VIN012354', 'White',85,'3series.jpg','Praha');

4. The database should be open either through DBeaver or pgAdmin 4 to create a connection.

5. Run the application either by clicking the run button in the run.py file or executing "python run.py" ("python3 run.py" for mac).
