# Control-5-2
Confidential.

## 🌎 Repository Structure
```
control-5-2/
│
├── modules/
├── .gitignore
├── venv/                       # Virtual enviroment
└── requirements.txt
└── bot1.py
└── run1.bat
```
## ✨ Details
Confidential.

## 🚀 How to run locally
1. Clone this repository:
```
git clone https://github.com/arteaga7/control-5-2.git
cd control-5-2
```
2. Set virtual environment and install dependencies.

For Windows:
```
uv venv venv
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\Activate.ps1
uv pip install --link-mode=copy -r requirements.txt
```

For Linux:
```
uv venv venv
source venv/bin/activate
uv pip install -r requirements.txt
```
3. Run "run1.bat", add the corresponding full path of the SharePoint folder.

![alt text](./img/bot1.png)
