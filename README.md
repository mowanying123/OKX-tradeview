# OKX TradeView

OKX TradeView is a cryptocurrency trading management platform built on Django 5.0, integrating multiple functional modules, including user authentication, data presentation, card management, vending machine payments, etc. The core module **Cryptoforward** of the project handles functions related to cryptocurrency trading.

For Chinese readme, visit [here](https://github.com/mowanying123/OKX-tradeview/blob/main/README_CN.md)

## Project Features

The project is designed in a modular fashion according to its functions, with each module responsible for different business logic. The following are the main modules in the project:

### Core Module: `apps/cryptoforward`

The `Cryptoforward` module is the core functionality of the project, responsible for data processing and presentation related to cryptocurrency trading. Its features include:
- **Message Formatting**: Format encrypted trading data through `formatMsg.py` for analysis and presentation.
- **Transaction Data Processing**: Manage and store transaction-related data through `models.py`.
- **View Presentation**: Implement the presentation and data update of transaction-related pages through `views.py`.
- **URL Routing**: Define and handle routes related to transactions through `urls.py`.

### Other Important Modules
- **Authentication**: Provides user login, registration, password recovery, and other features.
- **Dashboards**: Present data analysis dashboards to help users intuitively understand trading data and system status.
- **Cards**: Manage card data, providing UI display in card styles.
- **VendingMachine**: Provide vending machine-related functions, including product display and payment.
- **UI & Layouts**: Provide a rich set of UI components and layout templates to enhance user experience.

## Project Dependencies

The project depends on the following main Python packages, which can be viewed in the `requirements.txt` file:

```bash
asgiref==3.7.2
Django==5.0
gunicorn==21.2.0
packaging==23.1
python-dotenv==1.0.0
sqlparse==0.4.4
typing_extensions==4.7.1
whitenoise==6.5.0
django_q==1.3.9
redis==4.5.3
```

## Environment Configuration

1. The project manages environment variables through `python-dotenv`, requiring the creation of a `.env` file and configuration of the corresponding environment variables.

   Example `.env` file:
   ```bash
   SECRET_KEY=your-secret-key
   DEBUG=True
   DJANGO_ENVIRONMENT=local
   DATABASE_NAME=OKXTradeView
   DATABASE_USER=OKXTradeView
   DATABASE_PASSWORD=your-db-password
   ```

2. Ensure that PostgreSQL database is installed locally and connection information is properly configured.

## Deployment Steps

The following are the steps for project deployment:

### 1. Clone the Project
```bash
git clone https://github.com/mowanying123/OKX-tradeview.git 
cd OKX-tradeview
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migration
Ensure that the PostgreSQL database is running and the database connection is correctly configured in `config/settings.py`. Execute the following command for database migration:
```bash
python manage.py migrate
```

### 5. Start Development Server
Run the following command to start the local development server:
```bash
python manage.py runserver
```

### 6. Deploy to Production Environment
For the production environment, it is recommended to use `gunicorn` as the WSGI server. You can start the production server with the following command:
```bash
gunicorn --config gunicorn-cfg.py config.wsgi
```

At this point, the project should be successfully launched and running.

## Task Queue Setup

The project uses `Django Q` and Redis to handle asynchronous tasks. Deploy Redis and start the task queue with the following command:
```bash
python manage.py qcluster
```

## Contribution

Issues and Pull Requests are welcome. If you have any questions or suggestions, please contact the project maintainer.