# 📊 Tunisian Stock Market — Portfolio Optimization Agent

A web application for **portfolio optimization on the Tunisian stock market (BVMT)**, built with Django and Plotly. The app scrapes real stock data from [bvmt.com.tn](https://www.bvmt.com.tn), applies **Markowitz Mean-Variance optimization** to compute optimal asset allocations, and presents the results through interactive charts.

---

## 🇹🇳 Context

The **Bourse des Valeurs Mobilières de Tunis (BVMT)** is a frontier market with limited tooling for quantitative portfolio analysis. This project brings Modern Portfolio Theory to Tunisian equities — computing the efficient frontier, minimizing risk for a given return target, and suggesting optimal stock weightings directly from live market data.

---

## ✨ Features

- **Live data scraping** from bvmt.com.tn (Tunindex-listed stocks)
- **Markowitz Mean-Variance optimization** — computes the efficient frontier
- **Minimum variance portfolio** and **maximum Sharpe ratio portfolio**
- **Interactive Plotly charts** — efficient frontier, asset allocation pie chart, correlation heatmap
- **Django web interface** — clean UI to select assets, set constraints, and visualize results

---

## 🗂️ Project Structure

```
trading-agent/
├── core/                   # Portfolio optimization logic (Markowitz, data processing)
├── data/                   # Scraped BVMT stock price data
├── django_plotly/          # Django app (views, URLs, templates)
├── staticfiles/            # CSS, JS, frontend assets
├── manage.py               # Django entry point
└── requirements.txt        # Python dependencies
```

---

## ⚙️ How It Works

1. **Data Collection** — stock price history is scraped from bvmt.com.tn and stored in `data/`
2. **Return & Risk Computation** — daily returns, annualized mean returns, and covariance matrix are calculated
3. **Optimization** — `scipy.optimize` is used to solve the Markowitz quadratic program:
   - Minimize portfolio variance subject to a target return
   - Sweep across return targets to trace the **efficient frontier**
4. **Visualization** — results are rendered as interactive Plotly charts embedded in the Django views

---

## 🚀 Getting Started

```bash
git clone https://github.com/MedAmirSoltani/trading-agent.git
cd trading-agent
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Optimization | NumPy, SciPy (`minimize`) |
| Data Processing | Pandas |
| Visualization | Plotly (django-plotly-dash or direct embed) |
| Data Source | Scraped from bvmt.com.tn |
| Frontend | HTML / CSS / JavaScript |

---

## 📈 Portfolio Theory — Key Concepts

- **Efficient Frontier** — the set of portfolios offering maximum return for a given level of risk
- **Minimum Variance Portfolio** — lowest possible volatility across all asset combinations
- **Sharpe Ratio** — risk-adjusted return; maximized to find the optimal market portfolio
- **Covariance Matrix** — captures how BVMT stocks move relative to each other

---

## 👤 Author

**Mohamed Amir Soltani**  
AI Engineer | MS Big Data — UTT  
[GitHub](https://github.com/MedAmirSoltani)
