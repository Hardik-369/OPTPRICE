# 📈 OptiPrice Web App - Streamlit Interface

A beautiful web interface for Black-Scholes option pricing with real-time data visualization and comprehensive Greeks analysis.

## 🌟 Features

### 📊 **Interactive Web Interface**
- Modern, responsive design with Streamlit
- Real-time stock data fetching
- Interactive parameter adjustment
- Professional data visualization

### 🔢 **Option Pricing & Greeks**
- Black-Scholes option pricing model
- Complete Greeks calculation (Delta, Gamma, Theta, Vega, Rho)
- Support for both Call and Put options
- Real-time updates as parameters change

### 📈 **Advanced Visualizations**
- **Payoff Diagrams**: Interactive profit/loss charts
- **Greeks Charts**: Sensitivity analysis across price ranges
- **Price History**: 3-month stock price trends
- **Real-time Metrics**: Current price, volatility, market cap

### 🎛️ **Customizable Parameters**
- Strike price adjustment
- Expiration date (1-365 days)
- Custom volatility override
- Risk-free rate configuration
- Option type selection (Call/Put)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Option 1: Use installer
install_dependencies.bat

# Option 2: Manual installation
pip install -r requirements.txt
```

### 2. Run the Web Application
```bash
# Option 1: Use batch file
run_webapp.bat

# Option 2: Direct command
streamlit run app.py

# Option 3: PowerShell
.\run_webapp.ps1
```

### 3. Access the Application
Open your browser and navigate to: **http://localhost:8501**

## 🖥️ User Interface

### **Sidebar Controls**
- **Stock Ticker Input**: Enter any valid ticker symbol
- **Fetch Data Button**: Retrieve real-time stock information
- **Option Settings**: Configure strike, expiration, volatility
- **Risk Parameters**: Adjust risk-free rate

### **Main Dashboard**
- **Stock Information**: Current price, change, volatility, market cap
- **Option Results**: Theoretical price, moneyness, time value
- **Greeks Display**: All five Greeks with tooltips
- **Interactive Charts**: Payoff diagrams and sensitivity analysis

### **Visualization Tabs**
1. **Payoff Diagram**: Profit/loss visualization
2. **Greeks Chart**: Sensitivity across price ranges
3. **Price History**: Historical stock performance

## 📊 Screenshots & Examples

### Sample Analysis for AAPL:
```
Stock Information:
- Current Price: $213.55
- Historical Volatility: 19.97%
- Market Cap: $3.2T

Option Results:
- Call Option Price: $5.14
- Delta: 0.5286
- Gamma: 0.0325
- Theta: -$0.0900
```

## 🛠️ Technical Details

### **Technology Stack**
- **Frontend**: Streamlit (Python web framework)
- **Data Source**: Yahoo Finance API (yfinance)
- **Calculations**: NumPy, SciPy
- **Visualizations**: Plotly Interactive Charts
- **Caching**: Streamlit's built-in caching (5-minute TTL)

### **Key Features**
- **Real-time Data**: 5-minute cache for stock prices
- **Interactive Charts**: Zoom, pan, hover tooltips
- **Responsive Design**: Works on desktop and tablet
- **Error Handling**: Graceful handling of invalid tickers
- **Performance**: Optimized calculations and caching

### **Supported Platforms**
- Windows (tested)
- macOS (compatible)
- Linux (compatible)
- Any platform with Python 3.7+

## 📁 Project Structure

```
optiprice-streamlit/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── install_dependencies.bat  # Windows installer
├── run_webapp.bat           # Windows launcher
├── run_webapp.ps1           # PowerShell launcher
├── README.md                # This documentation
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── PROJECT_SUMMARY.md       # Quick reference
```

## 🎯 Usage Examples

### **Technology Stocks**
```
AAPL - Apple Inc.
MSFT - Microsoft Corporation
GOOGL - Alphabet Inc.
TSLA - Tesla Inc.
NVDA - NVIDIA Corporation
```

### **Financial Stocks**
```
JPM - JPMorgan Chase
BAC - Bank of America
WFC - Wells Fargo
GS - Goldman Sachs
MS - Morgan Stanley
```

### **Market Indices**
```
SPY - S&P 500 ETF
QQQ - NASDAQ 100 ETF
IWM - Russell 2000 ETF
```

## ⚙️ Configuration

### **Streamlit Settings** (`.streamlit/config.toml`)
- Port: 8501 (default)
- Theme: Custom OptiPrice theme
- Auto-reload: Enabled for development

### **Cache Settings**
- Stock data: 5-minute cache
- Charts: Real-time generation
- Performance: Optimized for responsiveness

## 🔧 Troubleshooting

### **Common Issues**

1. **"Module not found" error**
   ```bash
   pip install -r requirements.txt
   ```

2. **Port already in use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

3. **Stock data not loading**
   - Check internet connection
   - Verify ticker symbol is correct
   - Try refreshing the page

### **Performance Tips**
- Use valid ticker symbols for faster loading
- Historical volatility updates every 5 minutes
- Clear browser cache if experiencing issues

## 🔄 Updates & Extensions

### **Planned Features**
- [ ] Options chain comparison
- [ ] Implied volatility surface
- [ ] Portfolio Greeks aggregation
- [ ] Export functionality (PDF/CSV)
- [ ] More option strategies

### **Customization**
The web app is highly customizable. You can:
- Modify themes in `.streamlit/config.toml`
- Add new visualizations in `app.py`
- Extend calculations for new Greeks
- Add support for exotic options

## 📞 Support

For issues or questions:
1. Check this README for common solutions
2. Verify all dependencies are installed
3. Ensure Python 3.7+ is installed
4. Check firewall settings for port 8501

---

**Created**: July 2025  
**Version**: 1.0  
**Framework**: Streamlit  
**License**: Open Source  

Enjoy real-time option pricing with OptiPrice! 🚀
