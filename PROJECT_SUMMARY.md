# 📈 OptiPrice Streamlit Web App - Project Summary

## 🌐 Web Interface for Black-Scholes Option Pricing

A modern, interactive web application built with Streamlit that provides real-time option pricing and Greeks analysis.

### 📦 Project Contents

- **`app.py`** - Main Streamlit web application (15KB)
- **`requirements.txt`** - Python dependencies
- **`README.md`** - Comprehensive documentation
- **`install_dependencies.bat`** - Windows dependency installer
- **`run_webapp.bat`** - Windows web app launcher
- **`run_webapp.ps1`** - PowerShell launcher script
- **`.streamlit/config.toml`** - Streamlit configuration
- **`PROJECT_SUMMARY.md`** - This summary

### 🚀 Quick Launch

#### **1-Click Setup**
```bash
# Install dependencies
install_dependencies.bat

# Launch web app
run_webapp.bat
```

#### **Access the App**
Open browser → **http://localhost:8501**

### ✨ Key Features

#### **📊 Interactive Interface**
- Modern Streamlit design
- Real-time parameter adjustment
- Sidebar controls
- Responsive layout

#### **📈 Advanced Visualizations**
- **Payoff Diagrams** - Profit/loss visualization
- **Greeks Charts** - Sensitivity analysis
- **Price History** - 3-month stock trends
- **Interactive Metrics** - Hover tooltips

#### **🔢 Complete Option Analysis**
- Black-Scholes pricing
- All Greeks (Delta, Gamma, Theta, Vega, Rho)
- Call and Put options
- Real-time calculations

#### **🎛️ Customizable Parameters**
- Strike price adjustment
- Expiration (1-365 days)
- Custom volatility
- Risk-free rate
- Option type selection

### 🔧 Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Data**: Yahoo Finance API (yfinance)
- **Math**: NumPy, SciPy
- **Charts**: Plotly interactive visualizations
- **Performance**: 5-minute data caching

### 📊 Sample Interface Flow

1. **Enter Ticker** → AAPL, MSFT, GOOGL, etc.
2. **Fetch Data** → Real-time price & volatility
3. **Adjust Parameters** → Strike, expiration, volatility
4. **View Results** → Option price + Greeks
5. **Analyze Charts** → Payoff diagrams & sensitivity

### 💻 Usage Examples

#### **Technology Stocks**
- AAPL (Apple) - $213.55 → Call: $5.14
- MSFT (Microsoft) - $498.84 → Call: $7.75
- GOOGL (Google) - $179.53 → Call: $5.79

#### **High Volatility Stocks**
- TSLA (Tesla) - 76.64% vol → Premium: $27.94

### 🎯 Perfect For

- **Traders**: Real-time option pricing
- **Students**: Learning Black-Scholes model
- **Analysts**: Greeks sensitivity analysis
- **Researchers**: Option strategy development

### 🔄 How It Works

1. **Data Fetching**: Gets real-time stock prices via yfinance
2. **Volatility Calculation**: 1-month historical volatility
3. **Black-Scholes**: Applies classic option pricing formula
4. **Greeks**: Calculates all sensitivity measures
5. **Visualization**: Creates interactive charts
6. **Caching**: Optimizes performance with 5-min cache

### 🌟 Advantages over CLI Version

| Feature | CLI App | Web App |
|---------|---------|---------|
| Interface | Command line | Beautiful web UI |
| Visualization | Text only | Interactive charts |
| Parameters | Fixed | Real-time adjustment |
| Charts | None | Payoff + Greeks diagrams |
| Usability | Technical users | Everyone |
| Sharing | Screenshots | Live web link |

### 🚀 Installation & Launch

#### **Method 1: One-Click**
1. Double-click `install_dependencies.bat`
2. Double-click `run_webapp.bat`
3. Browser opens automatically

#### **Method 2: Manual**
```bash
pip install -r requirements.txt
streamlit run app.py
```

#### **Method 3: PowerShell**
```powershell
.\run_webapp.ps1
```

### 📱 Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- 📱 Mobile responsive

### 🔧 Configuration

The app includes optimized settings:
- Port: 8501 (customizable)
- Theme: Professional red/white
- Auto-reload: Enabled
- Caching: 5-minute TTL
- Performance: Optimized

### 📊 Performance Features

- **Smart Caching**: Stock data cached for 5 minutes
- **Lazy Loading**: Charts generated on-demand
- **Optimized Calculations**: Vectorized NumPy operations
- **Responsive UI**: Real-time parameter updates

---

## 🎉 Ready to Use!

The OptiPrice Streamlit web app is a professional-grade option pricing tool that transforms the command-line application into a beautiful, interactive web interface. Perfect for trading, education, and analysis.

**Launch the app and start analyzing options in seconds!** 🚀
