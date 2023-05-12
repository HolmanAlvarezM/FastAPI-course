# Introduction to FastAPI: Path, Operations, Validations and Authentification

## 1. What is FastAPI?

It´s a modern framework of high performance for the creation of APIs with Python, it's available since Python 3.6 version.

### Characteristics

- Fast
- Fewer bugs
- Easy and intuitive
- Strongest
- Based in standards

### Framewors used by FastAPI

- **Starlett:** asyncronous Framework for building services, it's one of fastest in python.
- **Pydantic:** Data valitation
- **Uvicorn:** Excecute make code with FastAPI

## 2. Instalation WSL / Windows

### **Update packages and install python**

```sh
sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip
python -m pip install --upgrade pip
```

### **Install virtual environement**

```sh
sudo apt install python3-venv
python3 -m venv venv
```

### **Create folder project and open VSCode**

```sh
mkdir <folder name>
cd <folder name>
code .
```

### **Activate / deactivate venv in WSL**

Open WSL terminal in VSCode

```sh
source venv/bin/activate
deactivate
```

### **Activate / deactivate venv in Windows**

Open WSL terminal in VSCode

```sh
.\venv\Scripts\activate
deactivate
```

### **Install FastAPI**

```sh
pip install fastapi
```

### **Install Uvicorn library**

```sh
pip install uvicorn
```

### **Execute App in local**

```sh
uvicorn main:app --reload --port 5000
```

### **Execute App view since wire**

```sh
uvicorn main:app --reload --port 5000 --host 0.0.0.0
```

### **Token implement**

```sh
pip install pyjwt
```

### **Create Requirements file**

```sh
pip3 freeze > requirements.txt
```

# Database, Modularation and production Deploy

## Install SQL Alchemy
```sh
pip install sqlalchemy
```