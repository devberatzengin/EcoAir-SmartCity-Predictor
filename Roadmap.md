# EcoAir SmartCity Predictor  
**Technical Requirements & Timeline**

## Project Vision

To analyze real-time air quality metrics from Istanbul stations, integrate them with live traffic density and meteorological parameters, and provide future projections.

The system utilizes:
- A Python-based AI service for intelligence and prediction
- A Java Spring Boot-based orchestration backbone for data management and scheduling

---

# Epic 1: Data Engineering & Collection  
**Estimated Duration: 1 Week**

## Story 1.1: IBB Air Quality Service Integration (2 Days)

- Fetch real-time PM10, SO2, CO, NO2, and O3 metrics  
- Integrate with IBB Open Data Portal  
- Cover approximately 40 air quality monitoring stations  

## Story 1.2: Meteorological Data Enrichment (1 Day)

- Retrieve wind speed, wind direction, humidity, and temperature  
- Use OpenWeatherMap API  
- Map data based on station coordinates  

## Story 1.3: Traffic Density Data Mapping (2 Days)

- Retrieve traffic density data from IBB Traffic API  
- Assign traffic data to nearest air quality station  
- Implement geographic proximity algorithms  

---

# Epic 2: Machine Learning & Inference Service  
**Estimated Duration: 1.5 Weeks**

## Story 2.1: Data Preprocessing & Feature Engineering (3 Days)

- Clean missing values  
- Handle outliers  
- Create time-series features:
  - Hourly cycles  
  - Daily cycles  
  - Lag features  

## Story 2.2: Time-Series Model Development (4 Days)

- Train RandomForest or XGBoost models  
- Support:
  - 15-minute real-time predictions  
  - 3-hour future forecasts  

## Story 2.3: Prediction API Deployment (2 Days)

- Develop a FastAPI service  
- Accept raw data from Java backend  
- Return prediction results in JSON format  

---

# Epic 3: System Orchestration & Data Management  
**Estimated Duration: 1.5 Weeks**

## Story 3.1: Spring Boot Infrastructure & DB Modeling (2 Days)

- Configure Maven project structure  
- Design relational schema in PostgreSQL  
- Create entities and repositories  

## Story 3.2: Scheduled Data Collection (The Worker) (3 Days)

- Implement `@Scheduled` tasks  
- Trigger ingestion and processing every 15 minutes  
- Persist enriched data into database  

## Story 3.3: Python Service Integration (WebClient) (2 Days)

- Use Spring WebClient  
- Send HTTP requests to Python FastAPI service  
- Store prediction results in database  

---

# Epic 4: Presentation Layer  
**Estimated Duration: 1 Week**

## Story 4.1: Dashboard & Visualization (4 Days)

- Develop web interface  
- Display Istanbul station statuses  
- Show:
  - Real-time metrics  
  - 3-hour predictions  
  - Historical comparison  