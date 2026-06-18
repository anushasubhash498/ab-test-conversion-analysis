# A/B Testing & Product Conversion Optimization Case Study

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![scipy](https://img.shields.io/badge/scipy-latest-navy.svg)](https://scipy.org/)
[![Chart.js](https://img.shields.io/badge/Chart.js-Dashboard-magenta.svg)](https://www.chartjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end Conversion Rate Optimization (CRO) statistical analysis case study. This project implements a Python-based experiment analyzer that processes user traffic logs, performs standard hypothesis tests (two-proportion z-test, confidence intervals, power analysis), and displays findings on a premium interactive glassmorphism dashboard.

---

## 🧪 Experiment Overview & Results

The experiment ran for **30 days** with a **50/50 split** cohort of **10,000 users** to test an optimized checkout landing page (Treatment) against the legacy design (Control).

* **Control Group (Old Page)**: **5,000 users** with **601 conversions** (**12.02% CR**).
* **Treatment Group (New Page)**: **5,000 users** with **695 conversions** (**13.90% CR**).
* **Absolute Lift**: **+1.88%**
* **Relative Improvement**: **+15.64%**

---

## 📊 Statistical Validation Summary

- **Hypothesis Definition**:
  - **Null Hypothesis ($H_0$)**: The conversion rate of the new page is equal to or less than the old page ($p_{new} \le p_{old}$).
  - **Alternative Hypothesis ($H_1$)**: The conversion rate of the new page is greater than the old page ($p_{new} > p_{old}$).
- **Z-Score**: **2.777** (Critical boundary is **1.645** for one-tailed $\alpha = 0.05$).
- **P-Value**: **0.0055** (Highly significant, $p < 0.05$).
- **95% Confidence Interval (CI) for Difference**: **[+0.52%, +2.98%]** (Since the range is strictly positive and excludes 0, we confirm a true positive lift).
- **Statistical Power**: **82.4%** (Exceeds the industry standard benchmark of 80%, indicating a low probability of a Type II error / false negative).

**Verdict**: **Reject the Null Hypothesis ($H_0$)**. Roll out the new landing page design to 100% of traffic.

---

## 📱 Device Segment Insights

| Device Group | Control CR (%) | Treatment CR (%) | Relative Lift (%) | Status |
|---|---|---|---|---|
| **Desktop** | 12.4% | 14.5% | +16.9% | ✅ Significant |
| **Mobile** | 11.5% | 13.2% | +14.8% | ✅ Significant |
| **Tablet** | 11.9% | 13.8% | +16.0% | ⚠️ Underpowered (low sample size) |

---

## 💻 Tech Stack & Tools

- **Statistical Analysis**: `Python 3`, `scipy.stats`
- **Data Engineering**: `pandas`, `numpy`
- **Visual Exploration**: `matplotlib`, `seaborn`
- **Presentation Layer**: `HTML5`, `CSS3 (Glassmorphic Elements)`, `JavaScript`, `Chart.js`

---

## 📂 Project Structure

```text
ab-test-conversion-analysis/
├── data/
│   ├── generate_data.py        # Generates synthetic A/B test logs
│   └── ab_test_data.csv        # Log of 10,000 experiment users
├── notebooks/
│   └── ab_test_analysis.py     # Python script carrying out hypothesis testing
├── outputs/
│   ├── conversion_rate_comparison.png
│   ├── cumulative_conversion_rate.png
│   └── device_segmentation.png
├── dashboard/
│   └── index.html              # Interactive CRO analytics dashboard
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run Locally

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/anushasubhash498/ab-test-conversion-analysis.git
cd ab-test-conversion-analysis

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Data Pipeline & Statistical Engine
```bash
# Generate user interaction datasets
python data/generate_data.py

# Execute Z-Test and generate charts
python notebooks/ab_test_analysis.py
```

### 3. Review dashboard
Open `dashboard/index.html` in any web browser to view the interactive experiment report with cumulative stability lines.

---

## 👤 About the Author
**Anusha Subhash**  
Candidate for **Data Analyst** and **Business Analyst** positions in Berlin.  
BSc in Computer Science & Digitisation.  
Experienced with SQL database management, Tableau visualization, and statistical programming in Python.
