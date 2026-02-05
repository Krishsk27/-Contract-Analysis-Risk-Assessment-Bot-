import streamlit as st
from src.llm_engine import ContractAnalyzer

st.title("📝 Standardized Contract Templates")

contract_type = st.selectbox("Select Contract Type", 
    ["Employment Agreement", "NDA", "Service Agreement", "Lease Deed"])

if st.button("Generate Template"):
    analyzer = ContractAnalyzer()
    # You would implement a prompt specifically for generation here
    template_text = analyzer.generate_template(contract_type)
    st.text_area("Template Preview", template_text, height=400)
    st.download_button("Download Template", template_text, file_name=f"{contract_type}.txt")