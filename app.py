import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import requests
import json

# Configure page
st.set_page_config(
    page_title="Offline Inspection AI Copilot",
    page_icon="🔧",
    layout="wide"
)

# Initialize session state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'df' not in st.session_state:
    st.session_state.df = None

def call_local_llm(prompt, context=""):
    """Call local Ollama LLM"""
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'phi',
                'prompt': f"{context}\n\n{prompt}",
                'stream': False
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()['response']
        else:
            return "LLM unavailable. Running in analysis-only mode."
    except:
        return "LLM offline. Showing statistical analysis only."

def analyze_inspection_data(df):
    """Run automated statistical analysis"""
    analysis = {}
    
    # Basic stats
    analysis['total_records'] = len(df)
    analysis['columns'] = df.columns.tolist()
    
    # Identify numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    analysis['numeric_columns'] = numeric_cols
    
    # Statistical summary
    if numeric_cols:
        analysis['summary_stats'] = df[numeric_cols].describe().to_dict()
        
        # Anomaly detection (simple z-score method)
        anomalies = {}
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                z_scores = np.abs((df[col] - mean) / std)
                anomaly_count = (z_scores > 3).sum()
                if anomaly_count > 0:
                    anomalies[col] = int(anomaly_count)
        analysis['anomalies'] = anomalies
    
    # Missing data analysis
    missing = df.isnull().sum()
    analysis['missing_data'] = missing[missing > 0].to_dict()
    
    return analysis

def generate_visualizations(df):
    """Create automated visualizations"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.warning("No numeric columns found for visualization")
        return
    
    # Distribution plots
    st.subheader("📊 Data Distributions")
    cols_per_row = 3
    rows = (len(numeric_cols) + cols_per_row - 1) // cols_per_row
    
    for i in range(rows):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i * cols_per_row + j
            if idx < len(numeric_cols):
                with cols[j]:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.hist(df[numeric_cols[idx]].dropna(), bins=30, edgecolor='black', alpha=0.7)
                    ax.set_title(f'{numeric_cols[idx]} Distribution')
                    ax.set_xlabel(numeric_cols[idx])
                    ax.set_ylabel('Frequency')
                    ax.grid(alpha=0.3)
                    st.pyplot(fig)
                    plt.close()
    
    # Correlation heatmap if multiple numeric columns
    if len(numeric_cols) > 1:
        st.subheader("🔥 Correlation Matrix")
        fig, ax = plt.subplots(figsize=(10, 8))
        corr = df[numeric_cols].corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
        ax.set_title('Feature Correlations')
        st.pyplot(fig)
        plt.close()
    
    # Time series if date column exists
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    if not date_cols:
        # Try to find date-like columns
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_cols.append(col)
                    break
                except:
                    pass
    
    if date_cols and numeric_cols:
        st.subheader("📈 Time Series Trends")
        date_col = date_cols[0]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        for col in numeric_cols[:3]:  # Plot first 3 numeric columns
            ax.plot(df[date_col], df[col], marker='o', label=col, alpha=0.7)
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.set_title('Trends Over Time')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close()

# Main UI
st.title("🔧 Offline Inspection AI Copilot")
st.markdown("**Secure, offline AI-powered analysis for industrial inspection data**")

st.sidebar.header("⚙️ Configuration")
st.sidebar.markdown("### System Status")
st.sidebar.success("✅ Python Libraries Loaded")
try:
    requests.get('http://localhost:11434/api/tags', timeout=2)
    st.sidebar.success("✅ LLM Online (Ollama)")
except:
    st.sidebar.warning("⚠️ LLM Offline (Analysis mode only)")

# File upload
st.header("📁 Data Input")
uploaded_file = st.file_uploader("Upload Inspection Data (CSV)", type=['csv'])

# Sample data generator
if st.button("🧪 Generate Sample Inspection Data"):
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    sample_data = pd.DataFrame({
        'inspection_date': dates,
        'equipment_id': [f'EQ-{i:03d}' for i in np.random.randint(1, 20, 100)],
        'corrosion_rate': np.random.exponential(0.5, 100),
        'wall_thickness': np.random.normal(10, 1, 100),
        'pressure_psi': np.random.normal(1500, 100, 100),
        'temperature_c': np.random.normal(80, 15, 100),
        'risk_score': np.random.uniform(0, 10, 100),
        'inspector': np.random.choice(['John', 'Sarah', 'Mike', 'Emma'], 100)
    })
    st.session_state.df = sample_data
    st.success("✅ Sample data generated!")

if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.success(f"✅ File uploaded: {uploaded_file.name}")

# Analysis section
if st.session_state.df is not None:
    df = st.session_state.df
    
    st.header("📋 Data Preview")
    st.dataframe(df.head(10))
    st.info(f"**Dataset:** {len(df)} records × {len(df.columns)} columns")
    
    if st.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Analyzing data..."):
            st.session_state.analysis_done = True
    
    if st.session_state.analysis_done:
        # Statistical Analysis
        st.header("📊 Automated Analysis")
        analysis = analyze_inspection_data(df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", analysis['total_records'])
        with col2:
            st.metric("Numeric Features", len(analysis['numeric_columns']))
        with col3:
            anomaly_total = sum(analysis['anomalies'].values()) if analysis['anomalies'] else 0
            st.metric("Anomalies Detected", anomaly_total)
        
        # Anomalies
        if analysis['anomalies']:
            st.subheader("⚠️ Anomaly Detection")
            for col, count in analysis['anomalies'].items():
                st.warning(f"**{col}**: {count} outliers detected (>3 standard deviations)")
        
        # Missing data
        if analysis['missing_data']:
            st.subheader("🔍 Data Quality Issues")
            for col, count in analysis['missing_data'].items():
                st.info(f"**{col}**: {count} missing values")
        
        # Visualizations
        generate_visualizations(df)
        
        # LLM Insights
        st.header("🤖 AI Insights")
        
        # Prepare context for LLM
        context = f"""You are an expert in industrial inspection and corrosion analysis.
Analyze this inspection dataset:
- Total records: {analysis['total_records']}
- Features: {', '.join(analysis['columns'])}
- Anomalies detected: {analysis['anomalies']}
- Missing data: {analysis['missing_data']}

Provide actionable insights for engineers."""
        
        insight_prompt = st.text_area(
            "Ask the AI about this data:",
            "Summarize the key risks and provide recommendations for the inspection team.",
            height=100
        )
        
        if st.button("Generate AI Insight"):
            with st.spinner("Consulting local AI..."):
                response = call_local_llm(insight_prompt, context)
                st.markdown("### 💡 AI Analysis")
                st.info(response)
        
        # Export section
        st.header("📤 Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            # Export cleaned data
            csv = df.to_csv(index=False)
            st.download_button(
                "Download Processed Data (CSV)",
                csv,
                "inspection_analysis.csv",
                "text/csv"
            )
        
        with col2:
            # Export analysis report
            report = f"""Inspection Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Dataset Summary:
- Total Records: {analysis['total_records']}
- Features: {len(analysis['columns'])}
- Anomalies: {sum(analysis['anomalies'].values()) if analysis['anomalies'] else 0}

Numeric Features:
{', '.join(analysis['numeric_columns'])}

Anomalies Detected:
{json.dumps(analysis['anomalies'], indent=2)}

Missing Data:
{json.dumps(analysis['missing_data'], indent=2)}
"""
            st.download_button(
                "Download Analysis Report (TXT)",
                report,
                "analysis_report.txt",
                "text/plain"
            )

else:
    st.info("👆 Upload a CSV file or generate sample data to begin analysis")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛡️ Offline Mode")
st.sidebar.markdown("All computations run locally. No data leaves this machine.")
st.sidebar.markdown("**Built with:** Python, Pandas, NumPy, Matplotlib, Streamlit")