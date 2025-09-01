# EasyQuery

EasyQuery is an intelligent database query system that enables users to interact with any SQL/relational database using natural language. The system leverages Large Language Models (LLMs) to convert conversational queries into SQL statements, providing an intuitive interface for database exploration and analysis.

## 🚀 Live Demo
![demo](./assets/demo.gif)

The backend is live and fully functional at: **[https://easyquery-backend-latest.onrender.com](https://easyquery-backend-latest.onrender.com)**

Docker image available at: **[https://hub.docker.com/repository/docker/sadhiin/easyquery-backend](https://hub.docker.com/repository/docker/sadhiin/easyquery-backend)**
```bash
docker push sadhiin/easyquery-backend:latest
```
## Features

### Universal Database Connectivity

- **Multi-Database Support**: Connect to any SQL/relational database (MySQL, PostgreSQL, SQL Server, Oracle, SQLite, etc.)
- **Remote & Local Connections**: Support both cloud-hosted and on-premises databases
- **Secure Connection Management**: Robust credential storage and connection pooling

### Natural Language Query Interface

- **Chat-Based Interaction**: Conversational interface for database queries
- **LLM Integration**: Advanced language model to understand user intent and generate optimized SQL
- **Text & Speech Input**: Support for both typed queries and voice commands
- **Query History**: Track and revisit previous queries

### Data Visualization & Analysis

- **Automatic Charts**: Generate appropriate visualizations based on query results
- **Multiple Chart Types**: Support for bar charts, line graphs, pie charts, scatter plots, etc.
- **Interactive Dashboards**: Dynamic data exploration capabilities
- **Export Options**: Save charts and data in various formats

### User Interface

- **Intuitive Design**: Clean, modern web interface for optimal user experience
- **Database Explorer**: Browse database schema and tables
- **Results Display**: Tabular and visual representation of query results
- **Responsive Design**: Works seamlessly across devices

## Supported LLM Providers

- OpenAI GPT
- Anthropic Claude
- Google Gemini
- Groq
- And more through LangChain integration

## Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Node.js (optional, for frontend development)

### Quick Start with Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/sadhiin/EasyQuery.git
   cd EasyQuery
   ```

2. Create a `.env` file in the root directory with your configuration:

   ```env
   # Database connection (optional, can be set via UI)
   DATABASE_URL=sqlite:///./test.db

   # LLM API Keys (choose your provider)
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   GOOGLE_API_KEY=your_google_key
   GROQ_API_KEY=your_groq_key
   ```

3. Start the application:

   ```bash
   docker-compose up --build
   ```

4. Open your browser and navigate to `http://localhost`

### Local Development Setup

#### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Install dependencies:

   ```bash
   uv sync

   or 
   cd backend
   pip install -r requirements.txt
   ```

3. Run the backend server:

   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Serve the static files (using a simple HTTP server):

   ```bash
   python -m http.server 8080
   ```

3. Open your browser and navigate to `http://localhost:8080`

## Usage

### Connecting to a Database

1. In the web interface, go to the "Database Connection" section
2. Enter your database connection string (e.g., `postgresql://user:password@localhost:5432/mydb`)
3. Click "Connect" to establish the connection

### Making Queries

1. Select your preferred LLM provider from the dropdown
2. Type your natural language query in the chat interface (e.g., "Show me the top 5 selling products")
3. Press Enter or click the send button
4. View the generated SQL and query results

### Voice Queries

1. Click the microphone button to start recording
2. Speak your query clearly
3. The system will transcribe your speech and process it as a text query

### Exploring Database Schema

- Use the database explorer to browse tables, columns, and relationships
- This helps in formulating better queries and understanding the data structure

## Architecture

EasyQuery follows a three-tier architecture:

- **Frontend**: Single-page application built with vanilla HTML, CSS, and JavaScript
- **Backend**: FastAPI-based REST API server handling business logic, LLM integration, and database connections
- **Database**: User's SQL database (MySQL, PostgreSQL, etc.)

The system uses Docker for containerization, ensuring easy deployment and scalability.

## API Documentation

When running the backend locally, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `GOOGLE_API_KEY`: Google API key
- `GROQ_API_KEY`: Groq API key

### Supported Databases

- PostgreSQL
- MySQL
- SQLite
- SQL Server
- Oracle
- And other SQLAlchemy-supported databases

## Development

### Project Structure

```text
EasyQuery/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/       # API routes and endpoints
│   │   ├── core/      # Configuration and security
│   │   ├── llm/       # LLM integration
│   │   ├── models/    # Pydantic models
│   │   ├── services/  # Business logic
│   │   └── utils/     # Utility functions
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/          # Static web frontend
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── Dockerfile
│   └── nginx.conf
├── docs/              # Documentation
├── docker-compose.yml
└── pyproject.toml
```

### Running Tests

```bash
# Backend tests
cd backend

# Frontend tests (if applicable)
cd frontend
# Add your testing commands
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

- Check the [Issues](https://github.com/sadhiin/EasyQuery/issues) page
- Create a new issue with detailed information
- Contact the maintainers

## Roadmap

- [ ] Enhanced data visualization options
- [ ] Query optimization suggestions
- [ ] Multi-database query support
- [ ] Advanced analytics features
- [ ] Plugin system for custom LLM providers

---

**EasyQuery** - Making database queries as easy as asking a question!
