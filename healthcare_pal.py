from neo4j import GraphDatabase
from typing import List, Dict, Any
from dotenv import load_dotenv
import os
import requests
import google.generativeai as genai

# Load environment variables
load_dotenv()

class HealthcarePALSystem:
    def __init__(self, uri: str, user: str, password: str, gemini_api_key: str):
        # Connect to Neo4j
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        # Set the Gemini API key for AI-based insights
        self.gemini_api_key = gemini_api_key
        # Configure Gemini API
        genai.configure(api_key=self.gemini_api_key)

    def close(self):
        # Close Neo4j connection
        self.driver.close()

    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def get_elderly_cases_for_drug(self, drug_name: str) -> List[Dict[str, Any]]:
        query = """
        MATCH (d:Drug {name: $drug_name})<-[:IS_PRIMARY_SUSPECT]-(c:Case)-[:FALLS_UNDER]->(a:AgeGroup)
        WHERE a.ageGroup = 'Elderly'
        RETURN c.primaryid AS case_id, c.age AS patient_age, c.gender AS patient_gender, c.reportDate AS report_date, d.primarySubstance AS primary_substance
        """
        return self.execute_query(query, {"drug_name": drug_name})

    def get_reactions_and_outcomes(self, case_ids: List[str]) -> List[Dict[str, Any]]:
        query = """
        MATCH (c:Case)-[:HAS_REACTION]->(r:Reaction), (c)-[:RESULTED_IN]->(o:Outcome)
        WHERE c.primaryid IN $case_ids
        RETURN c.primaryid AS case_id, r.description AS reaction, o.outcome AS outcome
        """
        return self.execute_query(query, {"case_ids": case_ids})

    def get_interacting_drugs(self, case_ids: List[str], primary_drug: str) -> List[Dict[str, Any]]:
        query = """
            MATCH (c:Case)-[:IS_PRIMARY_SUSPECT]->(d:Drug {primarySubstance: $primary_drug})
            WHERE c.primaryid IN $case_ids
            MATCH (c)-[:IS_CONCOMITANT|IS_INTERACTING]->(other:Drug)
            WHERE other.primarySubstance <> $primary_drug
            RETURN DISTINCT other.primarySubstance AS interacting_drug, 
                COUNT(c) AS interaction_count
            ORDER BY interaction_count DESC
        """
        return self.execute_query(query, {"case_ids": case_ids, "primary_drug": primary_drug})

    def analyze_drug_for_elderly(self, drug_name: str) -> str:
        reasoning_steps = []

        reasoning_steps.append(f"Step 1: Identifying cases involving elderly patients taking {drug_name}")
        elderly_cases = self.get_elderly_cases_for_drug(drug_name)
        if not elderly_cases:
            reasoning_steps.append(f"No cases found for elderly patients taking {drug_name}.")
            return "\n".join(reasoning_steps)

        case_ids = [case['case_id'] for case in elderly_cases]
        primary_substance = elderly_cases[0]['primary_substance']
        reasoning_steps.append(f"Found {len(case_ids)} cases of elderly patients taking {drug_name} (Primary Substance: {primary_substance})")

        reasoning_steps.append(f"Step 2: Analyzing reactions and outcomes for {drug_name} in elderly patients")
        reactions_outcomes = self.get_reactions_and_outcomes(case_ids)
        reaction_counts = {}
        outcome_counts = {}

        for case in reactions_outcomes:
            reaction_counts[case['reaction']] = reaction_counts.get(case['reaction'], 0) + 1
            outcome_counts[case['outcome']] = outcome_counts.get(case['outcome'], 0) + 1
        
        top_reactions = sorted(reaction_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_outcomes = sorted(outcome_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        reasoning_steps.append(f"Top 3 reactions: {', '.join([f'{r[0]} ({r[1]} cases)' for r in top_reactions])}")
        reasoning_steps.append(f"Top 3 outcomes: {', '.join([f'{o[0]} ({o[1]} cases)' for o in top_outcomes])}")

        reasoning_steps.append(f"Step 3: Identifying potential drug interactions with {drug_name}")
        interacting_drugs = self.get_interacting_drugs(case_ids, primary_substance)
        top_interactions = interacting_drugs[:3]
        if top_interactions:
            reasoning_steps.append(f"Top 3 potentially interacting drugs: {', '.join([f'{d['interacting_drug']} ({d['interaction_count']} cases)' for d in top_interactions])}")
        else:
            reasoning_steps.append("No interacting drugs found.")

        total_cases = len(case_ids)
        hospitalization_risk = (outcome_counts.get('Death', 0) / total_cases) * 100 if total_cases > 0 else 0
        reasoning_steps.append(f"Step 4: Calculating risk percentages")
        reasoning_steps.append(f"Risk of death: {hospitalization_risk:.2f}%")

        reasoning_steps.append("Step 5: Generating recommendation based on analysis")
        recommendation = self.generate_recommendation(drug_name, top_reactions, top_outcomes, top_interactions, hospitalization_risk)
        reasoning_steps.append(f"Recommendation: {recommendation}")

        return "\n".join(reasoning_steps)

    def generate_recommendation(self, drug_name: str, top_reactions: List, top_outcomes: List, top_interactions: List, hospitalization_risk: float) -> str:
        recommendation = f"Based on the analysis of elderly patients taking {drug_name}:\n"
        recommendation += f"1. Common reactions include {', '.join([r[0] for r in top_reactions])}. Monitor patients for these symptoms.\n"
        recommendation += f"2. The risk of death is approximately {hospitalization_risk:.2f}%.\n"
        if top_interactions:
            recommendation += f"3. Be cautious when co-prescribing with {', '.join([d['interacting_drug'] for d in top_interactions])}, as these drugs were frequently associated with adverse events.\n"
        recommendation += f"4. Consider alternative therapies if the patient is at high risk, or ensure close monitoring during treatment."
        return recommendation

    def generate_ai_insight(self, analysis: str) -> str:
        # Use the existing authentication method
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Customizing the prompt to provide more specific instructions on shaping the AI's response
        prompt = (
            f"Given the following analysis of drug reactions for elderly patients taking COSENTYX (SECUKINUMAB), "
            "generate a detailed medical insight. The analysis includes reactions, outcomes, and risk factors. "
            "Focus on providing a structured, clinically relevant interpretation of the data with emphasis on adverse "
            "reactions like falls, aortic occlusion, cerebrovascular accidents, and other serious outcomes. "
            "Offer insights on potential risks, possible drug interactions, and healthcare recommendations for elderly patients. "
            "Make sure the response is practical and actionable for healthcare providers to assess and manage patient safety. "
            "Do not just repeat the data, but offer a thoughtful assessment of its significance and potential clinical implications. "
            "\n\nAnalysis:\n"
            f"{analysis}"
        )

        # Generate the content using the customized prompt
        response = model.generate_content(prompt)

        return response.text



def main():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    pal_system = HealthcarePALSystem(uri, user, password, gemini_api_key)

    try:
        drug_name = input("Enter the name of the drug prescribed to an elderly patient: ")
        analysis = pal_system.analyze_drug_for_elderly(drug_name)
        print("\nAnalysis of Drug for Elderly Patients:")
        print(analysis)

        # Generate AI insight based on the drug analysis
        ai_insight = pal_system.generate_ai_insight(analysis)
        print("\nAI-Generated Insight:")
        print(ai_insight)

    finally:
        pal_system.close()

if __name__ == "__main__":
    main()
