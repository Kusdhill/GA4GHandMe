# GA4GH-23andMe-Wrapper

The goal of this project is to build a GA4GH API wrapper around the 23andMe REST API. The work will result in a server
that can be started by a user. The user will be required to provide their 23andMe credentials.
The server will then use those to connect with the 23andMe REST interface. The server will
then respond to GA4GH variant API requests from that user only. There are many people who
have used 23andMe and this project will allow any GA4GH API compatible application to run on
against their 23andMe variant information.