# Tutorial: How to Launch the System Step by Step

## Prerequisites
This project has been developed and tested on a Linux environment. Usage on Windows or macOS may require adjustments and some commands may not work exactly as described.


Before starting, make sure the following are installed on your system:
- **Docker**: ***https://docs.docker.com/desktop/setup/install/windows-install/***
- **Python 3.10.12**: ***https://www.python.org/downloads/***
- **Git**: ***https://git-scm.com/install/***



## Clone the Repository
Open a terminal in your selected directory and run:
```bash
git clone https://github.com/WiktorPodwin/rag-bot.git
cd rag-bot
```


## Install all dependencies
Create virtual environment:
```bash
python3 -m venv .venv
```

Now is the time for activating the virtual environment:
```bash
source .venv/bin/activate
```


Projects uses `uv` as a dependencies manager, to install this tool run:
```bash
pip install uv
```

To install all required packages, execute:
```bash
uv sync
```



## Configure Environment Variables
Create a new .env file in the project root directory.

You can use the `.env.template` file as a reference to see what variables are required and how to name them:
```bash
cp .env.template .env
```

Then, open `.env` and replace values marked with `< >` with your actual credentials or paths (from your cloud, database, etc.).



## Build and Start Docker Containers
Run the following command to build the Docker images and start all containers in the background (Docker app hast to be on before you run this command):
```bash
docker compose up -d --build
```



## Initialize Database Tables
Once the containers are running, execute the initialization script to set up the database schema:
```bash
bash ./scripts/prestart.sh 
```


## Download Model Weights
To download and store the embedding model locally:
```bash
bash ./scripts/model_setup.sh
```



## Start the Application
Launch the FastAPI application:
```bash
python src/serve.py
```



## Access the Application
Open your browser and go to ***http://127.0.0.1:8000/docs***.
You should now see the FastAPI interactive documentation (Swagger UI).
