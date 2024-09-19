
# Collaborative Document Editing Platform

A web-based platform built with Python and Flask that allows users to collaborate on documents in real-time. This platform features user authentication, document creation, sharing, versioning, and real-time editing with multiple collaborators.

There is no link, as you have to host the server yourselfe. Please understand this, as i canot pay for  a python server. But i included a tutorial to host the server.


![image](https://github.com/user-attachments/assets/24b7ef39-17f2-4c48-bba7-8e1b7a28d99f)

## Features

- **User Authentication**: Sign up, login, and logout functionality.
- **Document Management**: Create, edit, view, and delete documents.
- **Real-Time Collaboration**: Collaborate with others in real-time with WebSocket integration.
- **Document Sharing**: Share documents with other users and collaborate together.
- **Version Control**: Track document history and restore previous versions.
- **Search Functionality**: Search and filter documents by title and content.
- **Responsive Design**: Basic UI with CSS for a better user experience.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jojo20071/colabP
   cd collaborative-document-platform
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   ```bash
   python app.py
   ```

5. **Run the application**:
   ```bash
   flask run
   ```
   Or for production:
   ```bash
   gunicorn --bind 0.0.0.0:8000 wsgi:app
   ```

## Usage

- **Sign Up**: Create a new account.
- **Login**: Access your dashboard.
- **Create Documents**: Start creating and editing documents.
- **Share Documents**: Invite others to collaborate on your documents.
- **Collaborate**: See real-time changes from other users.
- **Manage Versions**: View and restore previous versions of documents.

## Future Improvements

- Improve the UI design.
- Add more collaboration features like comments, chat, etc.
- Enhance security features.
- Implement more advanced search options.

## Contributing

Feel free to fork this project, create issues, or submit pull requests.
