# 🔧 Offline Inspection AI Copilot

**An offline-first AI platform for industrial inspection data analysis** - built for secure, air-gapped environments like offshore rigs and industrial facilities.

## 🎯 The Problem

Industrial facilities (oil rigs, refineries, offshore platforms) face critical challenges:
- **No cloud access** in secure/remote environments
- **Data isolation requirements** for sensitive inspection data
- **Need for real-time analysis** without internet dependency
- **Complex computations** requiring scientific Python libraries
- **AI-powered insights** without cloud APIs

## 💡 The Solution

A fully containerized platform that runs **100% offline**:
- ✅ Built-in Python scientific stack (NumPy, Pandas, Matplotlib, SciPy)
- ✅ Local LLM (Phi/Mistral) for AI-powered insights
- ✅ Automated anomaly detection and statistical analysis
- ✅ Interactive visualizations and reporting
- ✅ Docker-packaged for "run anywhere" capability
- ✅ Zero external dependencies after setup

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (or Docker Engine + Docker Compose)
- 8GB RAM minimum (16GB recommended for larger models)
- 10GB disk space

### Installation

1. **Clone/Download this project**
   ```bash
   # Project structure:
   # .
   # ├── app.py
   # ├── Dockerfile
   # ├── docker-compose.yml
   # ├── requirements.txt
   # ├── setup.sh
   # └── README.md
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Access the application**
   - Open browser: `http://localhost:8501`
   - Start analyzing inspection data!

### Manual Setup (if script fails)

```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# Download AI model
docker exec ollama_llm ollama pull phi

# Check status
docker-compose ps
```

---

## 📖 How to Use

### 1. **Upload Data**
- Click "Upload Inspection Data (CSV)"
- Or use "Generate Sample Data" for testing

### 2. **Run Analysis**
- Preview your data
- Click "Run Analysis" button
- View automated insights:
  - Statistical summaries
  - Anomaly detection (outliers)
  - Missing data analysis
  - Distribution plots
  - Correlation matrices
  - Time series trends

### 3. **AI Insights**
- Ask questions about your data
- Get recommendations from the local LLM
- Example prompts:
  - "What are the main corrosion risks?"
  - "Which equipment needs immediate attention?"
  - "Summarize inspection findings"

### 4. **Export Results**
- Download processed data (CSV)
- Export analysis report (TXT)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│     Streamlit Web Interface         │
│  (Data Upload, Viz, AI Chat)        │
└──────────────┬──────────────────────┘
               │
    ┌──────────▼──────────┐
    │  Python Analytics    │
    │  • Pandas            │
    │  • NumPy             │
    │  • Matplotlib        │
    │  • SciPy             │
    │  • Scikit-learn      │
    └──────────┬───────────┘
               │
    ┌──────────▼───────────┐
    │   Ollama LLM Engine  │
    │   (Phi/Mistral/etc)  │
    │   Runs 100% locally  │
    └──────────────────────┘
```

**All components run in Docker containers - no external calls**

---

## 🎓 Technical Features

### Data Analysis Engine
- **Automated statistical analysis**: mean, std, quartiles, ranges
- **Anomaly detection**: Z-score based outlier identification (>3σ)
- **Missing data profiling**: identify data quality issues
- **Correlation analysis**: feature relationships
- **Time series visualization**: trend detection

### AI Capabilities
- **Local LLM inference**: No API keys, no cloud
- **Contextual understanding**: AI knows your data schema
- **Engineering-focused prompts**: Trained for technical analysis
- **Offline operation**: Works in air-gapped networks

### Security & Compliance
- **No data egress**: Everything stays on your machine
- **Containerized isolation**: Secure runtime environment
- **Audit-ready**: All operations logged locally
- **Reproducible**: Same container = same results

---

## 🔧 Configuration

### Change the LLM Model

Available models (via Ollama):
- `phi` (2.7B params) - Fast, good for quick analysis
- `mistral` (7B params) - More capable, slower
- `llama2` (7B params) - Balanced
- `codellama` (7B params) - For code-heavy tasks

```bash
# Download a new model
docker exec ollama_llm ollama pull mistral

# List installed models
docker exec ollama_llm ollama list

# Update app.py to use the new model:
# Change 'model': 'phi' to 'model': 'mistral'
```

### Adjust Memory/Resources

Edit `docker-compose.yml`:
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

### Add Custom Python Libraries

Add to `requirements.txt`, rebuild:
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Sample Use Cases

### 1. **Corrosion Rate Analysis**
Upload inspection data with fields:
- `equipment_id`, `inspection_date`, `corrosion_rate`, `wall_thickness`

Get automated:
- Equipment with critical corrosion rates
- Trend analysis over time
- Predictive maintenance recommendations

### 2. **Inspection Report Processing**
Upload CSV exports from inspection software:
- Detect anomalies in pressure/temperature readings
- Flag equipment outside normal ranges
- Generate executive summary via AI

### 3. **Failure Analysis**
Historical failure data:
- Correlate failure modes with operational parameters
- Identify common patterns
- AI-generated risk assessment

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml
ports:
  - "8502:8501"  # Use different external port
```

### LLM Not Responding
```bash
# Check Ollama status
docker logs ollama_llm

# Restart LLM container
docker-compose restart ollama

# Re-pull model
docker exec ollama_llm ollama pull phi
```

### Out of Memory
- Use smaller model (`phi` instead of `mistral`)
- Close other applications
- Increase Docker memory limit (Docker Desktop → Settings → Resources)

### Slow Performance
- For large CSV files, increase container memory
- Use smaller datasets for initial testing
- Consider running on a machine with more RAM

---

## 🚢 Deployment for Offline Use

### Export the Entire System

1. **Save Docker images**
   ```bash
   docker save inspection_copilot ollama/ollama > copilot_images.tar
   ```

2. **Package everything**
   ```bash
   tar -czf offline_copilot.tar.gz \
     app.py requirements.txt Dockerfile \
     docker-compose.yml README.md copilot_images.tar
   ```

3. **Transfer to offline machine**
   - Use USB drive or secure file transfer
   - Load images: `docker load < copilot_images.tar`
   - Run: `docker-compose up -d`

### Pre-download LLM Models

Before going offline:
```bash
# Download multiple models
docker exec ollama_llm ollama pull phi
docker exec ollama_llm ollama pull mistral
docker exec ollama_llm ollama pull llama2

# Verify
docker exec ollama_llm ollama list
```

Models are stored in the `ollama_models` volume and persist across restarts.

---

## 📝 Data Format Examples

### Inspection CSV Format
```csv
inspection_date,equipment_id,corrosion_rate,wall_thickness,pressure_psi,temperature_c,risk_score,inspector
2024-01-01,EQ-001,0.5,10.2,1500,80,3.2,John
2024-01-02,EQ-002,0.8,9.8,1520,82,5.1,Sarah
2024-01-03,EQ-003,0.3,10.5,1490,79,2.1,Mike
```

### Required Columns (flexible)
- At least one numeric column for analysis
- Optional: date column for time series
- Optional: categorical columns for grouping

---

## 🎤 Pitch-Ready Features

When presenting to judges:

**Problem Statement:**
"Industrial facilities can't use cloud AI due to security and connectivity constraints."

**Solution:**
"We built a portable AI lab that runs entirely offline - includes scientific Python libraries and a local LLM."

**Demo Flow:**
1. Upload inspection data (or generate sample)
2. Show automated analysis (anomalies, visualizations)
3. Ask AI for insights
4. Export report

**Key Differentiators:**
- ✅ 100% offline operation
- ✅ No vendor lock-in
- ✅ Runs anywhere (Docker)
- ✅ Extensible to any track (CCD, Inspection, Failure Analysis)

**Vision:**
"Same platform can power corrosion prediction, document analysis, and real-time monitoring - all without cloud dependency."

---

## 🛠️ Development

### Project Structure
```
.
├── app.py              # Main Streamlit application
├── Dockerfile          # Container definition
├── docker-compose.yml  # Multi-container orchestration
├── requirements.txt    # Python dependencies
├── setup.sh           # Automated setup script
├── README.md          # This file
└── data/              # Local data directory (auto-created)
```

### Extending the Code

**Add new analysis functions:**
```python
def custom_analysis(df):
    # Your analysis logic
    return results

# Add to app.py analysis section
```

**Add new visualizations:**
```python
# In generate_visualizations() function
fig, ax = plt.subplots()
# Your plot code
st.pyplot(fig)
```

**Customize LLM prompts:**
```python
# Modify context in the LLM section
context = f"""Custom instructions for your use case..."""
```

---

## 📚 Learning Resources

To build competence in 2 weeks:

### Week 1: Basics
- **Python Pandas**: [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- **Streamlit**: [Official Tutorial](https://docs.streamlit.io/get-started/tutorials)
- **Docker**: [Docker 101](https://www.docker.com/101-tutorial/)

### Week 2: Advanced
- **Ollama**: [Ollama Docs](https://ollama.com/)
- **LLM Prompting**: [Prompt Engineering Guide](https://www.promptingguide.ai/)
- **Data Viz**: [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)

---

## 🤝 Contributing

Ideas for enhancement:
- [ ] Add image-based inspection analysis (computer vision)
- [ ] Support Excel/PDF uploads
- [ ] Real-time data streaming
- [ ] Multi-user collaboration
- [ ] Custom ML model training
- [ ] 3D visualization for equipment models

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## 🎯 Next Steps

1. **Test with real Aramco data** once provided
2. **Fine-tune prompts** for specific inspection types
3. **Add domain-specific calculations** (e.g., corrosion rate formulas)
4. **Create templates** for different inspection workflows
5. **Build pitch deck** highlighting offline capabilities

---

## 💬 Questions?

This is a **hackathon MVP** - it prioritizes:
- ✅ Working demo over perfection
- ✅ Core features over edge cases
- ✅ Clear vision over comprehensive coverage

**Your goal:** Show judges a functional prototype that solves a real problem in a novel way.

**Remember:** Everyone else is also Googling "how to build this" right now. You're ahead by actually shipping code.

---

**Built# inspection-copilot
