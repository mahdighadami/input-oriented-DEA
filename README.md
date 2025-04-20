# DEA Efficiency Analyzer 🧮📊

A user-friendly GUI application built with **PyQt5** to compute, visualize, and analyze **Decision Making Units (DMUs)** using **Data Envelopment Analysis (DEA)**. This tool is ideal for operations research, efficiency studies, and productivity analysis.

---

## 🚀 Features

- 📥 **Input-oriented DEA model** (Deterministic)
- 📋 Interactive GUI built with **PyQt5**
- 📈 Visualization of:
  - **Efficiency Scores (θ)**
  - **Resource Waste (1 − θ)** ➖
- 🧠 Automated textual analysis of efficiency results
- 🔄 Navigation system with signal-based back buttons
- 💡 Interpretation section for better understanding of DEA outputs


---

## 🧑‍💻 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/dea-efficiency-analyzer.git
   cd dea-efficiency-analyzer

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

## ✅ Requirements

* Python 3.7+
* PyQt5
* matplotlib
* Install manually with:

```bash
pip install pyqt5 matplotlib
```

## 🧩 Project Structure
```bash
dea-efficiency-analyzer/
├── deterministic.py      # DEA computation logic
├── det_table.py          # GUI input form
├── det_out.py            # Output visualizer with plots and analysis
├── main.py               # Application entry point
├── assets/               # Icons, stylesheets, etc.
├── screenshots/          # Sample plot images
└── README.md
```

## 📊 Model Summary
DEA Type: Input-oriented, deterministic
Efficiency Score (θ): Ratio indicating performance efficiency
Waste (1 − θ): Interpretation of potential resource savings

## ✍️ Authors
Mahdi Ghadami - Ali Assadbeiki
Data Science Master's Students @ Shahid Beheshti University

## 📜 License
This project is licensed under the MIT License – see the LICENSE file for details.

## 🙌 Acknowledgments
* Inspired by real-world efficiency modeling
* Built as part of a course project in Optimization in Data Science
