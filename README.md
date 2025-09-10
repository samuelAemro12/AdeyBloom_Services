# AdeyBloom AI Services

This repository contains the backend services for the AdeyBloom eCommerce project, including a Telegram bot and AI-powered features. The service is built with FastAPI.

## Features

- **FastAPI Backend**: A modern, fast (high-performance) web framework for building APIs with Python.
- **Telegram Bot Integration**: (Planned) Will handle customer interactions and notifications via Telegram.
- **AI-Powered Features**: (Planned) Will include features like product recommendations, customer sentiment analysis, etc.

## Getting Started

### Prerequisites

- Python 3.9+
- `pip` for package management

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/samuelAemro12/AdeyBloom_Services.git
    cd AdeyBloom_Services
    ```

2.  **Create and activate a virtual environment:**
    -   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To start the service, run the following command in the root directory:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

Currently, the following endpoint is available:

-   **`GET /`**: The root endpoint. Returns a welcome message to confirm that the API is running.
    -   **Response:**
        ```json
        {
          "message": "Welcome to AdeyBloom AI Services API"
        }
        ```

## Future Work

-   Implement the Telegram bot for customer service and order updates.
-   Integrate AI models for personalized product recommendations.
-   Add more API endpoints for managing products, orders, and users.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
