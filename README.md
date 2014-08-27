checkpassword-phpbb
===================

DJB-compatible checkpassword for phpBB MySQL user database, used for Dovecot IMAP

The interface is specified in http://cr.yp.to/checkpwd/interface.html 

Dovecot related manual: http://wiki2.dovecot.org/AuthDatabase/CheckPassword

Debugging IMAP server:

    $ python3
    >>> import imaplib
    >>> mail = imaplib.IMAP4_SSL('imap.server.com')
    >>> mail.login('fiutek@gov.pl', 'password')

and check /var/log/mail.log on the server side.

Author
======

Serge Victor 2014, https://random.re/ 

License
=======

LGPLv3
