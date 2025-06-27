# Biztel AI Data Science Assignment

> **Note:** Please read this README  before accessing the deployed AWS endpoint. It contains important setup, usage, and authentication details.

## AWS Deployment
The API is currently deployed on an AWS EC2 instance and is publicly accessible.

**Endpoint URL:**  
[http://ec2-13-201-99-199.ap-south-1.compute.amazonaws.com:8000/docs](http://ec2-13-201-99-199.ap-south-1.compute.amazonaws.com:8000/docs)

**Authentication:**
- **API Key:** `AdityaSalagare`
- **Header:** `X-API-Key`
- In Swagger UI, click "Authorize" and enter the key.

## Objective
This project demonstrates production-level Python code, API development, and AI-driven solutions for real-world SaaS applications. It processes and analyzes chat transcripts between two agents discussing Washington Post articles, and exposes insights via a robust REST API.

---

## Assignment Tasks & How They Are Achieved

### **Task 1: Data Ingestion and Preprocessing**
- **✔ Load/process dataset with Pandas/NumPy:** `data_pipeline.py` uses Pandas for all data operations.
- **✔ Handle missing values, duplicates, incorrect types:** `DataCleaner` class handles these.
- **✔ OOP principles:** Modular classes: `DataLoader`, `DataCleaner`, `DataPreprocessor`.
- **✔ Categorical to numerical:** Label encoding is demonstrated.
- **✔ Text preprocessing:** Tokenization, stopword removal, lemmatization (NLTK).
- **✔ Preprocessing proof:** Sample before/after saved in `preprocessing_working.txt`.

### **Task 2: Exploratory Data Analysis (EDA)**
- **✔ Advanced EDA:** `eda.py` prints and visualizes agent/article-level stats, sentiment, turn ratings, and word frequencies.
- **✔ Hierarchical summaries:** Article and agent summaries, plus visualizations.
- **✔ Transcript-level summary via LLM:** `summarizer.py` uses a light LLM (DistilBART) for transcript summarization.
- **✔ Accuracy reporting:** All non-summary fields are directly derived from the data (100% accurate).

### **Task 3: REST API with FastAPI**
- **✔ FastAPI REST API:** `main.py` implements all endpoints.
- **✔ Endpoint 1:** `/summary` (dataset summary)
- **✔ Endpoint 2:** `/transform` (real-time text preprocessing)
- **✔ Endpoint 3:** `/analyze-transcript/{transcript_id}` (detailed transcript analysis)
- **✔ Error handling & logging:** Built-in FastAPI and Python logging.
- **✔ Performance:** Model loaded once, async endpoints.
- **✔ Authentication:** All endpoints except `/` require `X-API-Key` header.

### **Task 4: OOP Concepts**
- **✔ Modular, reusable, well-documented classes for each pipeline stage.**

### **Task 5: Code Optimization & Performance**
- **✔ Vectorized Pandas operations.**
- **✔ Async API endpoints.**
- **✔ Model loaded once for efficiency.**

### **Bonus Points**
- **✔ Authentication:** API key required for all endpoints except root.
- **✔ Dockerization:** `Dockerfile` and `.dockerignore` included for easy containerization.
- **✔ CI/CD:** GitHub Actions and CircleCI pipelines for automated testing and linting.
- **✔ Kubernetes:** Manifests for deploying to a K8s cluster.
- **✔ Monitoring:** Integrated with Datadog and Bugsnag.

---

## Project Structure
- `BiztelAI_DS_Dataset_V1.json` — The dataset
- `data_pipeline.py` — Data loading, cleaning, preprocessing (OOP)
- `eda.py` — Exploratory data analysis and visualizations
- `summarizer.py` — Transcript analysis and summarization (LLM)
- `main.py` — FastAPI REST API
- `requirements.txt` — Python dependencies
- `Dockerfile`, `.dockerignore` — For containerization
- `.github/workflows/ci-cd.yml` — GitHub Actions workflow
- `.circleci/config.yml` — CircleCI configuration
- `kubernetes/` — Kubernetes deployment and service manifests
- `tests/` — Automated tests for the API
- `.gitignore` — For Git hygiene
- `preprocessing_working.txt` — Proof of preprocessing (sample before/after)
- `plots/` — EDA visualizations

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <my-repository-url i.e this reposittories url>
   cd <repository-directory> in which u have stored the project
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Download NLTK data:**
   ```bash 
  python nltkdownload.py
   ```

---

## How to Run

### 1. **Data Preprocessing Working**
To generate a sample of before/after preprocessing:
```bash
python data_pipeline.py
```
- Output: `preprocessing_working.txt` (shows 10 sample messages before and after processing)

### 2. **Exploratory Data Analysis (EDA)**
To generate summary stats and plots:
```bash
python eda.py
```
- Output: Console summary and PNG plots in `plots/`

### 3. **Run the API Server**
To start the FastAPI server:
```bash
uvicorn main:app --reload
```
- The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

#### **Authentication**
- All endpoints except `/` require the header: `X-API-Key: <your_key>`
- Default key: `AdityaSalagare`
- In Swagger UI (`/docs`), click "Authorize" at the top right, enter the key, and click "Authorize".
- With `curl`:
  ```bash
  curl -H "X-API-Key: AdityaSalagare" http://127.0.0.1:8000/summary
  ```

### 4. **Run with Monitoring (Datadog & Bugsnag)**
To run the app with performance monitoring and error tracking enabled:
1.  Set your environment variables:
    ```bash
    export API_KEY="your-secret-key"
    export BUGSNAG_API_KEY="your-bugsnag-key"
    export DD_API_KEY="your-datadog-key"
    export DD_ENV="development"
    export DD_SERVICE="biztel-api"
    export DD_VERSION="1.0"
    ```
2.  Run the application with `dd-trace-run`:
    ```bash
    dd-trace-run uvicorn main:app --reload
    ```

#### **Authentication**
- All endpoints except `/` require the header: `X-API-Key: <your_key>`
- Default key: `AdityaSalagare`
- In Swagger UI (`/docs`), click "Authorize" at the top right, enter the key, and click "Authorize".
- With `curl`:
  ```bash
  curl -H "X-API-Key: AdityaSalagare" http://127.0.0.1:8000/summary
  ```

### 5. **Docker (Optional)**
To build and run the API in a container:
```bash
docker build -t biztel-api-app .
docker run -p 8000:8000 \
  -e API_KEY="your-secret-key" \
  -e BUGSNAG_API_KEY="your-bugsnag-key" \
  -e DD_API_KEY="your-datadog-key" \
  biztel-api-app
```

### 6. **Deploy to Kubernetes (Optional)**
If you have a Kubernetes cluster (like Minikube, Docker Desktop K8s, or a cloud provider like EKS):
1.  **Build and push your Docker image** to a registry like Docker Hub:
    ```bash
    docker build -t your-dockerhub-username/biztel-api:latest .
    docker push your-dockerhub-username/biztel-api:latest
    ```
2.  **Update the image name** in `kubernetes/deployment.yaml`.
3.  **Apply the manifests:**
    ```bash
    kubectl apply -f kubernetes/
    ```

---

## CI/CD Pipelines
This project is configured with CI/CD pipelines for both **GitHub Actions** and **CircleCI**.
- **What they do:** On every push or pull request to the `main` branch, the pipelines automatically install dependencies, run code quality checks (`flake8`), and execute automated tests (`pytest`).
- **Location:**
    - GitHub Actions: `.github/workflows/ci-cd.yml`
    - CircleCI: `.circleci/config.yml`

---

## How to Test the API with Swagger UI

1. **Open Swagger UI**
   - Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

2. **Authorize with API Key**
   - Click the "Authorize" button at the top right.
   - Enter `AdityaSalagare` in the `X-API-Key` field or where the header is needed.
   - Click "Authorize".

3. **Test Each Endpoint**
   - **GET /** (Read Root)
     - Click the GET / section to expand it.
     - Click **Try it out**.
     - Click **Execute**.
     - You should see a welcome message in the response.
   - **GET /summary** (Get Dataset Summary)
     - Expand the GET /summary section.
     - Click **Try it out**.
     - Click **Execute**.
     - You'll get a JSON summary of the dataset.
   - **POST /transform** (Preprocess Raw Text)
     - Expand the POST /transform section.
     - Click **Try it out**.
     - In the **Request body** field, enter:
       ```json
       {
         "text": "This is an example sentence for preprocessing!"
       }
       ```
     - Click **Execute**.
     - You'll see the original and preprocessed text in the response.
   - **GET /analyze-transcript/{transcript_id}** (Analyze a Transcript)
     - Expand the GET /analyze-transcript/{transcript_id} section.
     - Click **Try it out**.
     - Enter a valid `transcript_id` (you can get one from your dataset or from the `/summary` endpoint).
       - Example: `t_d004c097-424d-45d4-8f91-833d85c2da31`
     - Click **Execute**.
     - You'll get a detailed analysis and summary for that transcript.

---

## API Endpoints

- **GET `/`** — Welcome message
- **GET `/summary`** — Dataset summary (requires API key)
- **POST `/transform`** — Preprocess raw text (requires API key)
- **GET `/analyze-transcript/{transcript_id}`** — Analyze a transcript (requires API key)

Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Methodologies & Insights
- **OOP pipeline:** Modular, reusable, and well-documented classes for each stage
- **EDA:** In-depth analysis of agent behavior, sentiment, and conversation structure
- **Transcript analysis:** Uses a light LLM for summarization; all other fields are 100% accurate from the data
- **API:** Async, production-ready, with error handling, logging, and authentication
- **Preprocessing proof:** See `preprocessing_working.txt` for before/after samples
- **Docker:** Fully containerized for easy deployment using a multi-stage build for a smaller, more secure image.
- **CI/CD:** Automated testing and linting pipelines ensure code quality and stability.
- **Kubernetes:** Manifests are provided for scalable and orchestrated deployments.
- **Monitoring:** Integrated with Datadog for performance tracing and Bugsnag for real-time error monitoring.

---

## Submission Checklist
- [x] Dockerfile and .dockerignore for containerization
- [x] Authentication for API endpoints
- [x] CI/CD pipelines (GitHub Actions, CircleCI)
- [x] Kubernetes deployment manifests
- [x] Monitoring integration (Datadog, Bugsnag)
- [x] Preprocessing proof file

---

## Notes
- All code is production-ready, modular, and well-documented.
- For any questions or further improvements (e.g., advanced authentication, deployment), see code comments or contact the author. 

## Sample change 