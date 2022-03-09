# sisu_gmail - abstractions of the Gmail API

Running the tests:

1) If this is your first test, make an **unused gmail address**

2) Make sure to delete any welcome emails, etc

3) git clone https://github.com/loren-magnuson/sisu_gmail && cd sisu_gmail
 
5) Put your Gmail API enabled credentials JSON in credentials.json

6) python -m unittest

7) The Gmail API auth flow should start, complete it.

8) Your token will be saved as token.json in the sisu_gmail directory.

9) Tests should now attempt to complete using your creds.

10) Before your next test run, delete any left over emails