# Postgresql setup guide

These instructions are intended for use on Ubuntu, although all major Linux distributions should provide postgres in their package managers. So if you are on another distribution change install commands to work with your package-manager.

1. Install postgres and postgis:
```
sudo apt-get install postgresql postgresql-contrib postgis
```
2. Start postgres:
```
sudo systemctl start postgresql
```
When running ubuntu in [wsl](https://docs.microsoft.com/en-us/windows/wsl/about) run using service instead: `sudo service postgresql start
3. Create user 'simra':
```
sudo -u postgres createuser simra
```
4. Create database 'simra':
```
sudo -u postgres createdb simra
```
5. Set up permissions, passwords and the postgis extension using psql:
```
sudo -u postgres psql
```
Once inside psql:
```
alter user simra with encrypted password 'simra12345simra'; 
grant all privileges on database simra to simra; 
alter role simra superuser; 
create extension postgis; 
```