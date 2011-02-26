Deploy
======

$ ssh USER@SERVERNAME
$ sudo adduser tbdd
password: <*****>
$ sudo -u tbdd mkdir ~tbdd/.ssh
$ sudo cp .ssh/authorized_keys ~tbdd/.ssh/authorized_keys
$ sudo chmod -R 0700 ~tbdd/.ssh && sudo chown -R tbdd.tbdd ~tbdd/.ssh
$ ^D

$ fab -H USER@SERVERNAME live setup
$ fab -H USER@SERVERNAME live deploy
