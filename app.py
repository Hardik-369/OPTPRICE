import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="OptiPrice - Option Pricing Calculator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

class BlackScholesCalculator:
    """Black-Scholes option pricing calculator with Greeks"""
    
    def __init__(self, S, K, T, r, sigma, option_type='call'):
        """
        Initialize the Black-Scholes calculator
        
        Args:
            S (float): Current stock price
            K (float): Strike price
            T (float): Time to expiration (in years)
            r (float): Risk-free rate
            sigma (float): Volatility (annualized)
            option_type (str): 'call' or 'put'
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()
        
        # Calculate d1 and d2
        if T > 0 and sigma > 0:
            self.d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            self.d2 = self.d1 - sigma * np.sqrt(T)
        else:
            self.d1 = 0
            self.d2 = 0
    
    def option_price(self):
        """Calculate the Black-Scholes option price"""
        if self.T <= 0:
            if self.option_type == 'call':
                return max(0, self.S - self.K)
            else:
                return max(0, self.K - self.S)
        
        if self.option_type == 'call':
            price = (self.S * norm.cdf(self.d1) - 
                    self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2))
        else:  # put
            price = (self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - 
                    self.S * norm.cdf(-self.d1))
        return price
    
    def delta(self):
        """Calculate Delta - price sensitivity to underlying price"""
        if self.T <= 0:
            if self.option_type == 'call':
                return 1.0 if self.S > self.K else 0.0
            else:
                return -1.0 if self.S < self.K else 0.0
        
        if self.option_type == 'call':
            return norm.cdf(self.d1)
        else:  # put
            return norm.cdf(self.d1) - 1
    
    def gamma(self):
        """Calculate Gamma - rate of change of Delta"""
        if self.T <= 0 or self.sigma <= 0:
            return 0
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))
    
    def theta(self):
        """Calculate Theta - time decay (per day)"""
        if self.T <= 0:
            return 0
        
        if self.option_type == 'call':
            theta = (-(self.S * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T)) -
                    self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2))
        else:  # put
            theta = (-(self.S * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T)) +
                    self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2))
        return theta / 365  # Convert to per day
    
    def vega(self):
        """Calculate Vega - sensitivity to volatility"""
        if self.T <= 0:
            return 0
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) / 100  # Per 1% change in volatility
    
    def rho(self):
        """Calculate Rho - sensitivity to interest rate"""
        if self.T <= 0:
            return 0
        
        if self.option_type == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) / 100
        else:  # put
            return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2) / 100

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_stock_data(ticker):
    """
    Fetch stock data and calculate required parameters
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        tuple: (current_price, volatility, stock_info) or (None, None, None) if error
    """
    try:
        # Create yfinance ticker object
        stock = yf.Ticker(ticker)
        
        # Get current stock price
        info = stock.info
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        
        if current_price is None:
            # Try getting from recent data
            hist = stock.history(period='2d')
            if hist.empty:
                return None, None, None
            current_price = hist['Close'].iloc[-1]
        
        # Get 1 month of historical data for volatility calculation
        hist_data = stock.history(period='1mo')
        if hist_data.empty or len(hist_data) < 10:
            return None, None, None
        
        # Calculate daily returns
        daily_returns = hist_data['Close'].pct_change().dropna()
        
        # Calculate annualized volatility
        daily_volatility = daily_returns.std()
        annualized_volatility = daily_volatility * np.sqrt(252)  # 252 trading days per year
        
        # Get additional stock info
        stock_info = {
            'name': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'previous_close': info.get('previousClose', current_price),
            'currency': info.get('currency', 'USD')
        }
        
        return current_price, annualized_volatility, stock_info
        
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None, None, None

def create_payoff_diagram(S, K, option_price, option_type, current_price):
    """Create option payoff diagram"""
    # Create range of stock prices
    price_range = np.linspace(S * 0.7, S * 1.3, 100)
    
    if option_type.lower() == 'call':
        # Call option payoff
        payoff = np.maximum(price_range - K, 0) - option_price
        intrinsic = np.maximum(price_range - K, 0)
    else:
        # Put option payoff
        payoff = np.maximum(K - price_range, 0) - option_price
        intrinsic = np.maximum(K - price_range, 0)
    
    fig = go.Figure()
    
    # Add payoff line
    fig.add_trace(go.Scatter(
        x=price_range,
        y=payoff,
        mode='lines',
        name=f'{option_type.title()} Payoff',
        line=dict(color='blue', width=3)
    ))
    
    # Add intrinsic value line
    fig.add_trace(go.Scatter(
        x=price_range,
        y=intrinsic,
        mode='lines',
        name='Intrinsic Value',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # Add break-even line
    fig.add_hline(y=0, line_dash="dot", line_color="gray", 
                  annotation_text="Break-even")
    
    # Add current stock price line
    fig.add_vline(x=current_price, line_dash="dot", line_color="green",
                  annotation_text=f"Current Price: ${current_price:.2f}")
    
    fig.update_layout(
        title=f'{option_type.title()} Option Payoff Diagram',
        xaxis_title='Stock Price ($)',
        yaxis_title='Profit/Loss ($)',
        hovermode='x unified',
        showlegend=True,
        height=400
    )
    
    return fig

def create_greeks_chart(S, K, T, r, sigma, option_type):
    """Create Greeks visualization"""
    # Create range of stock prices around current price
    price_range = np.linspace(S * 0.8, S * 1.2, 50)
    
    deltas = []
    gammas = []
    thetas = []
    vegas = []
    
    for price in price_range:
        bs = BlackScholesCalculator(price, K, T, r, sigma, option_type)
        deltas.append(bs.delta())
        gammas.append(bs.gamma())
        thetas.append(bs.theta())
        vegas.append(bs.vega())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=price_range, y=deltas, name='Delta', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=price_range, y=gammas, name='Gamma', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=price_range, y=thetas, name='Theta', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=price_range, y=vegas, name='Vega', line=dict(color='orange')))
    
    # Add current stock price line
    fig.add_vline(x=S, line_dash="dot", line_color="gray",
                  annotation_text=f"Current: ${S:.2f}")
    
    fig.update_layout(
        title='Greeks vs Stock Price',
        xaxis_title='Stock Price ($)',
        yaxis_title='Greek Value',
        hovermode='x unified',
        height=400
    )
    
    return fig

def main():
    # Header
    st.title("📈 OptiPrice - Black-Scholes Option Pricing Calculator")
    st.markdown("*Real-time option pricing with comprehensive Greeks analysis*")
    
    # Sidebar for inputs
    st.sidebar.header("🔧 Option Parameters")
    
    # Stock ticker input
    ticker = st.sidebar.text_input(
        "Stock Ticker Symbol", 
        value="AAPL", 
        help="Enter a valid stock ticker (e.g., AAPL, MSFT, GOOGL)"
    ).upper()
    
    # Fetch stock data button
    if st.sidebar.button("📊 Fetch Stock Data", type="primary"):
        if ticker:
            with st.spinner(f"Fetching data for {ticker}..."):
                current_price, volatility, stock_info = get_stock_data(ticker)
                
                if current_price is not None:
                    st.session_state['stock_data'] = {
                        'ticker': ticker,
                        'current_price': current_price,
                        'volatility': volatility,
                        'stock_info': stock_info
                    }
                    st.sidebar.success("✅ Data fetched successfully!")
                else:
                    st.sidebar.error("❌ Failed to fetch stock data. Please check the ticker symbol.")
    
    # Check if we have stock data
    if 'stock_data' not in st.session_state:
        st.info("👆 Please enter a ticker symbol and click 'Fetch Stock Data' to begin analysis.")
        return
    
    stock_data = st.session_state['stock_data']
    current_price = stock_data['current_price']
    historical_volatility = stock_data['volatility']
    stock_info = stock_data['stock_info']
    
    # Display stock info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", f"${current_price:.2f}")
    with col2:
        change = current_price - stock_info['previous_close']
        st.metric("Price Change", f"${change:.2f}", f"{change:.2f}")
    with col3:
        st.metric("Historical Vol", f"{historical_volatility:.2%}")
    with col4:
        if stock_info['market_cap'] > 0:
            market_cap = stock_info['market_cap'] / 1e9  # Convert to billions
            st.metric("Market Cap", f"${market_cap:.1f}B")
    
    st.markdown(f"**{stock_info['name']}** | Sector: {stock_info['sector']}")
    
    # Option parameters
    st.sidebar.subheader("Option Settings")
    
    option_type = st.sidebar.selectbox(
        "Option Type",
        ["Call", "Put"],
        help="Select the type of option"
    )
    
    # Strike price (default to ATM)
    strike_price = st.sidebar.number_input(
        "Strike Price ($)",
        min_value=0.01,
        value=float(current_price),
        step=0.01,
        help="Option strike price (default: at-the-money)"
    )
    
    # Days to expiration
    days_to_expiry = st.sidebar.slider(
        "Days to Expiration",
        min_value=1,
        max_value=365,
        value=30,
        help="Number of days until option expiration"
    )
    
    # Volatility (can override historical)
    use_custom_vol = st.sidebar.checkbox("Use Custom Volatility")
    if use_custom_vol:
        volatility = st.sidebar.slider(
            "Volatility (Annual %)",
            min_value=1.0,
            max_value=200.0,
            value=float(historical_volatility * 100),
            step=1.0,
            help="Custom volatility as a percentage"
        ) / 100
    else:
        volatility = historical_volatility
        st.sidebar.info(f"Using historical volatility: {volatility:.2%}")
    
    # Risk-free rate
    risk_free_rate = st.sidebar.slider(
        "Risk-free Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=3.0,
        step=0.1,
        help="Risk-free interest rate"
    ) / 100
    
    # Calculate option price and Greeks
    time_to_expiry = days_to_expiry / 365.0
    
    bs_calc = BlackScholesCalculator(
        S=current_price,
        K=strike_price,
        T=time_to_expiry,
        r=risk_free_rate,
        sigma=volatility,
        option_type=option_type.lower()
    )
    
    option_price = bs_calc.option_price()
    delta = bs_calc.delta()
    gamma = bs_calc.gamma()
    theta = bs_calc.theta()
    vega = bs_calc.vega()
    rho = bs_calc.rho()
    
    # Main results
    st.header("📊 Option Pricing Results")
    
    # Option price and key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Option Price",
            f"${option_price:.2f}",
            help="Black-Scholes theoretical option price"
        )
    with col2:
        moneyness = "ITM" if (option_type == "Call" and current_price > strike_price) or (option_type == "Put" and current_price < strike_price) else "OTM"
        if abs(current_price - strike_price) / current_price < 0.02:
            moneyness = "ATM"
        st.metric("Moneyness", moneyness)
    with col3:
        intrinsic = max(0, current_price - strike_price) if option_type == "Call" else max(0, strike_price - current_price)
        time_value = option_price - intrinsic
        st.metric("Time Value", f"${time_value:.2f}")
    
    # Greeks display
    st.subheader("🔢 The Greeks")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Delta", f"{delta:.4f}", help="Price sensitivity to underlying")
    with col2:
        st.metric("Gamma", f"{gamma:.4f}", help="Rate of change of Delta")
    with col3:
        st.metric("Theta", f"${theta:.4f}", help="Time decay per day")
    with col4:
        st.metric("Vega", f"${vega:.4f}", help="Volatility sensitivity")
    with col5:
        st.metric("Rho", f"${rho:.4f}", help="Interest rate sensitivity")
    
    # Visualizations
    st.header("📈 Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["Payoff Diagram", "Greeks Chart", "Price History"])
    
    with tab1:
        payoff_fig = create_payoff_diagram(current_price, strike_price, option_price, option_type, current_price)
        st.plotly_chart(payoff_fig, use_container_width=True)
    
    with tab2:
        greeks_fig = create_greeks_chart(current_price, strike_price, time_to_expiry, risk_free_rate, volatility, option_type.lower())
        st.plotly_chart(greeks_fig, use_container_width=True)
    
    with tab3:
        # Stock price history
        with st.spinner("Loading price history..."):
            stock = yf.Ticker(ticker)
            hist_data = stock.history(period='3mo')
            
            if not hist_data.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=hist_data.index,
                    y=hist_data['Close'],
                    mode='lines',
                    name='Stock Price',
                    line=dict(color='blue')
                ))
                
                # Add strike price line
                fig.add_hline(y=strike_price, line_dash="dash", line_color="red",
                             annotation_text=f"Strike: ${strike_price:.2f}")
                
                fig.update_layout(
                    title=f'{ticker} Price History (3 Months)',
                    xaxis_title='Date',
                    yaxis_title='Price ($)',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Could not load price history")
    
    # Summary table
    st.header("📋 Summary")
    
    summary_data = {
        'Parameter': ['Stock Price', 'Strike Price', 'Time to Expiry', 'Volatility', 'Risk-free Rate', 'Option Type'],
        'Value': [f'${current_price:.2f}', f'${strike_price:.2f}', f'{days_to_expiry} days', f'{volatility:.2%}', f'{risk_free_rate:.2%}', option_type]
    }
    
    results_data = {
        'Metric': ['Option Price', 'Delta', 'Gamma', 'Theta', 'Vega', 'Rho'],
        'Value': [f'${option_price:.2f}', f'{delta:.4f}', f'{gamma:.4f}', f'${theta:.4f}', f'${vega:.4f}', f'${rho:.4f}']
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Input Parameters")
        st.dataframe(pd.DataFrame(summary_data), hide_index=True)
    
    with col2:
        st.subheader("Calculated Results")
        st.dataframe(pd.DataFrame(results_data), hide_index=True)

if __name__ == "__main__":
    main()
