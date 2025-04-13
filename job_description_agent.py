import os
from langchain_google_genai import ChatGoogleGenerativeAI

class JobDescriptionAgent:
    def __init__(self, api_key):
        os.environ["GOOGLE_API_KEY"] = api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)
    
    def generate_job_description(self, job_role, industry, experience_level, key_skills, 
                                company_name, company_specialization):
        """Generate a comprehensive job description based on provided parameters"""
        prompt = f"""Create a detailed job description for a {job_role} position in the {industry} industry.
        
        Company Name: {company_name}
        Company Specialization: {company_specialization}
        Experience Level: {experience_level}
        Key Skills: {key_skills}
        
        Include these sections:
        - Company Overview (Include details about {company_name} and its specialization in {company_specialization})
        - Dont include location details
        - Role Description
        - Responsibilities
        - Requirements
        - Preferred Qualifications
        - Benefits
        
        Make it professional, detailed, and appealing to qualified candidates."""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def refine_job_description(self, existing_jd, refinement_instructions, 
                              company_name=None, company_specialization=None):
        """Refine an existing job description based on provided instructions"""
        company_context = ""
        if company_name and company_specialization:
            company_context = f"""
            Also ensure the job description correctly represents:
            Company Name: {company_name}
            Company Specialization: {company_specialization}
            """
            
        prompt = f"""Refine the following job description according to these instructions: 
        {refinement_instructions}
        {company_context}
        
        ORIGINAL JOB DESCRIPTION:
        {existing_jd}
        
        Return the complete refined job description."""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def validate_job_description(self, job_description):
        """Check job description for common issues like bias, clarity, completeness"""
        prompt = f"""Analyze the following job description and identify any potential issues:
        - Check for gender or age bias in language
        - Identify vague requirements or responsibilities
        - Highlight any missing essential sections
        - Suggest improvements for clarity and appeal
        
        JOB DESCRIPTION:
        {job_description}
        
        Provide a structured analysis with specific recommendations for improvement."""
        
        response = self.llm.invoke(prompt)
        return response.content