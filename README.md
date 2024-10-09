
# Healthcare PAL System: Program-Aided Language Model (PAL)

This project implements a **Program-Aided Language Model (PAL)** for analyzing drug usage in **elderly patients** using data from a Neo4j database and **Gemini API**. The database is based on the healthcare analytics example provided by Neo4j, which contains information about drug usage, reactions, outcomes, and more. This system employs a **PALM** approach to generate insightful recommendations for healthcare practitioners.

## Project Overview

The goal of this project is to design a system that leverages Neo4j’s graph database to analyze cases of **elderly patients** who were prescribed certain drugs. The analysis is backed by querying the database and applying structured reasoning steps that follow a PAL approach. The output provides insights into adverse reactions, drug interactions, and the risks associated with using a particular drug for elderly patients.

Additionally, the system integrates **Gemini API** to generate AI-driven insights and recommendations. Using **Program-Aided Language Model (PAL)**, this project provides a structured mechanism for generating and interpreting complex healthcare data.

### Key Features
- **Drug analysis**: Analyze the cases where elderly patients were prescribed specific drugs.
- **Reactions and Outcomes**: Identify common reactions and outcomes based on historical data.
- **Drug Interactions**: Identify other drugs that may interact with the primary drug.
- **AI-driven Recommendations**: Generate recommendations using the Gemini API to provide actionable healthcare insights.
- **Implementation of PALM**: Utilizing the Gemini model and structured reasoning to simulate human-like judgment.

## Getting Started

### Prerequisites

1. **Neo4j Database**:
   - The database is powered by Neo4j, and a dump file from the [Neo4j Healthcare Analytics Example](https://github.com/neo4j-graph-examples/healthcare-analytics) repository is used.
   - **Important Note**: There was a **typographical error** in the dataset. The property `PrimarySubstabce` was corrected to `PrimarySubstance`. Make sure to update the database schema accordingly if you are working with the dataset.

2. **Gemini API**:
   - This project uses the **Gemini API** for generating AI-driven insights. You will need a valid **Gemini API key**. The API key is required to authenticate the system and generate recommendations.
   - The API uses **Program-Aided Language Model (PAL)** to produce structured and contextually relevant insights based on healthcare data.

3. **Python Dependencies**:
   - This project requires the following Python packages:
     - `neo4j`: Python driver for interacting with the Neo4j database.
     - `python-dotenv`: For loading environment variables from `.env` files.
     - `genai`: Python client to interface with the Gemini API.

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


#### 4. Set up your `.env` file
Create a `.env` file in the project root directory and add your Neo4j credentials, Gemini API key, and connection URI:

```plaintext
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=<your-neo4j-username>
NEO4J_PASSWORD=<your-neo4j-password>
GEMINI_API_KEY=<your-gemini-api-key>
```

### Running the Application

To run the program, use the following command:
```bash
python healthcare_pal.py
```

This will prompt you to enter a drug name for analysis. The system will then query the Neo4j database, perform analysis, and generate AI-driven insights using the Gemini API.

### Query Logic

The system leverages Cypher queries in Neo4j to perform the following steps:

1. **Find Elderly Cases**: Identify all cases where elderly patients (age group: Elderly) were prescribed a drug.
2. **Analyze Reactions and Outcomes**: Gather the most common reactions and outcomes related to the drug usage in elderly patients.
3. **Identify Drug Interactions**: Identify other drugs that may have interactions with the primary drug prescribed.
4. **Generate Recommendations**: Based on the analysis, the system generates AI-driven recommendations using the **Gemini API** for healthcare practitioners.

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

### AI-Driven Insights (Gemini API & PALM)

In addition to the database analysis, the **Gemini API** is used to generate AI-driven insights with **Program-Aided Language Model (PALM)**. After performing the analysis on the data, the system sends the findings to Gemini to generate recommendations and structured insights for healthcare practitioners. The insights help to evaluate risks, drug interactions, and suggest appropriate courses of action.

Here’s an example of how the AI-driven recommendation might look:

#### Example Output:

```
Projects\HealthCare> py healthcare_pal.py
Enter the name of the drug prescribed to an elderly patient: COSENTYX

Analysis of Drug for Elderly Patients:
Step 1: Identifying cases involving elderly patients taking COSENTYX
Found 8 cases of elderly patients taking COSENTYX (Primary Substance: SECUKINUMAB)
Step 2: Analyzing reactions and outcomes for COSENTYX in elderly patients
Top 3 reactions: Fall (5 cases), Aortic occlusion (3 cases), Cerebrovascular accident (3 cases)
Top 3 outcomes: Hospitalization - Initial or Prolonged (31 cases), Other Serious (Important Medical Event) (20 cases), Death (7 cases)
Step 3: Identifying potential drug interactions with COSENTYX      
No interacting drugs found.
Step 4: Calculating risk percentages
Risk of death: 87.50%
Step 5: Generating recommendation based on analysis
Recommendation: Based on the analysis of elderly patients taking COSENTYX:
1. Common reactions include Fall, Aortic occlusion, Cerebrovascular accident. Monitor patients for these symptoms.
2. The risk of death is approximately 87.50%.
4. Consider alternative therapies if the patient is at high risk, or ensure close monitoring during treatment.

AI-Generated Insight:
## Medical Insight: COSENTYX (SECUKINUMAB) in Elderly Patients     

The provided analysis highlights a concerning trend of serious adverse events in elderly patients taking COSENTYX. While the sample size of 8 cases is small, the high incidence of falls, aortic occlusion, cerebrovascular accidents (CVA), and significant mortality demands careful consideration.

**Adverse Reactions and Outcomes:**

* **Falls:** The high prevalence of falls (5 out of 8 cases) suggests an increased risk of falls in elderly patients taking COSENTYX. This could be related to the drug's impact on blood pressure, potential for dizziness, or other side effects. It is crucial to assess individual risk factors for falls (e.g., gait instability, medications, environmental hazards) and implement preventative measures.   
* **Aortic Occlusion & CVA:** The occurrence of both aortic occlusion and CVA in multiple cases is particularly alarming. This suggests a potential link between COSENTYX and cardiovascular complications. It is essential to thoroughly evaluate patients for existing cardiovascular risk factors and closely monitor for any signs of cardiovascular compromise during and after treatment.
* **Hospitalization & Death:** The high rates of hospitalization and death (31 cases and 7 cases, respectively) underscore the severity of adverse events associated with COSENTYX in the elderly. This data emphasizes the need for careful patient selection and vigilant monitoring.

**Risk Factors and Potential Interactions:**

* **Age and Pre-existing Conditions:** The elderly are inherently at increased risk for falls, cardiovascular disease, and other health issues.
* **Other Medications:** While no drug interactions were found in this specific analysis, it is crucial to review the patient's entire medication regimen for potential interactions that could exacerbate side effects.
* **Underlying Disease:**  COSENTYX is commonly used for inflammatory conditions. In elderly patients, these conditions may be more severe and complicated by age-related changes, potentially increasing the risk of adverse events.

**Recommendations for Healthcare Providers:**

1. **Patient Selection:**  Prioritize careful patient selection, considering the individual's age, overall health status, and existing cardiovascular risk factors.
2. **Baseline Assessment:** Perform a comprehensive baseline assessment, including cardiovascular evaluation, falls risk assessment, and a thorough medication review.
3. **Close Monitoring:**  Closely monitor patients for signs of adverse events, including falls, cardiovascular changes, and any changes in neurological status.
tweigh the risks in a particular patient.

**Conclusion:**

This analysis suggests a significant risk of adverse events, including falls, aortic occlusion, CVA, and death, associated with COSENTYX in elderly patients.  Healthcare providers should exercise caution and prioritize patient safety by following the above recommendations. Further research and larger studies are needed to fully elucidate the specific risks and benefits of COSENTYX in this vulnerable population.
```


