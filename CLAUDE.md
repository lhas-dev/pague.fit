# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pague.fit is a Django-based financial management and automated payment platform for small gyms, martial arts dojos, and fitness studios. The system automates payment reminders, processes PIX payments via Mercado Pago, and provides financial dashboards for gym owners.

## Core Architecture

The project follows standard Django patterns with a single `core` app containing the main business logic:

- **Models**: `Gym` (business entity) → `Plan` (membership plans) → `Student` (gym members) → `Subscription` (connects students to plans) → `Payment` (payment records)
- **Payment Flow**: Students access payment pages via unique UUID-based URLs (`/pay/<uuid>/`) to avoid exposing database IDs
- **Admin Interface**: Django admin is used for managing gyms, students, and plans (MVP approach)

## Common Development Commands

### Environment Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database Operations
```bash
# Apply migrations
python manage.py migrate

# Create new migration after model changes
python manage.py makemigrations

# Create superuser for admin access
python manage.py createsuperuser
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Access admin panel at http://127.0.0.1:8000/admin
```

## Key Implementation Details

- **Public Payment URLs**: Subscriptions use UUID `public_id` field for secure payment links
- **Date Handling**: Uses `python-dateutil` for subscription date calculations
- **Payment Status**: Three-state system (PENDING, APPROVED, REJECTED) with external payment ID tracking
- **Student Management**: Unique constraint on gym + phone_number to prevent duplicates within a gym
- **Subscription Status**: ACTIVE, OVERDUE, CANCELED with helper methods for status checking

## Environment Variables

Required environment variables (typically in `.env` file):
- `SECRET_KEY`: Django secret key
- `DEBUG`: Development mode flag
- `MERCADO_PAGO_ACCESS_TOKEN`: Payment gateway API key
- `SENDGRID_API_KEY`: Email service API key

## Future Integration Points

The codebase is prepared for:
- Webhook endpoints for payment confirmation
- Email automation for payment reminders
- Dashboard views for gym owners
- WhatsApp integration via Twilio