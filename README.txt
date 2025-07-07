ChatGPT Usage Analyzer
======================

ChatGPT Usage Analyzer is a simple, privacy-first tool to visualize your personal ChatGPT activity, including number of messages per day, token usage, and total usage over time.

It works entirely offline on your own machine. No data is uploaded or shared.

------------------------------------------------------------
What It Does
------------------------------------------------------------

- Parses your exported ChatGPT `conversations.json` file
- Displays a daily message count graph with token usage summary
- Highlights your most active and most verbose days
- Works with both ChatGPT Free and ChatGPT Plus
- Includes data from archived chats
- Requires no coding and no installation of Python

------------------------------------------------------------
How to Use
------------------------------------------------------------

1. Export your ChatGPT data  
   Visit: https://chatgpt.com/#settings/DataControls
   Click “Export data” and wait for the email.

2. Download and unzip your export  
   Inside, you'll find a file named `conversations.json`.

3. Download this analyzer  
   Either:  
   - Get the .zip version with included portable Python  
   - Or clone this repo manually

4. Move the analyzer files  
   Place the analyzer folder directly into your exported folder (the one with `conversations.json`).

5. Run the tool  
   Double-click `run-analyzer.bat`  
   A console window will appear, followed by a graph window.

------------------------------------------------------------
FAQ
------------------------------------------------------------

Q: Does this include archived conversations?  
A: Yes, archived chats are included in the exported `conversations.json`.

Q: Does this work with free accounts?  
A: Yes, both Free and Plus users can use this.

Q: Why is it a .bat file instead of an .exe?  
A: This is left as a simple .bat file to allow:
   - Easier inspection of the code
   - Better security transparency for cautious users
   - Portability and minimal system requirements

Q: What about Mac support?  
A: Currently untested on macOS. Contributions welcome!

------------------------------------------------------------
Included Files
------------------------------------------------------------

- run-analyzer.bat – Launch script
- resources/ – Contains embedded Python, required libraries, and analysis script

------------------------------------------------------------
Privacy & Security
------------------------------------------------------------

- Your data never leaves your computer
- No third-party services are used
- All code is included and readable

------------------------------------------------------------
Example Output
------------------------------------------------------------

(See included image: resources\example.png)

------------------------------------------------------------
Feedback & Contributions
------------------------------------------------------------

Pull requests, bug reports, and suggestions are welcome!  
Feel free to fork and improve.

------------------------------------------------------------
Licenses
------------------------------------------------------------

This project is licensed under the MIT License.

Bundled third-party software (e.g., Python, matplotlib) is licensed under their respective terms. License files are included where required.

------------------------------------------------------------
Contact
------------------------------------------------------------

GitHub: https://github.com/carsonruebel/chatgpt-usage-analyzer  
Personal Site: https://www.carsonruebel.com

------------------------------------------------------------
Created by Carson Ruebel
------------------------------------------------------------
