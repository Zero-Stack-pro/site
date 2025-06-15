# ZeroStack Company Website

This is the official website for ZeroStack - an innovative technology company specializing in industrial automation and enterprise monitoring solutions.

## Features

- Modern, responsive design
- Company information and services
- Product showcase
- Contact information
- Blog section

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Technologies Used

- Django 5.0.2
- Bootstrap 5
- Crispy Forms
- Python 3.x 