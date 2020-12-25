## The TO-DO-list application using the FLASK framework

### Explanations:

A TO-DO application designed by the FLASK framework, enables people to save their schedules and tasks and view them in future. It, also, reminds people of the tasks ahead.

- - - -

### Key features:

- Users can add, delete and see their TO-DOs.
- Ability to register new users.
- Protection of users’ information and privacy.
- All the TO-DOs are private. Users cannot see other users’ TO-DOs.
- Using the application as a web application and REST API.
- Ability to employ other platforms due to having the capability of JSON output.
- Ability to create TO-DOs in both **basic** and **advanced** modes :

<br>

#### Basic creation of TO-DO:
Users can easily and as fast as possible register their TO-DOs, which merely include title and content.


#### Advanced creation of TO-DO:
Users can also create their TO-DOs in the more detailed and advanced mode.

1. Record date and time of registration

2. Determine the color of TO-DOs based on their taste

3. Set a reminder time

- - - -

### What is Flask?
Flask is a framework for Python to develop web applications. It is non-opinionated, that is, it does not make decisions for you. It provides greater flexibility and control for developers using it. Flask provides you with the base tools to create a web app, and it can be easily extended to include most features which you would need to include in your app.

- - - -

### What is REST?
REST, or REpresentational State Transfer, is an architectural style for building web services and APIs. It requires the systems implementing REST to be stateless. The client sends a request to the server to retrieve or modify resources without knowing what state the server is in. The servers send the response to the client without needing to know what the previous communication with the client was.
Request and Responses can be utilized in various formats. Here, JSON format is intended.

- - - -
### What is JSON?
JSON (JavaScript Object Notation) is a light-weight data-interchange format. It is easy for humans to read and write. It is easy for machines to parse and generate.

#### JSON is built on two structures:
- A collection of name/value pairs; In various languages, this is realized as an object, record, struct, dictionary, hash table, keyed list, or associative array.
- An ordered list of values; In most languages, this is realized as an array, vector, list, or sequence.

### Why using JSON?
Since the JSON format is text only, it can easily be sent to and from a server, and used as a data format by any programming language.
- - - -
### Why using REST?
Enjoying REST capability, this program allows users to easily extend and connect it to other platforms. For instance, they can design an application on Android and IOS platforms that send and receive the required information in JSON format through connecting to a web server.
- - - -
### About UI:
The user interface of this program/application is fully responsive using the bootstrap framework. In some parts, it has become simpler and more attractive using the Jquery library.
- - - -
### Requirements:
+ Python 3
+ Sqlite 3
+ Flask
