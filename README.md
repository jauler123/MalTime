Project Name: MalTime
Description: This python flask web application parses the analysis.log file produced by a Cuckoo Sandbox analysis, and generates a timeline of 
the events that occured during the execution of the malware. The tool has filtering capabilities that include keyword search, filtering for 
processes, filtering for dll's and exe's, filtering for file paths and finally, user interaction/activity mimicked in cuckoo.
Author: Josh Auler
Email: jta2866@rit.edu


To run the application:

    1. Navigate to the /app directory and run the install.sh script as sudo to install flask dependencies.

    2. Navigate to the /app directory and enter "python3 app.py --logfile {path to your analysis.log file}".

    3. In a web browser, go to http://127.0.0.1:5000 and the timeline should be displayed.
