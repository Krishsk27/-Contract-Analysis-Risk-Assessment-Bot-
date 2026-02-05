import json
import requests
import re

class ContractAnalyzer:
    def __init__(self):
        # Default to local Ollama
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "llama3" 
        print(f"✅ Local AI Engine initialized using {self.model}")

    def _clean_json(self, raw_text):
        try:
            return json.loads(raw_text)
        except:
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except:
                    pass
            return None

    def _get_system_prompt(self):
        return """
        You are a Senior Legal Consultant. Analyze the contract and output strict JSON.

        1. CRITICAL FOR PARTIES: 
           Extract full legal names of all parties. If generic (e.g., "The Employer"), infer them from the signature block or first page.
        
        2. CRITICAL FOR "executive_advice":
           Write a specific, actionable paragraph. Tell the user exactly how to fix the risks found in THIS contract. 
           - Suggest specific alternatives (e.g., "Change notice period to 30 days").
           - Quote specific amounts or clauses to change.
           
        3. CRITICAL FOR RISKS:
           Score risks from 0-100 based on Indian Law (ICA 1872).

        Output strict JSON only.
        """

    def analyze_contract(self, contract_text, language="English"):
        prompt = f"""
        {self._get_system_prompt()}
        
        Analyze this contract text.
        Target Language: {language}
        
        REQUIRED JSON STRUCTURE:
        {{
            "contract_type": "String",
            "parties": ["Party A", "Party B"], 
            "risk_score": Integer (0-100),
            "overall_risk_level": "Low/Medium/High",
            "summary": "String (Brief overview)",
            "executive_advice": "String (YOUR STRATEGIC ADVICE PARAGRAPH HERE)",
            "clauses": [
                {{ "title": "String", "risk_level": "High/Medium/Low", "explanation": "String", "recommendation": "String", "original_text": "String" }}
            ],
            "missing_clauses": ["String"],
            "compliance_check": {{ "status": "Pass/Fail", "notes": "String" }}
        }}

        CONTRACT TEXT:
        {contract_text}
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.2, "num_ctx": 8192}
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=180)
            response.raise_for_status()
            parsed_data = self._clean_json(response.json().get("response", ""))
            
            if not parsed_data:
                return {"error": "Failed to parse JSON", "raw_text": response.json().get("response", "")[:200]}
                
            return parsed_data

        except Exception as e:
            return {"error": f"Local AI Error: {str(e)}"}

    def generate_template(self, contract_type, requirements=""):
        # This keeps your Template Generator logic working
        prompt = f"Act as a Legal Expert. Write a {contract_type}. Requirements: {requirements}. Output plain text."
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        try:
            return requests.post(self.api_url, json=payload, timeout=120).json().get("response", "Error")
        except Exception as e:
            return str(e)