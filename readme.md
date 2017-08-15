
Introduction
=======================

Welcome to the project. This is a cross platform machine statistics logging system.

Installation and Configuration
-------------

1. Install dependencies using pip. Dependencies are stored in *requirements.txt*.

    `pip install -r requirements.txt`

2. Initiate the database schema using *models.py*.

    `python models.py`

3. A sample *config.xml* is given for configuration. Edit it or add yours. Make sue to use the same template
   for saving client configurations.

4. Edit *settings.py* file to configure SMTP host, sender email and path to xml file (default is current config.xml)

4. While executing server_main.py.


*Your scripts are ready to use.

For running

    `python server_main.py`


Testing
====================

1. For unit testing 

	`pytest unit`
2. For integration testing

	`pytest integration`


Assumptions
-------------

1. Client configurations are to be in *config.xml*. A sample data is in the source code. The same template
   should be followed.

2. All communication between server and client is maintained through ssh tunneling using python paramiko
   library. The library take cares of the data communicated is encrypted before transmission.

3. The email alert are executed once after a run of the server script assuming, since the current log is taken
   at the same time.

4. The server script executes client script through ssh tunnel and read from the stdout stream of the client script.
   The client script read system info and parse it in json form to stdout.

5. For retrieving system information, I tried my best to make it cross platform. But to achieve this, It is
   required that the client user have sudo permission to install any python package using *pip*. Since server script
   also send package requirement file to client and try to install all dependencies required.

6. For storing the data, I have used sqlite and sqlalchemy package for orm to make db schema more readable.

