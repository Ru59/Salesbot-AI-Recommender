# Salesbot-AI-Recommender
Data-driven retail product recommendation system.
# 🤖 SalesBot — Retail Product Recommendation System

An interactive product recommendation system built with Python, Pandas, Scikit-learn and Streamlit.

SalesBot analyzes historical retail transaction data to identify products that are frequently purchased together and generates product recommendations based on observed purchasing patterns.

## 🚀 Live Demo

[Launch SalesBot](https://salesbot-ai-recommender-gabnkrdatikfq6duap8nuw.streamlit.app/)

## 🎯 Project Objective

The goal of this project is to demonstrate how historical retail transaction data can be transformed into a practical recommendation system.

The system answers a simple business question:

> "Customers who purchased this product also purchased what?"

This type of recommendation can support e-commerce businesses with:

- Cross-selling
- Product discovery
- Personalized recommendations
- Increasing basket size
- Understanding customer purchasing patterns

## 🧠 How SalesBot Works

The application follows this workflow:

1. Load historical retail transaction data.
2. Clean and prepare the transaction data.
3. Group products by customer transactions.
4. Identify products frequently purchased together.
5. Calculate recommendation strength based on historical purchase patterns.
6. Return the most relevant product recommendations.
7. Display the results through an interactive Streamlit application.

### Example

When a user selects:

**10 COLOUR SPACEBOY PEN**

SalesBot can identify products that were repeatedly purchased in the same transactions.

Example recommendation:

**PLASTERS IN TIN SPACEBOY**

- Bought together: 50 times
- Recommendation confidence: 20.66%

## 📊 Dataset

The project uses historical online retail transaction data containing information such as:

- Invoice numbers
- Product codes
- Product descriptions
- Quantities
- Transaction dates
- Customer IDs

The data is used to discover purchasing relationships between products.

## 🛠️ Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- GitHub

## 💡 Key Skills Demonstrated

This project demonstrates practical experience with:

- Data cleaning
- Data preprocessing
- Exploratory data analysis
- Transaction data analysis
- Recommendation systems
- Pattern identification
- Python programming
- Pandas
- Scikit-learn
- Streamlit application development
- GitHub
- Application deployment

## 🖥️ Application

SalesBot provides an interactive interface where users can:

1. Select a product.
2. Request recommendations.
3. View products frequently purchased together.
4. See purchase frequency.
5. View recommendation confidence.

## 📁 Project Structure

app.py

Contains the Streamlit application and user interface.

recommender.py

Contains the recommendation logic used to analyze purchasing relationships and generate recommendations.

SalesBot_Data.csv

Contains the retail transaction data used by the recommendation system.

requirements.txt

Contains the Python dependencies required to run the project.

📌 Project Outcome

SalesBot demonstrates how transaction-level retail data can be converted into an interactive recommendation tool.

Rather than simply analyzing historical sales, the project turns purchasing patterns into recommendations that could be used in an e-commerce environment.

👩🏽‍💻 Author

Sisipho Ruth Ngange

Aspiring Data Analyst / Data Scientist

LinkedIn:
https://www.linkedin.com/in/sisipho-ruth-ngange-538312430/
