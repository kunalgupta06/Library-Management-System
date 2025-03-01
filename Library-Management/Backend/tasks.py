# from celery import shared_task
# from flask_mail import Message
# from datetime import datetime, timedelta
# from flask import render_template
# import csv
# import os
# import logging
# from models import newuser, EBook, GrantRequest, BookRequest
# from controllers.__init__ import create_app

# def get_flask_app():
#     app = create_app()
#     mail = app.extensions.get("mail")
#     return app, mail

# @shared_task(ignore_result=False)
# def daily_user_reminders():
#     logging.info("Starting daily_user_reminders task")
#     try:
#         app, mail = get_flask_app()
#         with app.app_context():
#             now = datetime.utcnow()
#             users = newuser.query.all()
#             logging.info(f"Found {len(users)} users.")
#             for user in users:
#                 book_requests = GrantRequest.query.filter(
#                     GrantRequest.user_id == user.id, GrantRequest.is_granted == True
#                 ).all()
#                 books_due = [
#                     req
#                     for req in book_requests
#                     if req.date_returned and now <= req.date_returned <= now + timedelta(days=2)
#                 ]
#                 logging.info(f"User {user.email} has {len(books_due)} books due soon.")
#                 if books_due:
#                     send_reminder_email(user, books_due, mail)
#             logging.info("Daily user reminders task completed successfully")
#     except Exception as e:
#         logging.error(f"Error in daily_user_reminders task: {e}")

# def send_reminder_email(user, books_due, mail):
#     msg = Message("Library Reminder", recipients=[user.email])
#     msg.body = f"Dear {user.username},\n\nYou have books due for return soon:\n"
#     for book in books_due:
#         ebook = EBook.query.get(book.ebook_id)
#         msg.body += f"- {ebook.book_name}, due by {book.date_returned.strftime('%Y-%m-%d')}\n"
#     logging.info(f"Sending email to {user.email} for {len(books_due)} books due.")
#     mail.send(msg)

# @shared_task(ignore_result=False)
# def generate_monthly_report():
#     logging.info("Starting generate_monthly_report task")
#     try:
#         app, mail = get_flask_app()
#         with app.app_context():
#             now = datetime.utcnow()
#             start_time = now - timedelta(days=30)

#             ebooks = EBook.query.all()
#             feedbacks = BookRequest.query.filter(
#                 BookRequest.date_requested >= start_time
#             ).all()

#             html_report = render_template(
#                 "monthly_report.html",
#                 ebooks=ebooks,
#                 feedbacks=feedbacks,
#             )
#             msg = Message(
#                 "Monthly Library Report", recipients=["admin@example.com"]
#             )
#             msg.html = html_report
#             mail.send(msg)
#             logging.info("Monthly report task completed successfully")
#     except Exception as e:
#         logging.error(f"Error in generate_monthly_report task: {e}", exc_info=True)

# @shared_task(ignore_result=False)
# def export_book_requests_to_csv(librarian_email):
#     logging.info("Starting export_book_requests_to_csv task")
#     try:
#         app, mail = get_flask_app()
#         with app.app_context():
#             requests = BookRequest.query.all()
#             file_path = os.path.join("uploads", "book_requests.csv")

#             if not os.path.exists("uploads"):
#                 os.makedirs("uploads")

#             logging.info(f"File path for export: {file_path}")
#             with open(file_path, "w", newline="") as csvfile:
#                 fieldnames = [
#                     "ID",
#                     "User",
#                     "Book",
#                     "Date Requested",
#                     "Return Date",
#                 ]
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#                 for request in requests:
#                     ebook = EBook.query.get(request.ebook_id)
#                     writer.writerow(
#                         {
#                             "ID": request.id,
#                             "User": request.user.username,
#                             "Book": ebook.book_name,
#                             "Date Requested": request.date_requested.strftime('%Y-%m-%d'),
#                             "Return Date": request.date_returned.strftime('%Y-%m-%d') if request.date_returned else "Not returned",
#                         }
#                     )
#             logging.info("CSV writing completed successfully")

#             msg = Message("CSV Export Complete", recipients=[librarian_email])
#             msg.body = "The CSV export of book requests has been completed."
#             with open(file_path, "r") as fp:
#                 msg.attach("book_requests.csv", "text/csv", fp.read())
#             mail.send(msg)
#             logging.info("Export CSV task completed successfully")
#     except Exception as e:
#         logging.error(f"Error in export_book_requests_to_csv task: {e}", exc_info=True)
#         raise e


# from celery import Celery
# from datetime import datetime, timedelta
# from database import db
# from models import ActiveUser

# celery = Celery(__name__)

# @celery.task
# def update_inactive_users():
#     now = datetime.utcnow()
#     inactive_users = ActiveUser.query.filter(
#         ActiveUser.last_activity < now - timedelta(minutes=1),
#         ActiveUser.active == True
#     ).all()

#     for user in inactive_users:
#         user.active = False
#         db.session.commit()

# @celery.task
# def daily_reminder():
#     # Example daily reminder task
#     # Implement your reminder logic here
#     print("Sending daily reminders...")

# @celery.task
# def monthly_report():
#     # Example monthly report task
#     # Implement your monthly report logic here
#     print("Generating monthly report...")


# from celery_app import celery
# from models import ActiveUser, Admin, newuser, GrantRequest, EBook, Book
# from datetime import datetime, timedelta
# from database import db
# from flask_mail import Message
# import csv
# import os
# from io import StringIO
# from flask import render_template
# import logging

# @celery.task
# def update_inactive_users():
#     now = datetime.utcnow()
#     inactive_users = ActiveUser.query.filter(
#         ActiveUser.last_activity < now - timedelta(minutes=1),
#         ActiveUser.active == True
#     ).all()

#     for user in inactive_users:
#         user.active = False
#         db.session.commit()

# @celery.task
# def daily_user_reminders():
#     from app import app, mail
#     with app.app_context():
#         users = newuser.query.all()
#         for user in users:
#             if check_if_user_needs_reminder(user):
#                 send_reminder(user)

# def check_if_user_needs_reminder(user):
#     # Custom logic to check if a user needs a reminder
#     # E.g., user hasn't visited in a while or has an upcoming return date
#     return True

# def send_reminder(user):
#     from app import mail
#     msg = Message('Daily Reminder', recipients=[user.email])
#     msg.body = 'This is your daily reminder. Please visit or return your book.'
#     mail.send(msg)

# @celery.task
# def generate_monthly_report():
#     from app import app, mail
#     with app.app_context():
#         librarians = Admin.query.all()
#         report = create_monthly_report()
#         for librarian in librarians:
#             msg = Message('Monthly Activity Report', recipients=[librarian.adminemail])
#             msg.html = report
#             mail.send(msg)

# def create_monthly_report():
#     # Fetch relevant data
#     ebooks_issued = EBook.query.filter_by(issued=True).count()
#     return_dates_approaching = GrantRequest.query.filter(
#         GrantRequest.grant_date < datetime.utcnow() + timedelta(days=7)
#     ).count()
#     # Render the report using an HTML template
#     return render_template('monthly_report.html', ebooks_issued=ebooks_issued, return_dates_approaching=return_dates_approaching)

# @celery.task
# def export_book_requests_to_csv(librarian_email):
#     from app import app, mail
#     with app.app_context():
#         output = StringIO()
#         writer = csv.writer(output)
#         writer.writerow(['Book Name', 'Author', 'Date Issued', 'Return Date'])

#         requests = GrantRequest.query.all()
#         for request in requests:
#             writer.writerow([request.book.book_name, request.book.author, request.request_date, request.grant_date])

#         # Save the CSV to a file
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'book_requests.csv')
#         with open(file_path, 'w') as f:
#             f.write(output.getvalue())

#         # Send an email with the CSV file attached
#         msg = Message('Book Requests Export', recipients=[librarian_email])
#         with app.open_resource(file_path) as fp:
#             msg.attach('book_requests.csv', 'text/csv', fp.read())
#         mail.send(msg)

# @celery.task
# def notify_admin_of_rental_request(user_id, book_id):
#     from app import app, mail
#     with app.app_context():
#         admins = Admin.query.all()
#         for admin in admins:
#             msg = Message('New Rental Request', recipients=[admin.adminemail])
#             msg.body = f'User {user_id} wants to rent book {book_id}. Please review the request.'
#             mail.send(msg)


# from celery_app import celery
# from flask_mail import Message
# from flask import app, current_app
# from models import ActiveUser, GrantRequest, Book, EBook
# from database import db
# from datetime import datetime, timedelta
# import csv
# import os

# @celery.task
# def daily_user_reminders():
#     now = datetime.utcnow()
#     users = db.session.query(ActiveUser).filter(ActiveUser.last_activity < now - timedelta(days=1)).all()
#     for user in users:
#         if user.active:
#             # Send email/SMS/GChat message
#             msg = Message('Daily Reminder', recipients=[user.email])
#             msg.body = 'Please visit or return the book.'
#             current_app.extensions['mail'].send(msg)
#             # Implement SMS and Google Chat reminders as needed

# @celery.task
# def generate_monthly_report():
#     now = datetime.utcnow()
#     first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     report_date = first_day_of_month.strftime('%Y-%m-%d')
    
#     ebooks_issued = EBook.query.filter_by(issued=True).count()
#     return_dates = EBook.query.filter(EBook.return_date < now).count()
#     ratings_received = GrantRequest.query.filter(GrantRequest.grant_date.between(first_day_of_month, now)).count()
    
#     # Create the report
#     report_content = f'''
#     <h1>Monthly Report for {report_date}</h1>
#     <p>E-books Issued: {ebooks_issued}</p>
#     <p>Return Dates: {return_dates}</p>
#     <p>Ratings Received: {ratings_received}</p>
#     '''
    
#     msg = Message('Monthly Activity Report', recipients=['librarian@example.com'])
#     msg.html = report_content
#     current_app.extensions['mail'].send(msg)

# @celery.task
# def export_book_requests_to_csv(librarian_email):
#     requests = GrantRequest.query.all()
#     filename = f'book_requests_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.csv'
#     filepath = os.path.join('exports', filename)
    
#     os.makedirs('exports', exist_ok=True)
    
#     with open(filepath, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['ID', 'User ID', 'Book ID', 'Status', 'Request Date', 'Grant Date'])
#         for req in requests:
#             writer.writerow([
#                 req.id,
#                 req.user_id,
#                 req.book_id,
#                 req.status,
#                 req.request_date,
#                 req.grant_date
#             ])
    
#     # Send CSV file via email
#     msg = Message('Book Requests CSV Export', recipients=[librarian_email])
#     msg.body = 'Please find the attached CSV file for book requests.'
#     with app.open_resource(filepath) as fp:
#         msg.attach(filename, 'text/csv', fp.read())
#     current_app.extensions['mail'].send(msg)
    
#     os.remove(filepath)


from io import StringIO
from celery import shared_task
from celery_app import Celery
from flask_mail import Mail
from flask_mail import Message
from flask import app, current_app
from models import ActiveUser, Book, GrantRequest, EBook
from database import db
from datetime import datetime, timedelta
import csv
import os

@Celery.task
def daily_user_reminders():
    now = datetime.utcnow()
    users = db.session.query(ActiveUser).filter(ActiveUser.last_activity < now - timedelta(days=1)).all()
    for user in users:
        if user.active:
            # Send email
            msg = Message('Daily Reminder', recipients=[user.email])
            msg.body = 'Please visit or return the book.'
            try:
                current_app.extensions['mail'].send(msg)
            except Exception as e:
                print(f'Error sending reminder to {user.email}: {e}')
            # Implement SMS and Google Chat reminders as needed

# @Celery.task
# def generate_monthly_report():
#     now = datetime.utcnow()
#     first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     report_date = first_day_of_month.strftime('%Y-%m-%d')
    
#     ebooks_issued = EBook.query.filter_by(issued=True).count()
#     return_dates = EBook.query.filter(EBook.return_date < now).count()
#     ratings_received = GrantRequest.query.filter(GrantRequest.grant_date.between(first_day_of_month, now)).count()
    
#     # Create the report
#     report_content = f'''
#     <h1>Monthly Report for {report_date}</h1>
#     <p>E-books Issued: {ebooks_issued}</p>
#     <p>Return Dates: {return_dates}</p>
#     <p>Ratings Received: {ratings_received}</p>
#     '''
    
#     msg = Message('Monthly Activity Report', recipients=['kunalg2022@gmail.com'])
#     msg.html = report_content
#     try:
#         current_app.extensions['mail'].send(msg)
#     except Exception as e:
#         print(f'Error sending monthly report: {e}')

# @Celery.task
# def export_book_requests_to_csv(librarian_email):
#     requests = GrantRequest.query.all()
#     filename = f'book_requests_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.csv'
#     filepath = os.path.join('exports', filename)
    
#     os.makedirs('exports', exist_ok=True)
    
#     with open(filepath, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['ID', 'User ID', 'Book ID', 'Status', 'Request Date', 'Grant Date'])
#         for req in requests:
#             writer.writerow([
#                 req.id,
#                 req.user_id,
#                 req.book_id,
#                 req.status,
#                 req.request_date,
#                 req.grant_date
#             ])
    
#     # Send CSV file via email
#     msg = Message('Book Requests CSV Export', recipients=[librarian_email])
#     msg.body = 'Please find the attached CSV file for book requests.'
#     with open(filepath, 'rb') as fp:
#         msg.attach(filename, 'text/csv', fp.read())
#     try:
#         current_app.extensions['mail'].send(msg)
#     except Exception as e:
#         print(f'Error sending CSV export: {e}')
    
#     os.remove(filepath)

@shared_task
def send_monthly_activity_report():
    # Generate report content
    report_date = datetime.utcnow().strftime('%Y-%m-%d')
    users = ActiveUser.query.all()
    grants = GrantRequest.query.filter(GrantRequest.grant_date >= datetime.utcnow().replace(day=1)).all()
    books = Book.query.all()
    
    report_content = f"<h1>Monthly Activity Report for {report_date}</h1>"
    report_content += "<h2>Active Users</h2><ul>"
    for user in users:
        report_content += f"<li>{user.username} (Last Activity: {user.last_activity})</li>"
    report_content += "</ul>"
    
    report_content += "<h2>Grant Requests</h2><ul>"
    for grant in grants:
        report_content += f"<li>Book ID: {grant.book_id}, User ID: {grant.user_id}, Status: {grant.status}, Date: {grant.grant_date}</li>"
    report_content += "</ul>"
    
    report_content += "<h2>Books</h2><ul>"
    for book in books:
        report_content += f"<li>{book.book_name} by {book.author}</li>"
    report_content += "</ul>"
    from flask_mail import Mail
    mail = Mail(app)
    # Send the email
    msg = Message(subject='Monthly Activity Report',
                  recipients=['librarian@example.com'],  # Replace with actual recipient
                  html=report_content)
    
    with app.app_context():
        mail.send(msg)


@shared_task
def export_as_csv():
    # Create CSV content
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Book Name', 'Author', 'Date Issued', 'Return Date'])
    
    grants = GrantRequest.query.all()
    for grant in grants:
        book = Book.query.get(grant.book_id)
        writer.writerow([book.book_name, book.author, grant.request_date, grant.grant_date])
    
    output.seek(0)
    
    # Send CSV as an email attachment
    msg = Message(subject='Exported E-Book Data',
                  recipients=['librarian@example.com'],  # Replace with actual recipient
                  body='Attached is the CSV file containing the exported e-book data.')
    msg.attach('exported_ebooks.csv', 'text/csv', output.read())
    from flask_mail import Mail
    mail = Mail(app)
    with app.app_context():
        mail.send(msg)