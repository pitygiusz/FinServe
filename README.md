# Assessment Task: FinServe

This repository contains a working prototype of an AI-powered customer support system (Streamlit frontend and n8n backend), built as a scalable business solution for FinServe.

**[Full project documentation available here.](documentation.md)**

## Repository Structure

  * **`app.py`** – The main frontend application written in Python using Streamlit.
  * **`FinServe.json`** – The exported automation workflow ready to be imported into n8n (handling the backend orchestration and AI logic).
  * **`documentation.md`** – Comprehensive project documentation, including the analysis of business problems, solution architecture and future enhancements.
  * **`Scenarios.xlsx`** – Sample data containing mock policies to be used with the Google Sheets node.
  * **`.env.example`** – A template configuration file for environment variables.



## How to Run

### 1\. Running the Frontend (Python/Streamlit)

1.  Clone this repository:
    ```bash
    git clone https://github.com/pitygiusz/FinServe/
    cd FinServe
    ```
2. Install dependencies:
    ```bash
    pip install streamlit requests python-dotenv
    ```
3.  Rename `.env.example` to `.env` and paste your active n8n Webhook URL inside.
4.  Run the application:
    ```bash
    streamlit run app.py
    ```

### 2\. Running the Backend (n8n Orchestration)

1.  Log in to your n8n instance.
2.  Create new workflow from `FinServe.json` file provided in this repository.
3.  Set up credentials for Google Sheets (sample scenarios are available in `Scenarios.xlsx`) and Gemini AI nodes.
4.  Activate the workflow.