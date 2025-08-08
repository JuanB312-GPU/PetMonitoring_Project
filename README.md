# PetMonitoring_Project
Repository for the Pet Monitoring website, this web application allows users to create complete profiles of their pets and generate health reports based on body metrics and other behaviors, such as feeding, medical conditions, breed, etc.

## Used Technologies
A suite of software technologies for backend and frontend development, and database management.
- Python 3.x
- HTML
- PostgreSQL
- JavaScript

## Database Management Libraries and Frameworks
- FastAPI – Web framework for building APIs.
- SQLAlchemy – ORM for database communication.
- Bcrypt – Library for password hashing.
- Pydantic – Data validation and settings management using Python type hints (commonly used with JSON data).

## Testing Strategy & Quality Assurance

Testing is a critical component of this project, ensuring reliability, functionality, and user satisfaction. Our comprehensive testing approach includes multiple layers:

### Testing Types
- **Unit Tests** (`testing/unit/`) - Test individual components in isolation
  - Backend services, repositories, and utilities
  - Frontend components and functions
  - Validates core business logic and data processing

- **Integration Tests** (`testing/integration/`) - Test component interactions
  - API endpoint validation
  - Database operations and transactions
  - Service layer integration with data layer

- **Acceptance Tests** (`testing/acceptance/`) - Test user scenarios end-to-end
  - Complete user workflows using Behave framework
  - Business requirement validation
  - Real-world usage scenarios

- **Stress Tests** (`testing/stress/`) - Test system performance and limits
  - Load testing with JMeter
  - Performance benchmarking
  - System scalability validation

### Why Testing Matters
1. **Reliability** - Ensures the application works consistently across different scenarios
2. **User Safety** - Critical for pet health data accuracy and system trustworthiness
3. **Maintainability** - Facilitates safe code changes and feature additions
4. **Quality Assurance** - Validates that features meet specified requirements
5. **Regression Prevention** - Catches issues before they reach production

### Running Tests
Each testing directory contains specific README files with detailed instructions for running tests in that category. Tests can be executed individually or as part of the complete test suite.

## Installation & Setup

### Prerequisites
- Python 3.x (recommended 3.9 or higher)
- PostgreSQL database server
- Node.js (for frontend package management)
- Git (for version control)

### Database Setup
1. Install PostgreSQL on your system
2. Create a database named `PetMonitoring`
3. Update database credentials in `backend/config/settings.py` or create a `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/PetMonitoring
   SECRET_KEY=your-secret-key-here
   CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:8000,http://localhost:8000
   ```

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PetMonitoring_Project
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

4. **Initialize the database:**
   The application will automatically create tables on first run.

## Running the Application

### Quick Start (Windows)
- **PowerShell Script:** Run `start_app.ps1` for automated setup and launch
- **Batch File:** Run `start_app.bat` for basic startup

### Manual Execution
1. **Start the backend server:**
   ```bash
   python main.py
   ```
   The FastAPI server will start on `http://localhost:8000`

2. **Access the application:**
   - Open your web browser and navigate to `http://localhost:8000`
   - The API documentation is available at `http://localhost:8000/docs`

### Development Mode
- **Backend:** The FastAPI server includes auto-reload functionality for development
- **Frontend:** Static files are served directly by FastAPI
- **Testing:** Use `npm test` for frontend tests or run specific test suites from the testing directories

## Project Architecture

### Backend Structure
- **FastAPI Framework:** Modern, fast web framework for building APIs
- **SQLAlchemy ORM:** Database abstraction layer with PostgreSQL
- **Modular Design:** Organized in services, repositories, and routers
- **Authentication:** Secure user authentication with bcrypt password hashing

### Frontend Structure
- **Component-based:** Modular JavaScript components for different features
- **Responsive Design:** CSS styling optimized for various screen sizes
- **API Integration:** Seamless communication with backend services

### Key Directories
- `backend/` - All backend Python code (models, services, routers)
- `components/` - Frontend JavaScript components and styles
- `assets/` - Static assets (CSS, JS, images)
- `testing/` - Comprehensive test suites
- `diagrams/` - Project documentation and visual diagrams
- `database/` - Database-related files and configurations

## API Endpoints

The application provides RESTful API endpoints for:
- **Authentication:** User registration and login
- **Pet Management:** CRUD operations for pet profiles
- **Medical Records:** Health conditions, vaccinations, treatments
- **Activity Tracking:** Feeding, exercise, and behavior monitoring
- **Reports:** Health analytics and data visualization

Complete API documentation is available at `/docs` when the server is running.

## Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Application secret key for security
- `CORS_ORIGINS`: Allowed origins for CORS policy

### Database Configuration
The application uses PostgreSQL with SQLAlchemy ORM. Database models are automatically synchronized on startup.

## Contributing

### Development Workflow
1. Create a feature branch from main
2. Implement changes with appropriate tests
3. Run the complete test suite
4. Submit a pull request with detailed description

### Code Quality
- Follow Python PEP 8 style guidelines
- Write comprehensive tests for new features
- Document API changes and new endpoints
- Ensure all tests pass before submitting changes

## Project Features
### Create user account
Create a personal account, to monitor your pets' health:

![Register form](imgs/uRegister.png)

## Create pet's profile
Create a specific profile for your pets, with sepecies, breed, medical conditions and applicated vaccines:

![Register form](imgs/PRegister.png)

## Special description cards for each pet
The website displays a special description sheet for each pet, indicating its age, medical conditions, and vaccinations:

![Register form](imgs/CardP.png)

## Troubleshooting

### Common Issues

**Database Connection Error:**
- Ensure PostgreSQL service is running
- Verify database credentials in settings
- Check if the database `PetMonitoring` exists

**Port Already in Use:**
- The application uses port 8000 by default
- Kill any existing processes or change the port in main.py

**Module Import Errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python path and virtual environment setup

**Frontend Assets Not Loading:**
- Check that static files are properly served by FastAPI
- Verify file paths in HTML templates

### Performance Considerations
- The application includes database connection pooling for optimal performance
- Static files are efficiently served by FastAPI
- Database queries are optimized through SQLAlchemy ORM

## License & Support

This project is developed for educational purposes as part of a university software engineering seminar. For support or questions, please refer to the project documentation or contact the development team.

## Future Enhancements

- Mobile application development
- Advanced health analytics and AI predictions
- Integration with veterinary services
- Real-time notifications and alerts
- Multi-language support
- Cloud deployment options