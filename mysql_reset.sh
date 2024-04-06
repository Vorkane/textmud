#!/bin/bash

RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

printf "Do you want to reset the database? (Y/N) "
read answer


if [ "$answer" != "${answer#[Yy]}" ]; then
	echo -e "=== ${RED}Stopping evennia services${ENDCOLOR} ==="
#	evennia stop
	echo -e "=== ${RED}Dropping evennia database${ENDCOLOR} ==="
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "DROP DATABASE IF EXISTS evennia;"
	echo -e "=== ${GREEN}Dropped evennia database${ENDCOLOR} ==="
	echo -e "=== ${GREEN}Creating evennia database${ENDCOLOR} ==="
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "CREATE DATABASE IF NOT EXISTS  evennia /*\!40100 DEFAULT CHARACTER SET utf8 */;"
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "CREATE USER IF NOT EXISTS 'evennia'@'%' IDENTIFIED BY 'evennia1234';"
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "GRANT ALL PRIVILEGES on evennia.* TO 'evennia'@'%';"
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "FLUSH PRIVILEGES;"
	echo -e "=== ${GREEN}Created evennia database${ENDCOLOR} ==="
	sleep 5
	echo -e "=== ${GREEN}Migrating evennia data to database${ENDCOLOR} ==="
	evennia migrate
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "USE evennia;INSERT INTO accounts_accountdb (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, db_key, db_typeclass_path, db_date_created, db_lock_storage, db_is_connected, db_cmdset_storage, db_is_bot) VALUES (1, 'pbkdf2_sha256$600000$7KXiqrBUg9nhhOG25Nyjyx$pVe0GcKuYg5eyeCGYC33e+K4D3NpI6syMHpy4lLLaE0=', '2024-02-08 01:53:24.281916', 1, 'admin', '', '', '', 1, 1, '2024-02-08 01:53:15.021485', '', 'typeclasses.accounts.Account', '2024-02-08 01:53:15.542051', 'examine:perm(Developer);edit:false();delete:false();boot:false();msg:all();noidletimeout:perm(Builder) or perm(noidletimeout)', 0, 'commands.default_cmdsets.AccountCmdSet', 0),(2, 'pbkdf2_sha256$600000$7KXiqrBUg9nhhOG25Nyjyx$pVe0GcKuYg5eyeCGYC33e+K4D3NpI6syMHpy4lLLaE0=', NULL, 1, 'vorkane', '', '', '', 1, 1, '2024-02-08 01:53:59.000000', '', 'typeclasses.accounts.Account', '2024-02-08 01:53:59.724854', 'examine:perm(Developer);edit:false();delete:false();boot:false();msg:all();noidletimeout:perm(Builder) or perm(noidletimeout)', 0, 'commands.default_cmdsets.AccountCmdSet', 0);"
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "USE evennia;INSERT INTO accounts_accountdb_db_tags (accountdb_id, tag_id) VALUES (2, 1), (2, 2);"
	echo -e "=== ${GREEN}Remember to start evennia services${ENDCOLOR} ==="
else
	echo "No"
	exit
fi
