# GA4GH-23andMe-Wrapper

The goal of this project is to build a GA4GH API wrapper around the 23andMe REST API. The work will result in a server
that can be started by a user. The user will be required to provide their 23andMe credentials.
The server will then use those to connect with the 23andMe REST interface. The server will
then respond to GA4GH variant API requests from that user only. There are many people who
have used 23andMe and this project will allow any GA4GH API compatible application to run
against their 23andMe variant information.

# Usage

To begin, you should clone this repository. If you don't know how to do that, you can just download the code to your Desktop.

Before opening any of the files you will have to <a href="https://api.23andme.com/dev/">register</a> an API client with 23andMe. You can use the same parameters in the image below:
![alt text](https://github.com/Kusdhill/GA4GHandMe/blob/master/templates/registration.png "client_registration")

Once you have done this, 23andMe will give you two credentials: a client id, and a client secret. Put both of these in keys.py, along with a sessions key for flask. The sessions key can be anything.

Once that's setup, make a <a href="http://docs.python-guide.org/en/latest/dev/virtualenvs/">virtual environment</a>. 

If you don't have virtual environment already
```
pip install virtualenv
```

Once you have that you can make a virtual environment

```
virtualenv env_name
```

And then start the virtual environment
```
source env_name/bin/activate
```

With the virual environment running, go ahead and install the requirements.txt.

You should also make sure you have the GA4GH server <a href="http://ga4gh-reference-implementation.readthedocs.io/en/latest/demo.html">setup</a>.


```
pip install --upgrade -r requirements.txt
pip install ga4gh-server
```

After this is all complete, you can start up the server.

```
python server.py
```

Once that's up and running you can navigate to localhost:5000 in your web browser. The only thing you need to do from here is follow the prompts. Enjoy!

---
This project was made possible thanks to 23andMe's <a href="https://github.com/23andMe/api-example-flask">python oauth/flask example</a>, w3school's <a href="https://www.w3schools.com/html/html_tables.asp">sample data table</a>, and the help of <a href="https://github.com/kozbo">Kevin Osborn</a> and <a href="https://github.com/david4096">David Steinberg</a>.