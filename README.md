# AI Website Builder

A powerful AI-driven website builder similar to v0.dev that allows users to generate beautiful, functional websites using natural language prompts.

## Features

- 🤖 **AI-Powered Generation**: Create websites using natural language descriptions
- 🔐 **Authentication**: Secure login/signup with Firebase Auth
- 📱 **Responsive Design**: Modern, mobile-first UI design
- 💾 **Project Management**: Save, organize, and manage your generated websites
- ⬇️ **Easy Export**: Download websites as single HTML files
- ⚡ **Fast Generation**: Get results in 10-15 seconds
- 🎨 **Beautiful UI**: Clean, intuitive interface inspired by modern design

## Tech Stack

### Frontend
- **HTML5/CSS3/JavaScript**: Pure vanilla implementation (no React/Vue)
- **Firebase SDK**: Authentication and real-time database
- **Modern CSS**: Flexbox, Grid, CSS Variables, Animations

### Backend
- **Python/Flask**: Lightweight web framework
- **Firebase Admin**: Server-side Firebase integration
- **Groq API**: AI model integration for website generation
- **Hugging Face**: Additional AI model support

### Database
- **Firebase Firestore**: NoSQL document database
- **Real-time sync**: Live updates across devices

## Project Structure

\`\`\`
ai-website-builder/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── scripts/              # Database and utility scripts
│   ├── setup_database.py    # Initial database setup
│   └── migrate_database.py  # Database migrations
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   │   ├── style.css       # Main page styles
│   │   ├── auth.css        # Authentication page styles
│   │   └── dashboard.css   # Dashboard styles
│   └── js/              # JavaScript files
│       ├── main.js         # Main page functionality
│       ├── auth.js         # Authentication logic
│       └── dashboard.js    # Dashboard functionality
└── templates/            # HTML templates
    ├── index.html          # Landing page with chat interface
    ├── auth.html           # Login/signup page
    └── dashboard.html      # User dashboard
\`\`\`

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- Firebase project
- Groq API key
- Hugging Face token

### 2. Firebase Setup

1. Create a new Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Authentication (Email/Password and Google)
3. Create a Firestore database
4. Download the service account key JSON file
5. Update the Firebase config in the JavaScript files

### 3. Environment Setup

1. Clone the repository:
\`\`\`bash
git clone <repository-url>
cd ai-website-builder
\`\`\`

2. Create a virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Set up environment variables:
\`\`\`bash
export GROQ_API_KEY="your-groq-api-key"
export HUGGING_FACE_TOKEN="your-hugging-face-token"
\`\`\`

### 4. Database Setup

Run the database setup script:
\`\`\`bash
python scripts/setup_database.py
\`\`\`

### 5. Configuration

Update the following files with your API keys and Firebase config:

- `app.py`: Update API keys and Firebase credentials path
- `static/js/*.js`: Update Firebase configuration objects

### 6. Run the Application

\`\`\`bash
python app.py
\`\`\`

The application will be available at `http://localhost:5000`

## API Endpoints

### Website Generation
- `POST /api/generate-website`: Generate a website from a prompt
- `GET /api/get-projects/<user_id>`: Get user's projects
- `GET /api/download-project/<project_id>`: Download a project

### Authentication
- Handled by Firebase Auth on the frontend
- User data stored in Firestore

## Usage

### 1. Authentication
- Visit `/auth` to login or create an account
- Support for email/password and Google authentication

### 2. Generate Websites
- Use the chat interface on the homepage
- Enter a natural language description of your desired website
- Wait 10-15 seconds for AI generation
- Preview the result in the embedded iframe

### 3. Manage Projects
- Access your dashboard to view all created projects
- Download projects as single HTML files
- Delete unwanted projects

### 4. Example Prompts
- "Create a modern portfolio website for a photographer"
- "Build a landing page for a tech startup with pricing section"
- "Make a restaurant website with menu and contact information"
- "Design a blog layout with sidebar and article grid"

## AI Integration

The application uses multiple AI services:

- **Groq API**: Primary AI model for website generation
- **Hugging Face**: Backup AI model support
- **Custom Prompts**: Optimized system prompts for web development

## Security Features

- Firebase Authentication for secure user management
- Server-side API key management
- Input sanitization and validation
- CORS protection
- Secure file downloads

## Performance Optimizations

- Lazy loading of preview iframes
- Efficient database queries with proper indexing
- Client-side caching of user data
- Optimized CSS and JavaScript delivery

## Deployment

### Production Deployment

1. Set up a production Firebase project
2. Configure environment variables on your hosting platform
3. Update API endpoints and Firebase config for production
4. Deploy using your preferred platform (Heroku, Vercel, etc.)

### Environment Variables for Production
\`\`\`
FLASK_ENV=production
GROQ_API_KEY=your-production-groq-key
HUGGING_FACE_TOKEN=your-production-hf-token
FIREBASE_CREDENTIALS_PATH=path/to/production/credentials.json
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the example implementations

## Roadmap

- [ ] Template library for quick starts
- [ ] Advanced customization options
- [ ] Team collaboration features
- [ ] Version control for projects
- [ ] Custom domain deployment
- [ ] Advanced AI model options
- [ ] Plugin system for extensions
