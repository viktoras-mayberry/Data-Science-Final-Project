# 📤 Submission Guide

Follow these steps to submit your completed project using Git and GitHub.

---

## Step 1: Fork the Repository

1. Go to the project repository on GitHub.
2. Click the **Fork** button (top-right corner).
3. This creates a copy of the repository under your own GitHub account.

---

## Step 2: Clone Your Fork

```bash
git clone https://github.com/<your-username>/data-science-final-project.git
cd data-science-final-project
```

---

## Step 3: Create a Branch

Create a new branch for your work. Use your name as the branch name:

```bash
git checkout -b submission/<your-firstname-lastname>

# Example:
git checkout -b submission/john-doe
```

---

## Step 4: Complete the Project

- Work through all 6 notebooks in order
- Fill in all TODO sections
- Run all cells to ensure outputs are displayed
- Write your insights and analysis in the markdown cells

---

## Step 5: Commit Your Changes

Make regular commits as you work (not just one big commit at the end):

```bash
# Stage your changes
git add .

# Commit with a meaningful message
git commit -m "Complete Phase 1: Data loading and SQL queries"

# Continue working...
git add .
git commit -m "Complete Phase 2: EDA visualizations and insights"
```

### Commit Message Guidelines

Write clear, descriptive commit messages:
- ✅ `"Add EDA visualizations for churn analysis"`
- ✅ `"Implement Random Forest model with hyperparameter tuning"`
- ❌ `"update"`
- ❌ `"done"`
- ❌ `"asdfgh"`

---

## Step 6: Push to GitHub

```bash
git push origin submission/<your-firstname-lastname>
```

---

## Step 7: Create a Pull Request

1. Go to your forked repository on GitHub.
2. You will see a banner: **"submission/your-name had recent pushes"** → Click **Compare & pull request**.
3. Set the **base repository** to the original class repository.
4. Set the **base branch** to `main`.
5. Title your PR: `Submission: <Your Full Name>`
6. In the description, write a brief summary of your project:
   - Any interesting findings from EDA
   - Which ML model performed best and why
   - Challenges you faced and how you solved them
7. Click **Create pull request**.

---

## ⚠️ Important Reminders

- **Do NOT** commit your `.env` file (it is already in `.gitignore`).
- **Do NOT** commit the raw CSV dataset (it is already in `.gitignore`).
- **DO** make sure all notebook cells have been **run** so that outputs (charts, tables, metrics) are visible.
- **DO** include your analysis and insights in the markdown cells — not just code.
- **Deadline:** Check with your instructor for the submission deadline.

---

## 📋 Submission Checklist

Before submitting, verify the following:

- [ ] All 6 notebooks are completed with code AND markdown analysis
- [ ] All notebook cells have been executed (outputs are visible)
- [ ] PostgreSQL database was set up and used for data loading
- [ ] At least 3 ML models were trained and compared
- [ ] A deep learning model was built and evaluated
- [ ] Commits are clean and descriptive (not just one giant commit)
- [ ] Pull request is created with a proper title and summary
- [ ] No credentials or sensitive data are committed
- [ ] Code is clean and well-commented

---

**Good luck with your submission! 🎉**
