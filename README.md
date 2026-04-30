# Airline Fuel Optimization Agent (AWS Strands + MCP)
This project builds an intelligent fuel optimization agent that combines traditional optimization with LLM reasoning using AWS Strands and MCP. It analyzes flight, weather, and aircraft data to generate efficient routing and altitude recommendations, improving fuel efficiency and operational decision-making. 

---

##  Architecture

The system follows a layered architecture:

1. **Input Layer**
   - Flight data from CSV

2. **Optimization Layer**
   - Local fuel calculation
   - Baseline optimization

3. **Agent Layer (Strands)**
   - Uses LLM (via Ollama)
   - Applies reasoning:
     - Altitude efficiency
     - Wind impact
     - Safety constraints

4. **MCP Tool Layer**
   - Weather MCP → fetch METAR/TAF  
   - Mission Control MCP → publish recommendations  

5. **Output Layer**
   - JSON output + CLI report  

---

## Tech Stack

- Python 3.11+
- AWS Strands
- MCP Protocol
- Ollama (LLM runtime)
- Rich (CLI UI)
- METAR Weather API

---

## Project Structure

```
airline-fuel-optimization-agent/
│
├── main.py                     
│
├── agent/                      
│   └── agent.py
│
├── optimization.py             
│
├── data/                       
│   └── flights.csv
│
├── mcp_servers/                
│   ├── weather_server.py       
│   └── mission_control.py      
│
├── Dockerfile                  
├── requirements.txt           
├── README.md                  
│


```

---

##  Setup

### 1. Clone the Repository
```bash
git clone 
cd Airline-fuel-optimization-agent
```

---

### 2. Create Virtual Environment
```bash
python3 -m venv airline-venv
```

#### Activate:

- **Mac/Linux**
```bash
source airline-venv/bin/activate
```

- **Windows**
```bash
airline-venv\Scripts\activate
```

---

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4. Setup Ollama (Local Installation)

#### Install Ollama  
Download from: https://ollama.com/download  

- Windows → `.exe`  
- Mac → `.dmg`  

Verify installation:
```bash
ollama --version
```

---

#### Download LLM Model
```bash
ollama pull llama3.1
```

 Model size: ~4.9 GB (one-time download)

---

#### Start Ollama
```bash
ollama serve
```

 If already running, skip this step

Check:
```bash
curl http://localhost:11434
```

Expected output:
```
Ollama is running
```

---

### 5. Run the Project
```bash
python main.py
```

---

###  Optional: Run Single Flight
```bash
python main.py --flight AI101
```




---

##  Example Input

```csv
flight_id,origin,destination,aircraft_type,planned_altitude_ft,planned_route,passengers,cargo_kg
AI101,DEL,BOM,A320,35000,DEL-NAG-BOM,180,2000
AI202,BLR,DEL,B737,36000,BLR-HYD-DEL,160,1500
AI303,MUM,DXB,A320,37000,MUM-KAR-DXB,170,1800
```

---

##  Example Output

```json
{
  "flight_id": "AI101",
  "origin": "DEL",
  "destination": "BOM",
  "original_fuel": 1647.6,
  "optimized_fuel": 1614.6,
  "savings_kg": 33.0,
  "savings_pct": 2.0,
  "recommended_action": "Increase altitude to FL370",
  "rationale": "Higher altitude improves lift-to-drag ratio, reducing fuel burn. Wind impact is minimal and conditions are safe (VFR).",
  "mission_control_status": "sent"
}
```

---

##  How It Works

1. Load flight data from CSV  
2. Run local fuel optimization  
3. Agent fetches weather via MCP  
4. LLM refines recommendation  
5. Publish to mission control  
6. Output final report  

---

##  Features

- Fuel optimization logic  
- Weather-aware decision making  
- MCP-based tool integration  
- Agentic workflow using Strands  
- CLI reporting  

---

 


