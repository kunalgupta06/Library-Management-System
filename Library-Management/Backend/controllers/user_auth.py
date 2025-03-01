import datetime
from flask import app, current_app, jsonify, make_response, request, session, url_for
from threading import Thread
from flask import Blueprint, jsonify
from flask_caching import Cache
from tasks import export_as_csv
# from . import cache
# print(f"Cache used in user_auth.py: {cache}")

from flask_mail import Mail, Message
from models import ActiveUser, Admin, EBook, GrantRequest, newuser, user, Book
from database import db
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime, time, timedelta
from datetime import datetime, timedelta
from tasks import  daily_user_reminders,export_as_csv
import logging

#from tasks import daily_user_reminders, generate_monthly_report, export_book_requests_to_csv
from celery_app import Celery


class Register(Resource):
    def post(self):
        data = request.get_json()
        print(data)  # Print received data for debugging

        if 'email' not in data or 'username' not in data or 'password' not in data or 'confirmpassword' not in data:
            return {'message': 'Missing required fields.'}, 400

        existing_user = newuser.query.filter((newuser.email == data['email']) | (newuser.username == data['username'])).first()
        if existing_user:
            return {'message': 'User Already Exists! Please use a different email or username.'}, 400

        if data["password"] != data["confirmpassword"]:
            return {'message': 'Password and confirm password do not match.'}, 400

        hashed_password = generate_password_hash(data["password"])
        new_user = newuser(
            name=data['name'],
            email=data['email'],
            phonenumber=data['phonenumber'],
            username=data['username'],
            password=hashed_password,
            confirmpassword=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        
        user_login_instance = user(
            username=data['username'],
            userpassword=hashed_password,
            useremail=data['email']
        )
        
        db.session.add(user_login_instance)
        db.session.commit()

        active_user = ActiveUser(
            username=data['username']
            
        )
        db.session.add(active_user)
        db.session.commit()


        # activeuser= ActiveUser(
        #     username=data['username'],
        #     active="True"
        # )
        # db.session.add(activeuser)
        # db.session.commit()

        return {'message': 'User registered successfully!'}, 201


class Login(Resource):
    def post(self):
        data = request.get_json()

        if 'usernameOrEmail' not in data or 'password' not in data or 'role' not in data:
            return {'message': 'Missing required fields.'}, 400

        role = data.get('role')

        try:
            if role == 'admin':
                admin_user = Admin.query.filter((Admin.adminemail == data['usernameOrEmail']) | (Admin.adminname == data['usernameOrEmail'])).first()
                if not admin_user or not (admin_user.password, data['password']):
                    return {'message': 'Invalid credentials. Please check and try again.'}, 401
                session['user'] = {'username': admin_user.adminname, 'role': 'admin'}
                return {'message': 'Welcome Admin!', 'user': {'id': admin_user.id,'username': admin_user.adminname, 'role': 'admin'}}, 200
            else:
                user_instance = newuser.query.filter((newuser.email == data['usernameOrEmail']) | (newuser.username == data['usernameOrEmail'])).first()
                if not user_instance or not check_password_hash(user_instance.password, data['password']):
                    return {'message': 'Invalid credentials. Please check and try again.'}, 401
                session['user'] = {'username': user_instance.username, 'role': 'user'}
                return {'message': 'Welcome User!', 'user': {'id': user_instance.id,'username': user_instance.username, 'role': 'user'}}, 200
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            return {'message': 'An unexpected error occurred. Please try again later.'}, 500
        
class UpdateActivity(Resource):
    def post(self):
        username = request.json.get('username')
        active_user = ActiveUser.query.filter_by(username=username).first()
        if active_user:
            active_user.last_activity = datetime.utcnow()
            db.session.commit()
        return jsonify({"message": "Activity updated"})

@Celery.task
def update_inactive_users():
    now = datetime.utcnow()
    inactive_users = ActiveUser.query.filter(
        ActiveUser.last_activity < now - timedelta(minutes=1),
        ActiveUser.active == True
    ).all()

    for user in inactive_users:
        user.active = False
        db.session.commit()

class stats(Resource):
    def get(self):
        active_users = ActiveUser.query.filter_by(active=True).count()
        grant_requests = GrantRequest.query.count()
        ebooks_issued = GrantRequest.query.filter_by(status='Approved').count()
       


        stats = {
            'active_users': active_users,
            'grant_requests': grant_requests,
            'ebooks_issued': ebooks_issued,
            
        }
        return jsonify(stats)




UPLOAD_FOLDER = 'D:\Mad 2 Library\Library-Management\Backend\controllers\static'

class add_book(Resource):
    def post(self):
        print("Form Data:", request.form)
        print("Files:", request.files)

        # Check for necessary form data
        if 'bookName' not in request.form or 'bookPhoto' not in request.files or 'bookPDF' not in request.files:
            return jsonify({"error": "Missing form data or file"}), 400

        book_name = request.form['bookName']
        author = request.form['author']
        date_of_publish = request.form['dateOfPublish']
        price = request.form['price']
        genre = request.form['genre']

        # Handle the book photo
        book_image = request.files['bookPhoto']
        if book_image and book_image.filename:
            image_extension = '.' + book_image.filename.split('.')[-1]
            image_filename = secure_filename(book_name) + image_extension
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            try:
                # Ensure the directory exists
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                
                book_image.save(image_path)
            except Exception as e:
                print("Error saving file:", e)
                return jsonify({"error": "Error saving file"}), 500
        else:
            image_filename = None


        book_pdf = request.files['bookPDF']
        if book_pdf and book_pdf.filename:
            pdf_extension = '.' + book_pdf.filename.split('.')[-1]
            pdf_filename = secure_filename(book_name) + "_pdf" + pdf_extension
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
            try:
                # Ensure the directory exists
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                
                book_pdf.save(pdf_path)
            except Exception as e:
                print("Error saving file:", e)
                return jsonify({"error": "Error saving file"}), 500
        else:
            pdf_filename = None

        # Validate and process date
        try:
            date_of_publish = datetime.strptime(date_of_publish, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

        # Save book to database (assumes a SQLAlchemy setup)
        try:
            new_book = Book(
                book_name=book_name,
                author=author,
                date_of_publish=date_of_publish,
                price=price,
                image_filename=image_filename,
                pdf_filename=pdf_filename,
                genre=genre,
            )
            db.session.add(new_book)
            db.session.commit()
        except Exception as e:
            print("Database Error:", e)
            return jsonify({"error": "Database error"}), 500

        return jsonify({"message": "Book added successfully"}), 200

class libBook(Resource):
    def get(self):
        # Fetch all books from the database
        books = Book.query.all()
        
        # Generate the list of books with the correct fields
        books_list = [
            {
                "id": book.id,
                "book_name": book.book_name,
                "author": book.author,
                "date_of_publish": book.date_of_publish.strftime('%Y-%m-%d'),
                "price": book.price,
                "photo_path": url_for('static', filename=f'{book.image_filename}', _external=True),
                "pdf_path": url_for('static', filename=f'{book.pdf_filename}', _external=True) if book.pdf_filename else None,
                "genre": book.genre
            }
            for book in books
        ]
        return jsonify(books_list)
    

class members(Resource):
    def get(self):
        users = user.query.all()
        active_users = ActiveUser.query.all()
        active_dict = {user.username: user.active for user in active_users}

        users_list = [{'id': user.id, 'name': user.username, 'username': user.username, 'active': active_dict.get(user.username, False)} for user in users]
        return jsonify(users_list)
    

class updatebook(Resource):
    def put(self, book_id):
        try:
            book = Book.query.get(book_id)
            if not book:
                return make_response(jsonify({"error": "Book not found"}), 404)

            # Update book details
            book.book_name = request.form.get('bookName')
            book.author = request.form.get('author')
            book.date_of_publish = datetime.strptime(request.form.get('dateOfPublish'), '%Y-%m-%d')
            book.price = request.form.get('price')
            book.genre = request.form.get('genre')

            # Update book photo if provided
            if 'bookPhoto' in request.files:
                book_image = request.files['bookPhoto']
                if book_image and book_image.filename:
                    image_extension = '.' + book_image.filename.split('.')[-1]
                    image_filename = secure_filename(book.book_name) + image_extension
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    try:
                        if not os.path.exists(app.config['UPLOAD_FOLDER']):
                            os.makedirs(app.config['UPLOAD_FOLDER'])
                        book_image.save(image_path)
                        book.image_filename = image_filename
                    except Exception as e:
                        return make_response(jsonify({"error": "Error saving file", "details": str(e)}), 500)

            # Commit changes to the database
            db.session.commit()
            return make_response(jsonify({"message": "Book updated successfully"}), 200)
        
        except Exception as e:
            return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)


class delete_book(Resource):
    def delete(self,book_id):
        print(f"Attempting to delete book with ID: {book_id}")
        book = Book.query.get(book_id)
        if not book:
            return {"message": "Book not found"}, 404

        try:
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book deleted successfully"}, 200
        except Exception as e:
            print(f"Error deleting book: {e}")
            return {"message": "Database error"}, 500

class DailyReminder(Resource):
    def post(self):
        task = daily_user_reminders.apply_async()
        return jsonify({"task_id": task.id}), 202


    

class RentBook(Resource):
    def post(self):
        try:
            data = request.get_json()
            print(f"Incoming request data: {data}")

            book_id = data.get('book_id')
            user_id = data.get('user_id')

            # Debugging statements to verify data extraction
            print(f"Extracted book_id: {book_id}, user_id: {user_id}")

            if not book_id or not user_id:
                print("Missing book_id or user_id in the request")
                return {'error': 'Invalid data'}, 400

            # Fetch the book and user from the database
            book = Book.query.get(book_id)
            user_instance = user.query.get(user_id)

            # Debugging statements to verify database queries
            print(f"Fetched book: {book}, Fetched user: {user_instance}")

            if not book or not user_instance:
                print("Book or User not found")
                return {'error': 'Book or User not found'}, 404

            if book.is_rented:
                print("Book is already rented")
                return {'error': 'Book is already rented'}, 400

            # Create a new grant request
            grant_request = GrantRequest(
                user_id=user_id,
                book_id=book_id,
                status='Pending'
            )
            db.session.add(grant_request)
            db.session.commit()

            response = {'message': 'Rental request submitted successfully, awaiting admin approval.'}
            print("Grant request successfully created and committed to the database")
            return response, 200

        except Exception as e:
            # Detailed error logging
            print(f"An error occurred: {e}", exc_info=True)
            return {'error': 'An error occurred while processing your request.'}, 500

class AdminApproveRequest(Resource):
    def post(self):
        try:
            data = request.get_json()
            request_id = data.get('requestId')
            action = data.get('action')  # 'approve' or 'reject'

            if not request_id or action not in ['approve', 'reject']:
                return {'error': 'Invalid data'}, 400

            grant_request = GrantRequest.query.get(request_id)

            if not grant_request:
                return {'error': 'Request not found'}, 404

            if action == 'approve':
                grant_request.status = 'Approved'
                grant_request.grant_date = datetime.utcnow()
                book = Book.query.get(grant_request.book_id)
                if book:
                    book.is_rented = True
                    db.session.add(book)
            else:
                grant_request.status = 'Rejected'

            db.session.commit()
            return {'message': 'Request processed successfully.'}, 200

        except Exception as e:
            print(f"An error occurred: {e}")  # Debugging
            return {'error': 'An error occurred while processing the request.'}, 500
        
class ReturnBook(Resource):
    def post(self):
        try:
            data = request.get_json()
            book_id = data.get('book_id')
            user_id = data.get('user_id')

            grant_request = GrantRequest.query.filter_by(book_id=book_id, user_id=user_id, status='Approved').first()

            if grant_request:
                db.session.delete(grant_request)
                db.session.commit()

                # Reset the book's is_rented status
                book = Book.query.get(book_id)
                if book:
                    book.is_rented = False
                    db.session.commit()

                return jsonify({'message': 'Book returned successfully.'}), 200
            else:
                return jsonify({'error': 'Grant request not found or already returned.'}), 404
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'error': 'An error occurred while processing your request.'}), 500



class GetBookRequests(Resource):
    def get(self):
        requests = GrantRequest.query.all()
        return jsonify([{
            'id': req.id,
            'user_id': req.user_id,
            'book_id': req.book_id,
            'status': req.status,
            'request_date': req.request_date.isoformat(),
            'grant_date': req.grant_date.isoformat() if req.grant_date else None
        } for req in requests])

class ApproveRequest(Resource):
    def post(self, request_id):
        req = GrantRequest.query.get(request_id)
        if req:
            req.status = 'Approved'
            req.grant_date = datetime.utcnow()  # Set the grant date when approved
            db.session.commit()

            # Grant access to the user
            book = Book.query.get(req.book_id)
            if book:
                book.access_granted = True
                db.session.commit()

            return jsonify({'message': 'Request approved'}), 200
        return jsonify({'message': 'Request not found'}), 404

# class ApproveRequest(Resource):
#     def post(self, request_id):
#         req = GrantRequest.query.get(request_id)
#         if req:
#             req.status = 'Approved'
#             req.grant_date = datetime.utcnow()  # Set the grant date when approved
#             db.session.commit()

#             # Grant access to the user
#             book = EBook.query.get(req.book_id)  # Assuming the model name is EBook
#             if book:
#                 book.issued = True
#                 db.session.commit()

#             # Update statistics
#             stats = stats()

#             return jsonify({'message': 'Request approved', 'stats': stats}), 200
#         return jsonify({'message': 'Request not found'}), 404


class RejectRequest(Resource):
    def post(self, request_id):
        try:
            req = GrantRequest.query.get(request_id)
            if req:
                req.status = 'Rejected'
                db.session.commit()

                # Remove user access to the book if needed
                book = Book.query.get(req.book_id)
                if book:
                    book.access_granted = False
                    db.session.commit()

                return jsonify({'message': 'Request rejected'}), 200
            return jsonify({'message': 'Request not found'}), 404
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    

# class RevokeRequest(Resource):
#     def post(self, request_id):
#         try:
#             book_request = GrantRequest.query.get(request_id)
#             if not book_request:
#                 return jsonify({'error': 'Request not found'}), 404

#             if book_request.status == 'Approved':
#                 db.session.delete(book_request)
#                 db.session.commit()

#                 # Optionally reset the book's status if needed
#                 book = Book.query.get(book_request.book_id)
#                 if book:
#                     book.is_rented = False
#                     db.session.commit()

#                 return jsonify({'message': 'Request revoked successfully'}), 200
#             else:
#                 return jsonify({'error': 'Request cannot be revoked'}), 400
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return jsonify({'error': 'An error occurred while processing your request.'}), 500

class RevokeRequest(Resource):
    def post(self, request_id):
        try:
            book_request = GrantRequest.query.get(request_id)
            if not book_request:
                return jsonify({'error': 'Request not found'}), 404

            if book_request.status == 'Approved':
                db.session.delete(book_request)
                db.session.commit()

                # Optionally reset the book's status if needed
                book = EBook.query.get(book_request.book_id)
                if book:
                    book.issued = False
                    db.session.commit()

                # Update statistics
                stats = stats()

                return jsonify({'message': 'Request revoked successfully', 'stats': stats}), 200
            else:
                return jsonify({'error': 'Request cannot be revoked'}), 400
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'error': 'An error occurred while processing your request.'}), 500



@Celery.task
def notify_admin(request_id):
    req = GrantRequest.query.get(request_id)
    if req:
        msg = Message('New Book Request', recipients=['admin@example.com'])
        msg.body = f'User {req.user_id} wants to access book {req.book_id}.'
        msg.html = f'''
            <p>User {req.user_id} wants to access book {req.book_id}.</p>
            <a href="/approve_request/{req.id}" style="margin-right: 10px;">Approve</a>
            <a href="/reject_request/{req.id}">Reject</a>
        '''
        Mail.send(msg)

# class DailyReminder(Resource):
#     def post(self):
#         task = daily_user_reminders.apply_async()
#         return jsonify({"task_id": task.id}), 202

# class TriggerMonthlyReport(Resource):
#     def post(self):
#         task = generate_monthly_report.apply_async()
#         return jsonify({"task_id": task.id}), 202

# class TriggerExportCSV(Resource):
#     def post(self):
#         librarian_email = request.json.get("email")
#         task = export_book_requests_to_csv.apply_async(args=[librarian_email])
#         return jsonify({"task_id": task.id}), 202


admin_bp = Blueprint('admin', __name__)


class TriggerExportCSV(Resource):
    def trigger_csv_export():
        export_as_csv.delay()
        return jsonify({'message': 'CSV export job triggered!'}), 202
