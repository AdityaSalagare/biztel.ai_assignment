# Project Documentation: Insights and Methodologies

## 1. Introduction
This document provides a detailed explanation of the methodologies, architectural choices, and key insights derived from the Biztel AI assignment. The goal was to build a production-ready data analysis pipeline and API, starting from a raw dataset of chat transcripts.

---

## 2. Methodologies and Architecture

### 2.1. Data Pipeline (`data_pipeline.py`)
The foundation of the project is a modular, Object-Oriented Programming (OOP) pipeline that ensures code reusability, maintainability, and clarity.

-   **`DataLoader` Class**:
    -   **Responsibility**: Handles loading the raw `BiztelAI_DS_Dataset_V1.json` file.
    -   **Methodology**: It reads the nested JSON and flattens it into a structured Pandas DataFrame. Each row in the DataFrame represents a single turn in a conversation, which is a much more convenient format for analysis.

-   **`DataCleaner` Class**:
    -   **Responsibility**: Ensures the quality and integrity of the data.
    -   **Methodology**:
        -   **Missing Value Handling**: Rows with missing `message` or `agent` fields are dropped, as these are critical for any meaningful analysis.
        -   **Duplicate Record Removal**: The `drop_duplicates()` function is used on a subset of columns (`transcript_id`, `agent`, `message`). This was a deliberate choice to avoid a `TypeError` caused by the `knowledge_source` column, which contains unhashable lists. This approach correctly identifies and removes duplicate turns without causing errors.

-   **`DataPreprocessor` Class**:
    -   **Responsibility**: Transforms raw text and categorical data into a format suitable for analysis and machine learning.
    -   **Methodology**:
        -   **Text Preprocessing**: For each message, a standard NLP preprocessing pipeline is applied:
            1.  **Lowercasing**: To ensure uniformity.
            2.  **Tokenization**: Splitting text into individual words.
            3.  **Stopword Removal**: Removing common words (e.g., "the", "a", "in") using NLTK's English stopword list.
            4.  **Punctuation Removal**.
            5.  **Lemmatization**: Reducing words to their base or root form (e.g., "running" to "run") using NLTK's `WordNetLemmatizer`. This helps in consolidating word counts and identifying topics more accurately.
        -   **Categorical Encoding**: The file includes a function to convert categorical columns (like `sentiment`) into numerical representations using `sklearn.preprocessing.LabelEncoder`, a necessary step for many machine learning models.

### 2.2. Exploratory Data Analysis (EDA) (`eda.py`)
The EDA script was designed to uncover patterns and generate high-level insights from the dataset.

-   **Methodology**:
    -   **Statistical Summaries**: It generates summaries at different levels:
        -   **High-Level**: Overall statistics for the entire dataset.
        -   **Article-Level**: Aggregates data by `article_url` to see which articles generate the most conversation.
        -   **Agent-Level**: Aggregates data by `agent` to compare their communication patterns (e.g., message count, average message length, sentiment distribution).
    -   **Visualizations**: It uses Matplotlib and Seaborn to create several plots, which are saved to the `/plots` directory. These include distributions of messages, sentiments, turn ratings, and conversation lengths, providing a quick visual understanding of the data's characteristics. Word clouds and bar charts are used to visualize the most frequent topics.

### 2.3. AI-Driven Transcript Analysis (`summarizer.py`)
This module uses a lightweight, open-source Large Language Model (LLM) to perform specific analysis on individual transcripts.

-   **Methodology**:
    -   **LLM Choice**: We use `sshleifer/distilbart-cnn-6-6`, a distilled version of the BART model. It was chosen for its excellent summarization capabilities and its small footprint, making it fast and efficient for a real-time API.
    -   **Insight Extraction**:
        -   **Possible Article Link, Message Counts**: These are extracted directly from the dataset for the given `transcript_id`. This method is deterministic and 100% accurate against the provided data.
        -   **Overall Sentiment**: This is calculated by finding the statistical **mode** (the most frequent value) of all sentiment labels for each agent within the transcript. This is a robust way to determine the dominant sentiment without being skewed by single outlier emotions.
        -   **Conversation Summary**: The full text of the transcript is concatenated and fed to the DistilBART model to generate a concise summary of the conversation.

### 2.4. API Development and Optimization (`main.py`)
The API exposes the project's functionalities through a RESTful interface, built with performance and scalability in mind.

-   **Methodology**:
    -   **Framework**: FastAPI was chosen for its high performance, native `async` support, automatic data validation with Pydantic, and interactive documentation (Swagger UI).
    -   **Performance Optimization**:
        1.  **Model Loading**: The `TranscriptAnalyzer` (and the underlying LLM) is loaded only **once** at startup using FastAPI's `lifespan` event handler. This avoids the significant overhead of reloading the model on every API request.
        2.  **Asynchronous Endpoints**: All endpoints are defined with `async def`, allowing the server to handle multiple concurrent requests efficiently without blocking.
    -   **Security**: A simple but effective API key authentication mechanism (`X-API-Key` header) is implemented to protect the endpoints.
    -   **Error Handling**: The API uses FastAPI's built-in `HTTPException` to return clear, standard HTTP error responses.

### 2.5. Deployment (AWS EC2)
The application was deployed to a public endpoint to demonstrate its production readiness.

-   **Methodology**:
    1.  An **AWS EC2 t2.micro (Free Tier)** instance running Amazon Linux 2 was launched.
    2.  The environment was set up with Git, Python 3, and a virtual environment.
    3.  Challenges related to the environment were resolved:
        -   **Memory Issues**: A **swap file** was created to provide extra memory, preventing the `pip install` process from being killed while installing large packages like `torch`.
        -   **Dependency Conflicts**: Specific versions of packages (`urllib3`, `safetensors`) were installed to resolve compatibility issues with the older OpenSSL version on Amazon Linux 2.
    4.  The EC2 **Security Group** (firewall) was configured to allow inbound traffic on port `8000`.
    5.  The `uvicorn` server was run persistently using the `screen` utility, ensuring the API remains active even after the SSH session is disconnected.

---

## 3. Key Insights from the Data

The analysis revealed several key insights into the agents' interactions:

1.  **Agent Behavior**:
    -   `agent_1` sends slightly more messages, but `agent_2`'s messages are, on average, longer. This could indicate that `agent_2` is more descriptive in their responses.
    -   The number of turns per conversation varies, but most conversations are substantial in length.

2.  **Sentiment and Tone**:
    -   The most dominant sentiment by far is **"Curious to dive deeper,"** followed by "Neutral" and "Happy." This suggests that the agents are actively engaged and maintain a positive, inquisitive tone throughout their discussions.
    -   Negative sentiments like "Angry," "Disgusted," and "Fearful" are extremely rare, indicating professional and constructive conversations.

3.  **Conversation Quality**:
    -   The vast majority of conversation turns are rated as **"Excellent"** or **"Good."** This high quality is a strong indicator of a well-curated dataset and effective agent communication.

4.  **Common Topics**:
    -   The word clouds and frequency charts are dominated by terms like `"team"`, `"game"`, `"player"`, `"washington"`, `"post"`, and `"article"`. This clearly confirms that the conversations revolve around sports articles published in the Washington Post, aligning with the dataset's description.

---

## 4. Conclusion
This project successfully fulfills all assignment requirements, delivering a well-structured, documented, and deployed application. It demonstrates a comprehensive understanding of production-level data science workflows, from data ingestion and analysis to API development and cloud deployment. 