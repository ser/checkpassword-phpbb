#!/usr/bin/env python3
#
# (C) Serge Victor, LGPLv3 license
# https://github.com/ser/checkpassword-phpbb
#
# the easiest way for debugging in a command line:
# printf "%s\0%s\0%s\0" unknown bloggs Y123456 | ./checkpassword-phpbb.py id 3<&0
#
import os
import pwd
import sys
import traceback
import mysql.connector
from passlib.hash import phpass # https://pythonhosted.org/passlib/lib/passlib.hash.phpass.html

# phpBB MySQL details
config = {
  'user': '',
  'password': '',
  'host': '',
  'database': '',
  'raise_on_warnings': True,
}

def verifypass(username,password):
    # Connect to the MySQL Server
    cnx = mysql.connector.connect(**config)
    # we want to ask mysql for password for particular phpBB user, 0=normal users, 3=forum owners (1=inactive, 2=bots)
    sql = "SELECT user_password AS password FROM phpbb_users WHERE username_clean = '%s' AND user_type IN (0,3)" % username
    cursor = cnx.cursor(buffered=True)
    cursor.execute(sql)
    row = cursor.fetchone() # we need one record only
    cursor.close()
    cnx.close()
    if row is None: # no such user, it cannot be authenticated   
       return False
    phpbbppasshash = bytes.decode(row[0]) 
    return phpass.verify(password, phpbbppasshash) # True = user verified

def main():
    scriptname = os.path.basename(sys.argv[0])
    with os.fdopen(3) as infile:
        data = infile.read(512).split('\0')
    username, password = data[:2]
    justuser = username.split("@")[0]
    try:
        domain = username.split("@")[1]
    except:
        domain = "cia.gov.pl" # default domain, adapt it to your need
    if verifypass(justuser,password) == False:
       return 1 # password does not match, user cannot be authenticated
    else:
       os.environ['USER'] = "%s@%s" % (justuser, domain)
       os.environ['HOME'] = "/home/vmail/%s/%s" % (domain, justuser) # adapt it to your needs
       os.environ['userdb_uid'] = "999" # adapt it to your needs
       os.environ['userdb_gid'] = "999" # adapt it to your needs
       os.environ['userdb_mail'] = "maildir:~/Maildir" # adapt it to your needs
       #os.environ['userdb_quota_rule'] = "*:storage=100M" # adapt it to your needs and add to EXTRA environ
       os.environ['INSECURE_SETUID'] = "1"
       os.environ['EXTRA'] = 'userdb_uid userdb_gid userdb_mail'
    os.execvp(sys.argv[1], sys.argv[1:])
    # bye bye ;-)

try:
    sys.exit(main() or 111)
except KeyboardInterrupt:
    sys.exit(2)
except Exception:
    traceback.print_exc(file=sys.stderr)
    sys.exit(111)
