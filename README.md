# Pague.fit

A financial management and automated payment platform designed for small gyms, martial arts dojos, and fitness studios. This project was built as a portfolio piece to demonstrate full-stack development skills using the Django framework.

## The Problem

Owners of small fitness studios often manage everything by themselves, from teaching classes to handling finances. A major recurring pain point is managing monthly membership payments:

- **High Communication Overhead:** Manually reminding every student that their payment is due is time-consuming and repetitive.
- **Complex Payment Process:** Students lack a simple, modern way to pay, often relying on in-person cash payments or direct bank transfers, which are hard to track.
- **Lack of Financial Visibility:** Owners struggle to get a clear, real-time overview of their monthly revenue, active members, and overdue payments.
- **No Self-Service for Students:** Students have no easy way to check their payment history or manage their subscription.

## The Solution

**Pague.fit** is a web platform that automates the entire payment lifecycle for these small businesses. It allows academy owners to:

- **Register** their academy and define membership plans.
- **Manage** their student roster with ease.
- **Automate** payment reminders via email for upcoming and overdue fees.
- **Offer** a simple and secure payment method for students (starting with PIX, Brazil's instant payment system).
- **Gain** a clear overview of their financial health through a simple dashboard.

## Key Features (MVP)

- **Academy Management:** Owners can register their academy and manage their core information.
- **Student & Plan Management:** Simple interface (via Django Admin for the MVP) to add/edit students and membership plans.
- **Secure Payment Links:** Each student subscription has a unique, public URL for payment, requiring no login from the student.
- **PIX Payment Integration:** Seamless integration with the Mercado Pago API to generate and process PIX payments.
- **Automated Confirmation:** A webhook endpoint listens for payment confirmations from Mercado Pago, automatically updating the system and renewing the student's subscription period.
- **Scheduled Reminders:** A daily cron job sends automated email reminders to students whose payments are approaching or are overdue.
- **Financial Dashboard:** A private dashboard for the owner showing key metrics like monthly revenue, active members, and overdue accounts.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (development), PostgreSQL (production-ready)
  \-- **Frontend:** Tailwind.css
- **Payments API:** Mercado Pago
- **Email API:** SendGrid
- **Deployment:** Render / Heroku
- **Development:** Git, GitHub, `pyenv`, Virtual Environments

## Screenshots

_(Here you should add screenshots of your application. This is extremely important for a portfolio project\!)_

**Owner's Dashboard**

**Student's Payment Page**

## Getting Started / Local Setup

To run this project locally, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/pague.fit.git
    cd pague.fit
    ```

2.  **Setup the Python environment:**
    (Recommended) Use `pyenv` and a virtual environment.

    ```bash
    # Set the correct python version for the project
    pyenv local 3.12.4

    # Create and activate the virtual environment
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    _(First, make sure to generate the requirements.txt file with `pip freeze > requirements.txt`)_

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the project root. Copy the contents of `.env.example` (if you created one) or add the following variables:

    ```
    SECRET_KEY='your-django-secret-key'
    DEBUG=True
    MERCADO_PAGO_ACCESS_TOKEN='your-mp-access-token'
    SENDGRID_API_KEY='your-sendgrid-api-key'
    ```

5.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser to access the admin panel:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000`. The admin panel is at `http://127.0.0.1:8000/admin`.

## Future Improvements

- [ ] Implement a self-service onboarding flow for new academies.
- [ ] Add a dedicated portal for students to view payment history and manage their plan.
- [ ] Integrate WhatsApp notifications via the Twilio API.
- [ ] Add recurring credit card payments.
- [ ] Enhance the dashboard with charts and more detailed analytics.

## Author

**[Luiz Henrique Almeida da Silva]**

- [LinkedIn](https://www.linkedin.com/in/luizhrqas/)
- [GitHub](https://github.com/lhas-dev)

## License

This project is licensed under the MIT License.
