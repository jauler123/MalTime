Project Name: MalTime
Description: This python flask web application parses the analysis.log file produced by a Cuckoo Sandbox analysis, and generates a timeline of 
the events that occured during the execution of the malware. The tool has filtering capabilities that include keyword search, filtering for 
processes, filtering for dll's and exe's, filtering for file paths and finally, user interaction/activity mimicked in cuckoo.
Author: Josh Auler
Course: Advanced Malware Forensics


To run the application:

    1. Navigate to the /app directory and run sudo chmod +x install.sh to give the install script permission to execute
    
    2. Run the install.sh script as sudo to install flask dependencies using sudo ./install.sh.

    3. To run MalTime, enter "python3 app.py --logpath {path to your analysis.log file}".

    4. In a web browser, go to http://127.0.0.1:5000 and the timeline should be displayed.
