import streamlit as st
from main import AIUseGenerator

st.set_page_config(page_title="AI Use Case Generator", layout="wide")

def main():
    st.title("AI Use Case Generator")
    st.markdown("""
    Generate basic AI/ML use cases for your industry.
    """)

    company_name = st.text_input("Enter Company/Industry Name")
    
    if st.button("Generate Analysis", type="primary"):
        if company_name:
            with st.spinner("Analyzing... Please wait..."):
                try:
                    generator = AIUseGenerator()
                    result = generator.analyze_company(company_name)
                    
                    # Display results
                    st.markdown(result)
                    
                    # Add download button
                    st.download_button(
                        label="Download Analysis",
                        data=result,
                        file_name=f"{company_name}_analysis.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error("An error occurred, but here's a basic analysis:")
                    generator = AIUseGenerator()
                    result = generator.get_basic_output(company_name)
                    st.markdown(result)
        else:
            st.warning("Please enter a company name")

if __name__ == "__main__":
    main()