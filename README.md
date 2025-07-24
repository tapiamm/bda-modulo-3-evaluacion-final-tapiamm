# ✈️ Customer Data & Flight Activity Analysis

This project involves data exploration, cleaning, visualization, and statistical analysis on a dataset of customers from a flight loyalty program. The goal is to better understand customer behavior and characteristics, and to answer key business questions using Python tools.

---

## 🧰 Custom ETL Functions

To keep the code organized and reusable, a `.py` file called `etl_funciones.py` was created. It contains specific functions for the ETL process, such as:

- Data cleaning
- Null value handling
- Data type conversions
- Merging tables
- Saving data in different formats

These functions allowed efficient and consistent processing during the exploratory and analytical phases.

---

## 📂 Dataset Overview

Two CSV files were merged into a single DataFrame called `customer_info`, which includes:

- Customer demographic data  
- Flight history  
- Earned and redeemed loyalty points  
- Type of loyalty card and signup details  

---

## 🔍 Phase 1: Data Exploration & Cleaning

### 🧭 Initial Exploration
- Detected null values (e.g., cancellation date)
- Found duplicates (one record per customer per month)
- Used `info()`, `describe()`, and `value_counts()` to evaluate data quality and structure

### 🧹 Cleaning
- Handled nulls based on relevance
- Grouped by Loyalty Number to remove duplicates for customer-level analysis
- Converted columns to efficient types like `category` or `Int64` for optimization

---

## 📊 Phase 2: Visualization & Analysis

Visualizations were created with `matplotlib` and `seaborn` to answer the following key questions:

### 📅 How are bookings distributed across months?
- Grouped by booking month  
- Bar plot to identify trends and seasonality

### ✈️ Is there a relationship between flight distance and loyalty points?
- Aggregated data per customer  
- Scatter plot with regression line showing a positive correlation

### 🗺️ Customer distribution by province
- Unique customers grouped by province  
- Count plot sorted by frequency

### 💸 Average salary by education level
- Salaries grouped by education  
- Bar and box plots to compare means and variation

### 💳 Loyalty card type proportions
- Pie chart showing distribution by card type

### ❤️ Distribution by marital status and gender
- Grouped bar plot (`hue='Gender'`) to visually compare categories

---

## 🎓 BONUS: Statistical Evaluation by Education Level

### 🎯 Goal:
Test whether there are significant differences in flight bookings by education level.

#### 1️⃣ Data Prep
- Aggregated monthly bookings per customer  
- Filtered relevant columns: `Flights Booked` and `Education`

#### 2️⃣ Descriptive Analysis
- Calculated means, standard deviation, and percentiles for each group

#### 3️⃣ Statistical Tests
- **Normality**: Shapiro-Wilk or Kolmogorov-Smirnov → non-normal distribution  
- **Variance Homogeneity**: Not assumed due to lack of normality  
- **Hypothesis Test**: Kruskal-Wallis test showed no significant differences among groups

---

## 🧪 Conclusion

This analysis revealed useful customer behavior patterns. The statistical test confirmed that education level does **not** significantly affect the number of flights booked.  
Marketing strategies can therefore focus on other influential variables like loyalty card type, flight frequency, points earned, or Customer Lifetime Value (CLV). These insights support more effective decision-making in personalization, loyalty programs, and campaign targeting.

---

## 🗂️ Files

- `etl_funciones.py`: Custom ETL functions  
- `flight_analysis.ipynb`: Jupyter Notebook with full analysis  
- `customer_data.csv`: Merged dataset used in the project

---

## 🚀 Next Steps

- Build interactive dashboards in Tableau or Power BI  
- Apply clustering techniques to segment customer types  
- Integrate additional data sources for deeper insights  
- Automate ETL with scheduled Python scripts

---

## 📬 Contact

Feel free to reach out or explore more of my work:

- [LinkedIn](www.linkedin.com/in/maría-tapia-1639b21b4)  
- [GitHub](https://github.com/tapiamm) 

