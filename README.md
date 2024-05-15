# Capitals Flask Web App

This is a Flask web application that provides information about world capitals.

## Running the app using a virtual environment

### Prerequisites

- Python 3.8 or higher
- `venv` module

### Setup

1. Clone the repository or download the zip file and extract it.

2. Navigate to the project directory:
    ```sh
    cd capitals
    ```

3. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

5. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

6. Run the Flask app:
    ```sh
    flask run --port=1111
    ```

The app will be running at `http://127.0.0.1:1111`.

## Running the app using Docker

### Prerequisites

- Docker

### Setup

1. Clone the repository or download the zip file and extract it.

2. Navigate to the project directory:
    ```sh
    cd capitals
    ```

3. Build the Docker image:
    ```sh
    docker build -t capitals-app .
    ```

4. Run the Docker container:
    ```sh
    docker run -p 1111:1111 capitals-app
    ```

The app will be running at `http://127.0.0.1:1111`.

## Project Structure

- `app.py` - The main Flask application file.
- `requirements.txt` - The list of Python packages required to run the app.
- `models.py` - The database models for the app.
- `capitals.py` - Additional script related to capitals data.
- `resources/worldcities.csv` - CSV file containing data about world cities.
- `templates/` - HTML templates for the app.

## License

This project is licensed under the MIT License.
