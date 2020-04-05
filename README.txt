--------------------------------------- Team Details ------------------------------------------

* Siddu Madhure Jayanna - 200263301
* Shraddha Bhadauria    - 200261564 


-------------------------------------- Code Files Used ----------------------------------------

* server.py - server implementation
* client.py - client implementation 
* helper.py - client's helper functions 


--------------------------------- Implementation Details --------------------------------------

* Implemented using python3
* Server port is set to **7734** inside the main function of server.py
* Inside the main function of client.py, the server port is set to **7734**, server host is set to **192.168.33.1** and upload port is set to **5555**
* Every new client/peer should use some available port as their upload port and this should be updated in its client.py script before running it
* The server details inside the main function of client.py should also be updated based on server's config details
* Peer RFCs are stored in a folder called **RFC_Store** with client.py file inside the client folder
* RFC text file naming format: RFC file name will be the title of the RFC with its number. For Example, RFC35.txt -> here RFC35 is the RFC title and 35 is RFC number


--------------------------------- Steps To Run The System --------------------------------------

* Install python3
* Change the directory to the root folder of the project
* server - Start the server by running **python script.py** command
* Client part is stored in **client** folder and it has 2 RFC files inside RFC_Store folder
* To run multiple clients - Make multiple copies of the client folder and update client's upload port to a new port (inside client.py file). Also, update the RFC_store folder with new client's RFC files
* Client - cd into client folder and run **python client.py** command
* Now you can test and analyze different functionalities using client and server's menu options and logs
