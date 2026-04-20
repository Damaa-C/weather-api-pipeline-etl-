# Weather API ETL Pipeline 🌦️
**Automated Data Extraction, Transformation, and Loading**

A professional, modular ETL pipeline that fetches real-time weather data from OpenWeatherMap, cleans and processes it using Python/Pandas, and persists it into a PostgreSQL database. Designed for both manual execution and scheduled orchestration via Apache Airflow.

##  Project Structure
Each file in this repository has a dedicated responsibility to ensure the code is maintainable and "DRY" (Don't Repeat Yourself).

- [extract.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/extract.py): Handles API requests and raw JSON extraction.
- [transform.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/transform.py): Cleans data and performs unit conversions (Kelvin to Celsius).
- [load.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/load.py): Manages database connections and SQL transactions.
- [pipeline.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/pipeline.py): The orchestrator used to run the full process manually.
- [airflow.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/airflow.py): The Airflow DAG configuration for scheduled automation.
- `.env`: (User Created) Secure storage for API keys and DB credentials.

## Tech Stack
- **Python 3.10+**
- **Pandas**: Data transformation and cleaning.
- **SQLAlchemy**: Database ORM and connection management.
- **Psycopg2**: PostgreSQL adapter.
- **Requests**: API communication.
- **Apache Airflow**: Workflow orchestration.

##  Configuration
Create a `.env` file in the project root with your specific credentials:

```env
# API Config
API_KEY=your_openweathermap_api_key
LAT=44.34
LON=10.99

# Database Config
DB_HOST=your-database-hostname.com
DB_PORT=5432
DB_USER=your_username
DB_NAME=your_db_name
DB_PASSWORD=your_password
```
##  Usage

### Manual Execution
To run the pipeline as a one-time script:

```bash
python pipeline.py
```
![pipeline.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/python_env%20pipeline.py%20run.png)

## Airflow Automation
Move `airflow.py` to your `Airflow /dags` directory.

Ensure environment variables are configured in your Airflow instance (via your .env file or Airflow Variables).

The DAG is pre-configured to run hourly with a single retry on failure.

## Database Schema
The pipeline targets a table named `weather_report`. If the table does not exist, SQLAlchemy will create it automatically.
Below is an overview of how data in database looks;
![weather_report](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/database%20overview.png)
