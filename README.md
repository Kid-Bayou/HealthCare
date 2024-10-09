# Healthcare PAL System: Program-Aided Language Model (PAL)

This project implements a **Program-Aided Language Model (PAL)** for analyzing drug usage in **elderly patients** using data from a Neo4j database. The database is based on the healthcare analytics example provided by Neo4j, which contains information about drug usage, reactions, outcomes, and more.

## Project Overview

The goal of this project is to design a system that leverages Neo4j’s graph database to analyze cases of **elderly patients** who were prescribed certain drugs. The analysis is backed by querying the database and applying structured reasoning steps that follow a PAL approach. The output provides insights into adverse reactions, drug interactions, and the risks associated with using a particular drug for elderly patients.

### Key Features
- **Drug analysis**: Analyze the cases where elderly patients were prescribed specific drugs.
- **Reactions and Outcomes**: Identify common reactions and outcomes based on historical data.
- **Drug Interactions**: Identify other drugs that may interact with the primary drug.
- **Recommendation**: Generate recommendations based on analysis, highlighting risks and potential drug interactions.

## Getting Started

### Prerequisites

1. **Neo4j Database**:
   - The database is powered by Neo4j, and a dump file from the [Neo4j Healthcare Analytics Example](https://github.com/neo4j-graph-examples/healthcare-analytics) repository is used.
   - **Important Note**: There was a **typographical error** in the dataset. The property `PrimarySubstabce` was corrected to `PrimarySubstance`. Make sure to update the database schema accordingly if you are working with the dataset.

2. **Python Dependencies**:
   - This project requires the following Python packages:
     - `neo4j`: Python driver for interacting with the Neo4j database.
     - `python-dotenv`: For loading environment variables from `.env` files.

### Installation

#### 1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

#### 2. Set up the Python environment
Create and activate a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

#### 3. Install the required dependencies
```bash
pip install -r requirements.txt
```

Make sure your `requirements.txt` file includes:
```plaintext
neo4j
python-dotenv
```

#### 4. Set up your `.env` file
Create a `.env` file in the project root directory and add your Neo4j credentials and connection URI:

```plaintext
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=<your-neo4j-username>
NEO4J_PASSWORD=<your-neo4j-password>
```

### Running the Application

To run the program, use the following command:
```bash
python healthcare_pal.py
```

This will prompt you to enter a drug name for analysis. The system will then query the Neo4j database and return a detailed analysis of the drug usage among elderly patients, including potential risks, reactions, and drug interactions.

### Query Logic

The system leverages Cypher queries in Neo4j to perform the following steps:

1. **Find Elderly Cases**: Identify all cases where elderly patients (age group: Elderly) were prescribed a drug.
2. **Analyze Reactions and Outcomes**: Gather the most common reactions and outcomes related to the drug usage in elderly patients.
3. **Identify Drug Interactions**: Identify other drugs that may have interactions with the primary drug prescribed.
4. **Generate Recommendations**: Based on the analysis, the system generates recommendations for healthcare practitioners.

### Database Schema

The database is modeled with several nodes and relationships, including:

- **Nodes**:
  - `Drug`: Contains information about drugs, including `primarySubstance` and `name`.
  - `Case`: Contains information about individual patient cases, including `primaryid`, `age`, `gender`, `reportDate`, and `eventDate`.
  - `AgeGroup`: Contains information about age groups (e.g., "Elderly").
  - `Reaction`: Contains descriptions of reactions (e.g., "Pulmonary embolism").
  - `Outcome`: Contains the outcome of the case (e.g., "Death").
  - `Therapy`, `Manufacturer`, `ReportSource`: Other nodes used for associating additional information.

- **Relationships**:
  - `IS_PRIMARY_SUSPECT`: Links `Drug` to `Case` (the drug is suspected of causing the adverse event).
  - `FALLS_UNDER`: Links `Case` to `AgeGroup` (identifies the patient's age group).
  - `HAS_REACTION`: Links `Case` to `Reaction`.
  - `RESULTED_IN`: Links `Case` to `Outcome`.
  - `IS_CONCOMITANT`: Links `Case` to other drugs taken concurrently.
  - `IS_INTERACTING`: Links `Drug` to other drugs that may have interactions.

### Example Output

When you enter a drug name, the system will output detailed information like:

- **Step 1**: Identifying cases involving elderly patients taking the specified drug.
- **Step 2**: Analyzing reactions and outcomes associated with the drug.
- **Step 3**: Identifying other drugs that may interact with the drug.
- **Step 4**: Calculating risks such as the probability of hospitalization.
- **Step 5**: Generating a recommendation for healthcare practitioners.

### Example of Analysis:

```
Step 1: Identifying cases involving elderly patients taking AFINITOR
Found 5 cases of elderly patients taking AFINITOR

Step 2: Analyzing reactions and outcomes for AFINITOR in elderly patients
Top 3 reactions: Pulmonary embolism (2 cases), Nausea (1 case), Dizziness (1 case)
Top 3 outcomes: Death (2 cases), Recovery (1 case), Hospitalization (2 cases)

Step 3: Identifying potential drug interactions with AFINITOR
Top 3 potentially interacting drugs: LIPITOR (2 cases), ASPIRIN (1 case), XELJANZ (1 case)

Step 4: Calculating risk percentages
Risk of hospitalization: 40.00%

Step 5: Generating recommendation based on analysis
Recommendation: Based on the analysis of elderly patients taking AFINITOR:
1. Common reactions include Pulmonary embolism, Nausea, and Dizziness. Monitor patients for these symptoms.
2. The risk of hospitalization is approximately 40.00%.
3. Be cautious when co-prescribing with LIPITOR, ASPIRIN, and XELJANZ, as these drugs were frequently associated with adverse events.
4. Consider alternative therapies if the patient is at high risk, or ensure close monitoring during treatment.
```

