sudo docker exec -it cerberus python3 manage.py createsuperuser


Ensure the volumes are empty.
Run ```docker-compose build _cerberus```.
Run ```docker-compose --profile all up```,
Run ```docker exec -it cerberus createsuperuser```
    Set username and password for django admin access
Open ```localhost:8080`
Login credentials for keycloak login(You can change them from env file) -
    username = USER_NAME
    password = PASSWORD
Add your realm
Add client then edit client Access Type "public to confidential", "ON" Authorization Enabled, set Valid Redirect URIs "http://cerberus.localhost/* and Web Origins to "http://cerberuss.localhost". click on save.
A New tab appeares in Clients near settings tab named "Credentials"
Click on Credentials and copy ```Secret-key```
Now click on ```Users``` from side menu
Click on ```Add User```
Enter username ```cerberus_user``` then save
Click on Credentials and set password ```Cerberus@123```
Go to ```Role mappings``` click on ```client roles -> realm management -> choose "manage-users" and "realm-admin" from Available roles```
Go to ```cerberus.localhost/admin/``` and credentials are same as you set on line 4
Add servers -> URL - ```http://keycloak:8080/``` and internal URL - ```http://keycloak:8080/``` and save
Add realms -> Name - ```same as set on line no 10``` , select server, add client-id - ```same name set on line no 11```, and paste secret-key copied from client credentials then save
Now select realm from checkbox and perform ```Refresh OpenID Connect .well-known, Refresh Certificates and Clear client tokens```
Setup is done. Access any URL from urls.py in cerberus_dango
