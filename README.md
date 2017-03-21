# GA4GH-23andMe-Wrapper

The goal of this project is to build a GA4GH API wrapper around the 23andMe REST API. The work will result in a server
that can be started by a user. The user will be required to provide their 23andMe credentials.
The server will then use those to connect with the 23andMe REST interface. The server will
then respond to GA4GH variant API requests from that user only. There are many people who
have used 23andMe and this project will allow any GA4GH API compatible application to run
against their 23andMe variant information.

# Usage

To begin, make sure you have the GA4GH client <a href="http://ga4gh-reference-implementation.readthedocs.io/en/latest/demo.html">setup</a>.

You will also need to make a <a href="http://docs.python-guide.org/en/latest/dev/virtualenvs/">virtual environment</a>. With the virual environment running, go ahead and install the requirements.

```
pip install requirements.txt
```

After this is all complete, you can start up the server using

```
python server.py
```

and navigate to localhost:5000.