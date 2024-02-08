#!/bin/bash

printf "Do you want to reset the database? (Y/N) "
read answer

if [ "$answer" != "${answer#[Yy]}" ]; then
	echo -e "=== ${RED}Dropping evennia database${ENDCOLOR} ==="
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "DROP DATABASE IF EXISTS evennia;"
	echo -e "=== ${GREEN}Dropped evennia database${ENDCOLOR} ==="
	echo -e "=== ${GREEN}Creating evennia database${ENDCOLOR} ==="
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "CREATE DATABASE IF NOT EXISTS  evennia /*\!40100 DEFAULT CHARACTER SET utf8 */;"
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "CREATE USER IF NOT EXISTS evennia@localhost IDENTIFIED BY 'evennia1234';"
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "GRANT ALL PRIVILEGES on evennia.* TO 'evennia'@'localhost';"
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "FLUSH PRIVILEGES;"
	echo -e "=== ${GREEN}Created evennia database${ENDCOLOR} ==="
	echo -e "=== ${GREEN}Migrating evennia data to databse${ENDCOLOR} ==="
	evennia migrate
	mysql -h10.0.10.3 -uroot -p7f927v88 -e "USE evennia;INSERT INTO `accounts_accountdb` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `db_key`, `db_typeclass_path`, `db_date_created`, `db_lock_storage`, `db_is_connected`, `db_cmdset_storage`, `db_is_bot`) VALUES
(1, 'pbkdf2_sha256$390000$qZgu2obdQvsHx39kbhFH9W$Q90oH3T4ET81DkqhhuIE4QXXy+mXGzXBX3Ti+ENs+Rw=', '2024-02-08 01:53:24.281916', 1, 'admin', '', '', '', 1, 1, '2024-02-08 01:53:15.021485', '', 'typeclasses.accounts.Account', '2024-02-08 01:53:15.542051', 'examine:perm(Developer);edit:false();delete:false();boot:false();msg:all();noidletimeout:perm(Builder) or perm(noidletimeout)', 0, 'commands.default_cmdsets.AccountCmdSet', 0),
(2, 'pbkdf2_sha256$390000$ETzXd3MUf3iUeeBke1tmiY$OLufmiYNRRD2ieEdGO7P+SyyBtOLNarbRi3R2asmMvE=', NULL, 1, 'vorkane', '', '', '', 1, 1, '2024-02-08 01:53:59.000000', '', 'typeclasses.accounts.Account', '2024-02-08 01:53:59.724854', 'examine:perm(Developer);edit:false();delete:false();boot:false();msg:all();noidletimeout:perm(Builder) or perm(noidletimeout)', 0, 'commands.default_cmdsets.AccountCmdSet', 0);"

else
	echo "No"
	exit
fi
