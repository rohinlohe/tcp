## TCP in Python: implementation notes

### How to build and run the code

The command line will accept input of the form 
```text
python TCP.py [-l] [-p {port number}] [-H {hostname}] [-v]
```

The [-l] tag is for listening. It must be used along with the [-p] tag, which takes in a specific port number. The [-H] tag is to specify a hostname (for the client). Lastly, the [-v] tag runs the programs in verbose method, which means extra debugging information is printed. 

In order to run the server, the following command can be used:
```text
python TCP.py -l -p {port number} [-v]
```

In order to run the client, the following command can be used:
```text
python TCP.py -p {port number} -H {hostname} [-v]
```
### Example Run 

<img src="clientside.png" width="75%">
<img src="serverside.png" width="75%">
