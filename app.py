# app.py
import streamlit as st
from main import AIUseGenerator

st.set_page_config(page_title="AI Use Case Generator", layout="wide")

def main():
    st.title("AI/ML Use Case Generator")
    st.markdown("""
    This tool analyzes companies and industries to generate practical AI/ML use cases and implementation resources.
    """)

    company_name = st.text_input("Enter Company/Industry Name")
    
    if st.button("Generate Analysis", type="primary"):
        if company_name:
            with st.spinner("Analyzing... This might take a few minutes."):
                try:
                    generator = AIUseGenerator()
                    result = generator.analyze_company(company_name)
                    
                    # Display results in tabs
                    tab1, tab2, tab3 = st.tabs(["Market Research", "Use Cases", "Resources"])
                    
                    with tab1:
                        st.markdown("## Market Research Summary")
                        market_research = result.split('## AI/ML Use Cases')[0]
                        st.markdown(market_research)
                    
                    with tab2:
                        st.markdown("## AI/ML Use Cases")
                        use_cases = result.split('## AI/ML Use Cases')[1].split('## Implementation Resources')[0]
                        st.markdown(use_cases)
                    
                    with tab3:
                        st.markdown("## Implementation Resources")
                        resources = result.split('## Implementation Resources')[1]
                        st.markdown(resources)
                    
                    # Add download button
                    st.download_button(
                        label="Download Complete Analysis",
                        data=result,
                        file_name=f"{company_name}_analysis.md",
                        mime="text/markdown"
                    )
                    
                    st.success("Analysis completed successfully!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a company name")

if __name__ == "__main__":
    main()