# Password Hunter
Password Hunter is a comprehensive security tool designed to extract sensitive information from popular web browsers and devices.The project is aimed at cyber security students and professionals who are interested in web browser and device security.

It is important to note that using this tool on any system or device without the explicit permission of the owner is illegal and considered unethical. The creators of this tool are not responsible for any unlawful or unethical activities carried out using this program.

Therefore, by downloading and using this program, you acknowledge that you are using it for educational purposes only and will not use it for any illegal or unethical activities.

# Installation Instruction
First, install the required modules

```
pip3 install requirements.txt
```

# Usage
You can compile the source code or simply install the execuatable file.

# Download Installation file
If you don't want to compile the souce code, simply download the latest installation file: [PasswordHunter](https://github.com/PasswordHunter/passwordhunter/releases/download/v1.5/passwordhunter.v1.5.exe)

You can also use older vesions. See [releases](https://github.com/PasswordHunter/passwordhunter/releases)

# Run from souce
```
python password_hunter.py
```

# Convert it to exe to run on any windows machine
Note: To compile the codes into an executable requires knowledge of the use of pyinstaller, please read more about it before running the below code.
```
pyinstaller --onefile --icon=icon.ico --name=PasswordHunter -w password_hunter.py
```
