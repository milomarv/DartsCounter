# 🎯 Dart Counter Web Application

## Overview
This Dart Counter is a web server application designed to facilitate playing the classic game of darts, commonly known as 501. However, users can also configure the game to play with other point values. The application allows customization of the number of legs and sets, as well as the option to play in modes such as Best of or First to.

## Features

### 1. Configure Game
Users can set up the game according to their preferences, including choosing the point value for each game (e.g., 501), specifying the number of legs and sets, and selecting the mode (Best of or First to).

### 2. Type in Scores
The application provides a dedicated Typer Page where users can conveniently input their scores during gameplay.

### 3. Scoreboard
Scores entered by the users are instantly reflected on the Scoreboard page. Here, players can view the current points, along with other relevant statistics. Additionally, the scoreboard page offers graphical representations of the game progress for each player.

## Prerequisites

Before getting started, ensure that the following prerequisites are met:

1. **Python**: Make sure you have Python installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

2. **Git**: Git is used for version control. If you haven't already, download and install Git from the [official website](https://git-scm.com/downloads).

## Installation
1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/your-username/DartsCounter.git
    ```
2. Navigate to the project directory:
    ```bash
    cd DartsCounter
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Updating
If there are updates available for the Dart Counter application, you can pull the latest changes from the repository:
```bash
git pull origin main
```

## Run the Application
1. Activate the virtual environment (if not already activated):
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

2. Run the application:
    - On Windows (using Waitress):
        ```bash
        waitress-serve --listen=*:8050 app:server
        ```
    - On macOS and Linux (using Gunicorn):
        ```bash
        gunicorn --listen=*:8050 app:server
        ```
    
## Make the Application Publicly Available

1. If you haven't already, start the application as instructed in the previous section.

2. Open a new terminal window or command prompt.

3. Navigate to the directory where ngrok.exe is located.

4. Run the following command to expose your local server to the internet:
    ```bash
    .\ngrok.exe http http://localhost:8050  
    ```

5. Ngrok will generate a forwarding URL (e.g., `http://abcd1234.ngrok.io`) that you can share with others to access your application.

6. **Warning**: Exercise caution when using ngrok to expose your local server. Sharing the generated URL indiscriminately can provide direct access to your local machine, potentially posing security risks.

7. Share the generated URL with anyone you want to give access to your application.

## Technologies Used
- Python
- Dash (Python web framework for building analytical web applications)
- Plotly (Python graphing library for interactive visualizations)