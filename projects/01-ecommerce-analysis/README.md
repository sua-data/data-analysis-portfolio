# 🐶 E-commerce Sales Data Analysis

## 📌 Project Overview

This project analyzes e-commerce sales data using **Python, Pandas, and MySQL**.
The goal is to understand product sales performance and identify key revenue drivers.

## 📊 Dataset

The dataset contains order transaction data from an e-commerce store.

| Column       | Description        |
| ------------ | ------------------ |
| order_id     | Order ID           |
| order_date   | Date of order      |
| product_name | Product name       |
| price        | Product price      |
| quantity     | Quantity purchased |
| sales        | Total sales amount |

Sales column was calculated as:

sales = price × quantity

---

## 🛠 Tech Stack

* Python
* Pandas
* MySQL
* Matplotlib
* Jupyter Notebook

---

## 📈 Analysis Process

### 1️⃣ Data Import

Load data from MySQL database using pandas.

### 2️⃣ Data Cleaning

Create sales column and check data structure.

### 3️⃣ Exploratory Data Analysis (EDA)

Key analysis performed:

* Product sales frequency
* Total sales by product
* Sales distribution
* Sales visualization

---

## 📊 Key Insights

* **Dog Snack** generated the highest total revenue.
* Snack products showed higher purchase frequency.
* Some products have higher price but lower sales volume.

---

## 📉 Visualization

Example visualization:

Sales by product

(bar chart generated using matplotlib)

---

## 📂 Project Structure

```
data-analysis-portfolio
│
├─ projects
│   └─ 01-ecommerce-analysis
│       ├─ analysis.ipynb
│       └─ README.md
```

---

## 🚀 Future Improvements

* Monthly sales trend analysis
* Customer segmentation
* Product recommendation analysis
