=== Setup Instructions ===
1. Install Docker Desktop on the local computer:
    Installation Guide (Windows): https://docs.docker.com/desktop/windows/install/
    Installation Guide (Mac): https://docs.docker.com/desktop/mac/install/
2. Extract the .zip file into the desired folder on a local computer.

=== How to Start ===
1. Start the Docker Desktop application.
2. Open the file explorer and navigate to the folder where the extracted source code is located.
3. Open a Powershell or Terminal console in this folder:
    On Windows: Shift + Right-click in the folder > Open Powershell window here...
    On Mac: Click Finder in the application bar > Services > New Terminal at Folder.
    If these options are not avaliable on your machine, you can alternatively:
        1. Open Powershell or Terminal window using search.
        2. Enter the following command (where [SOURCE CODE LOCATION] is the folder where the extracted source code is located.):
            cd [SOURCE CODE LOCATION]

4. Type the following command into the console window:
    docker compose up
5. You should see the containers starting up in the console window.
6. The web application is now running.

=== Accessing the web application ===
1. Open a browser window.
2. Navigate to the following address in the URL bar:
    localhost
3. This should bring up the main search page of the application.

=== Adding an admin user ===
1. Open a console window in the source code folder as above
2. Enter the following command 
    docker exec -it backend_container_1 python ./add_admin_user.py --username [USERNAME] --password [PASSWORD]
3. The admin user has been added.

=== Logging in and importing reports ===
1. On the web application, click "Admin Portal" on the navigation bar.
2. Login with the username and password specified when adding an admin user.
3. To import a specific ATel manually enter the ATel number and press "Import"
4. To start a background import of all ATels currently on AT, press "Import All". 
5. The application will be begin to automatically import all ATels. This may take up to 24hrs depending on internet connection speed.
6. Searches may be performed in the meantime, however they may not return complete results until all ATels have finished importing.

=== Stopping the application ===
1. Navigate to the console window running the docker application.
2. Press CTRL-C (Command-C on Mac) to stop the container and the web application.
3. Enter the following command:
    docker compose down
4. You may now close the console window and Docker Desktop.


        