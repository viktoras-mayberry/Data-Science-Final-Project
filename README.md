# 🎓 Data Science Final Project — Customer Churn Prediction

> **Final Capstone Project** for the 6-Month Data Science Training Program

## 📋 Project Overview

You are a Data Scientist at a telecommunications company. The business is experiencing customer churn — customers leaving for competitors. Your task is to **analyze customer data, identify key churn drivers, and build predictive models** to help the business proactively retain customers.

This project is designed to test your skills across the full data science pipeline:

| Skill Area | How It's Applied |
|---|---|
| **Python** | End-to-end scripting, data wrangling with Pandas & NumPy |
| **PostgreSQL & pgAdmin** | Storing data in a relational database, writing SQL queries |
| **EDA** | Visualizations with Matplotlib/Seaborn, statistical analysis |
| **Machine Learning** | Logistic Regression, Random Forest, XGBoost |
| **Deep Learning** | Feedforward Neural Network with TensorFlow/Keras |
| **GitHub** | Version control, branching, pull requests for submission |

---

## 📊 Dataset

You will use the **Telco Customer Churn** dataset from Kaggle.

🔗 **Download Link:** [https://www.kaggle.com/datasets/blastchar/telco-customer-churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

Download the CSV file and place it in: `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`

### Column Descriptions

| Column | Description |
|---|---|
| `customerID` | Unique customer identifier |
| `gender` | Male / Female |
| `SeniorCitizen` | Whether the customer is a senior citizen (1/0) |
| `Partner` | Whether the customer has a partner (Yes/No) |
| `Dependents` | Whether the customer has dependents (Yes/No) |
| `tenure` | Number of months the customer has stayed |
| `PhoneService` | Whether the customer has phone service (Yes/No) |
| `MultipleLines` | Multiple lines service (Yes/No/No phone service) |
| `InternetService` | Type of internet service (DSL/Fiber optic/No) |
| `OnlineSecurity` | Online security add-on (Yes/No/No internet service) |
| `OnlineBackup` | Online backup add-on (Yes/No/No internet service) |
| `DeviceProtection` | Device protection add-on (Yes/No/No internet service) |
| `TechSupport` | Tech support add-on (Yes/No/No internet service) |
| `StreamingTV` | Streaming TV add-on (Yes/No/No internet service) |
| `StreamingMovies` | Streaming movies add-on (Yes/No/No internet service) |
| `Contract` | Contract term (Month-to-month/One year/Two year) |
| `PaperlessBilling` | Paperless billing (Yes/No) |
| `PaymentMethod` | Payment method |
| `MonthlyCharges` | Monthly charge amount |
| `TotalCharges` | Total charges to date |
| `Churn` | Whether the customer churned (Yes/No) — **TARGET** |

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **PostgreSQL 14+** — [Download](https://www.postgresql.org/download/)
- **pgAdmin 4** — [Download](https://www.pgadmin.org/download/) (usually bundled with PostgreSQL)
- **Git** — [Download](https://git-scm.com/downloads)
- **Jupyter Notebook** (installed via `requirements.txt`)

---

## 🚀 Getting Started

### Step 1: Fork & Clone the Repository

```bash
# Fork this repository on GitHub (click the "Fork" button)
# Then clone your fork:
git clone https://github.com/<your-username>/data-science-final-project.git
cd data-science-final-project
```

### Step 2: Set Up the Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Set Up PostgreSQL & pgAdmin

#### 3a. Create the Database Using pgAdmin

1. **Open pgAdmin 4** from your Start Menu (Windows) or Applications (macOS).
2. In the left panel, expand **Servers** → right-click on your server → **Connect**.
3. Enter your PostgreSQL password when prompted.
4. Right-click on **Databases** → **Create** → **Database...**
5. Set the database name to: `telco_churn`
6. Click **Save**.

#### 3b. Create the Tables Using pgAdmin

1. In pgAdmin, expand **Databases** → **telco_churn**.
2. Click on **telco_churn** to select it, then click **Tools** → **Query Tool** in the top menu.
3. Open the file `database/schema.sql` from this project.
4. Copy the entire SQL content into the Query Tool.
5. Click the **▶ Execute/Run** button (or press `F5`).
6. You should see a "Commands completed successfully" message.
7. Verify the tables were created: expand **Schemas** → **public** → **Tables** — you should see `customers`, `services`, and `billing`.

#### 3c. Create the `.env` File

Create a `.env` file in the project root with your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=telco_churn
DB_USER=postgres
DB_PASSWORD=your_password_here
```

> ⚠️ **IMPORTANT:** The `.env` file is listed in `.gitignore` and will **NOT** be pushed to GitHub. Never commit credentials to a repository.

#### 3d. Download the Dataset & Seed the Database

1. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn).
2. Place the CSV file at: `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`
3. Run the seed script:

```bash
python database/seed_data.py
```

This will read the CSV and populate the PostgreSQL tables.

#### 3e. Verify the Data in pgAdmin

1. Go back to pgAdmin → **Query Tool** (for `telco_churn` database).
2. Run these verification queries:

```sql
-- Check row counts
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM services;
SELECT COUNT(*) FROM billing;

-- Preview customer data
SELECT * FROM customers LIMIT 10;

-- Check churn distribution
SELECT churn, COUNT(*) FROM billing GROUP BY churn;
```

You should see approximately **7,043 rows** in each table.

---

## 📝 Step-by-Step Project Guide

Work through the notebooks in order. Each notebook contains **instructions, TODOs, and starter code** — your job is to complete the implementation.

### Phase 1: Data Loading & SQL Integration (`notebooks/01_data_loading.ipynb`)
- Connect to your PostgreSQL database using SQLAlchemy
- Write SQL queries to extract and join data from multiple tables
- Load the results into Pandas DataFrames
- Perform initial data inspection

### Phase 2: Exploratory Data Analysis (`notebooks/02_eda.ipynb`)
- Analyze distributions of numerical and categorical features
- Create visualizations: histograms, bar charts, box plots, heatmaps
- Investigate churn patterns across customer segments
- Document your key findings and insights

### Phase 3: Feature Engineering (`notebooks/03_feature_engineering.ipynb`)
- Handle missing values
- Encode categorical variables (Label Encoding / One-Hot Encoding)
- Scale numerical features using StandardScaler
- Engineer new features (e.g., tenure groups, charge ratios)
- Split data into training and test sets

### Phase 4: Machine Learning Models (`notebooks/04_machine_learning.ipynb`)
- Train a Logistic Regression baseline model
- Train a Random Forest classifier
- Train an XGBoost classifier
- Perform hyperparameter tuning with GridSearchCV
- Analyze feature importance

### Phase 5: Deep Learning Model (`notebooks/05_deep_learning.ipynb`)
- Build a feedforward neural network using TensorFlow/Keras
- Design the architecture (layers, activations, dropout)
- Train with early stopping and validation monitoring
- Visualize training/validation loss curves

### Phase 6: Model Evaluation & Report (`notebooks/06_evaluation.ipynb`)
- Compare all models using: Accuracy, Precision, Recall, F1-Score, AUC-ROC
- Generate confusion matrices and ROC curves
- Write your final recommendation with business interpretation
- Summarize the entire project

---

## 📁 Project Structure

```
data-science-final-project/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── .env                               # Your database credentials (NOT committed)
├── SUBMISSION_GUIDE.md                # How to submit your project
│
├── data/
│   └── raw/                           # Place your CSV dataset here
│
├── database/
│   ├── schema.sql                     # PostgreSQL table definitions
│   └── seed_data.py                   # Script to populate the database
│
├── notebooks/
│   ├── 01_data_loading.ipynb          # Phase 1: SQL & Data Loading
│   ├── 02_eda.ipynb                   # Phase 2: Exploratory Data Analysis
│   ├── 03_feature_engineering.ipynb   # Phase 3: Feature Engineering
│   ├── 04_machine_learning.ipynb      # Phase 4: ML Models
│   ├── 05_deep_learning.ipynb         # Phase 5: Deep Learning
│   └── 06_evaluation.ipynb           # Phase 6: Evaluation & Report
│
└── src/
    ├── __init__.py
    ├── db_utils.py                    # Database connection helpers
    ├── preprocessing.py               # Preprocessing functions
    └── evaluation.py                  # Evaluation & plotting helpers
```

---

## 📏 Grading Rubric

| Component | Weight | Description |
|---|---|---|
| **PostgreSQL & pgAdmin Setup** | 10% | Database created, tables populated, SQL queries work |
| **Data Loading** | 10% | Correct SQL joins, clean DataFrame output |
| **EDA** | 20% | Quality of visualizations, depth of insights |
| **Feature Engineering** | 15% | Proper encoding, scaling, feature creation |
| **Machine Learning** | 20% | Model training, tuning, feature importance |
| **Deep Learning** | 15% | Neural network design, training, evaluation |
| **GitHub & Code Quality** | 10% | Clean commits, proper branching, documentation |

---

## 📚 Useful Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [TensorFlow/Keras Tutorials](https://www.tensorflow.org/tutorials)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [Seaborn Gallery](https://seaborn.pydata.org/examples/index.html)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

---

## ❓ Need Help?

- Review the course materials from the training
- Check the resources linked above
- Ask your instructor during office hours
- Collaborate with classmates (but submit your own work!)

---

**Good luck! 🚀 Show us what you've learned!**
