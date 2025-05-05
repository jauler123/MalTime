Project Name: MalTime
Description: This python flask web application parses the analysis.log file produced by a Cuckoo Sandbox analysis, and generates a timeline of 
the events that occured during the execution of the malware. The tool has filtering capabilities that include keyword search, filtering for 
processes, filtering for dll's and exe's, filtering for file paths and finally, user interaction/activity mimicked in Cuckoo.
Author: Josh Auler
Course: Advanced Malware Forensics


To run the application:

    1. Clone the repository using git or download the zip and unpack it.

    2. Navigate to the /app directory and run sudo chmod +x install.sh to give the install script permission to execute.
    
    3. Run the install.sh script as sudo to install flask dependencies using sudo ./install.sh.

    4. To run MalTime, enter "python3 app.py --logpath {path to your analysis.log file}".

    5. In a web browser, go to http://127.0.0.1:5000 and the timeline should be displayed.



Sample Run of the Application

Step 1

![image](https://github.com/user-attachments/assets/43826b60-1052-45e7-82fb-329179186f59)

Step 2

![image](https://github.com/user-attachments/assets/7a8809d6-3f2b-4ffc-8115-21d374ce447d)

Step 3: Output shortened

![image](https://github.com/user-attachments/assets/22da9e55-ac1a-413e-817e-5ada2f4ea329)

![image](https://github.com/user-attachments/assets/8b1a8824-b8cb-4c23-a956-2e42b4b77778)

Step 4

![image](https://github.com/user-attachments/assets/b4d036b4-4c29-43fa-a1e9-ca2fc74f5ef5)

Step 5

![image](https://github.com/user-attachments/assets/054f7681-0bec-4ea0-a924-1ee355562f10)

