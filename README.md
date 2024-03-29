# ATel Lookup

Powerful web-based search interface for intelligently querying and visualising ATel reports from [The Astronomer's Telegram](https://astronomerstelegram.org/).

**Authors:** Rohan Khayech, Ryan Martin, Nathan Sutardi, Greg Lahaye and Tully Slattery.

Developed in collaboration with Dr. Arash Bahramian and Professor James Miller-Jones at the Curtin Institute of Radio Astronomy (CIRA).

## Description
The ATel Lookup application is a powerful and comprehensive web-based search interface that allows users to intelligently query reports from The Astronomer’s Telegram by object name and location. It also displays timeline and graph visualisations that will help astronomers and the general public better understand celestial objects, events and their relationship. 

### Functionality
The ATel Lookup application allows for all ATel reports listed on The Astronomer’s Telegram to be automatically imported in the background, with key features such as celestial object names, coordinates, keywords and event observation dates parsed and extracted from the title and body text of each report. This allows for a richer search interface allowing searching for reports not only by text, keywords and submission date, but by celestial objects themselves. The object name search cross-references the SIMBAD Astronomical database, to allows users to search reports by any accepted alias used to refer to a celestial object, returning reports that contain any of these alternate names, or contain coordinates within range of the object. The object coordinate search also makes use of SIMBAD, to find all celestial objects within a certain radius and return any reports that mention these objects, alongside all reports containing coordinates within the given radius. 

The application provides a listing of ATel reports matching the search criteria, allowing the original reports to be viewed on The Astronomer’s Telegram. The application also provides rich visualisations allowing the user to make greater contextual observations about the reported events. The timeline provides a chronological visualisation of when reports were submitted, allowing astronomer’s to easily identify periods of frequent activity related to a celestial object. The network graph allows astronomers to identify clusters of related reports associated with specific celestial events. These visualisations are both interactive, allowing users to easily view an original report by simply clicking on a node.

### Project Details

The application was developed as part of a final year Capstone project at Curtin University. The development team that has worked on the project over the semester consists of three Computer Science students; Rohan Khayech, Ryan Martin and Nathan Sutardi, Software Engineering student, Greg Lahaye and Cyber Security student Tully Slattery. With the team built-up with students from multiple majors, our specialised skills were put to great use over the course of the project, covering both front and backend development, user interface and algorithmic design and security considerations.  

The project was commissioned by researcher Dr. Arash Bahramian and Director of Science, Professor James Miller-Jones at CIRA, the Curtin Institute of Radio Astronomy. CIRA consists of a multi-disciplinary team of both engineers and scientists focused on the field of radio astronomy. 

### Screenshots
<details>
    <summary>
        View Screenshots
    </summary>
<br>

![image](https://user-images.githubusercontent.com/49182055/227155074-9f3da04d-8d66-4f2f-bbbd-92e185eea8ab.png)

![image](https://user-images.githubusercontent.com/49182055/227156670-505090a3-2400-4b78-bd32-072cfdc411f6.png)
    
![image](https://user-images.githubusercontent.com/49182055/227155209-c4a20f54-44a4-4670-878c-8b21e06c47c1.png)

![image](https://user-images.githubusercontent.com/49182055/227156721-79cdd1d6-2274-42aa-a4ab-01550a3f76e1.png)

</details>


## Licence and Copyright
Copyright 2021 Rohan Khayech, Ryan Martin, Nathan Sutardi, Greg Lahaye and Tully Slattery.

ATel Lookup is licensed under the GNU Affero General Public License v3.0.
See the full licence terms [here](LICENSE).

    Copyright (C) 2021 Rohan Khayech, Ryan Martin, Nathan Sutardi, Greg Lahaye and Tully Slattery
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.
    
    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

___

## Usage Instructions
### Setup:
    1. Install Docker Desktop on the local computer.
    2. Download the source code of the latest release.
    3. Extract the .zip file into the desired folder on a local computer.

**Latest Release:** [v1.0.1](https://github.com/rohankhayech/ATel-Lookup/releases/latest)

**Docker Installation Guide:** [Windows](https://docs.docker.com/desktop/windows/install) | [Mac](https://docs.docker.com/desktop/mac/install)


### Building and starting the application:
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

### Accessing the web application:
    1. Open a browser window.
    2. Navigate to the following address in the URL bar:
        localhost
    3. This should bring up the main search page of the application.

### Adding an admin user:
    1. Open a console window in the source code folder as above
    2. Enter the following command 
        docker exec -it backend_container_1 python ./add_admin_user.py --username [USERNAME] --password [PASSWORD]
    3. The admin user has been added.

### Logging in and importing reports:
    1. On the web application, click "Admin Portal" on the navigation bar.
    2. Login with the username and password specified when adding an admin user.
    3. To import a specific ATel manually enter the ATel number and press "Import"
    4. To start a background import of all ATels currently on AT, press "Import All". 
    5. The application will be begin to automatically import all ATels. This may take up to 24hrs depending on internet connection speed.
    6. Searches may be performed in the meantime, however they may not return complete results until all ATels have finished importing.

### Stopping the application:
    1. Navigate to the console window running the docker application.
    2. Press CTRL-C (Command-C on Mac) to stop the container and the web application.
    3. Enter the following command:
        docker compose down
    4. You may now close the console window and Docker Desktop.

