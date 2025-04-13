# # main.py
# import streamlit as st
# import pandas as pd
# import os
# import json
# from datetime import datetime

# # Import our agent modules
# from job_description_agent import JobDescriptionAgent
# from resume_parser_agent import ResumeParserAgent
# from candidate_analyzer_agent import CandidateAnalyzerAgent
# from communication_agent import CommunicationAgent

# # Set page configuration
# st.set_page_config(
#     page_title="Agentic HR Assistant Pro",
#     page_icon="👔",
#     layout="wide"
# )

# # Initialize session state variables
# if "job_description" not in st.session_state:
#     st.session_state.job_description = ""
# if "resumes" not in st.session_state:
#     st.session_state.resumes = {}
# if "candidates_data" not in st.session_state:
#     st.session_state.candidates_data = pd.DataFrame(
#         columns=["Name", "Email", "Skills Match (%)", 
#                  "Experience Match (%)", "Overall Score", 
#                  "Key Skills", "Strengths", "Weaknesses", 
#                  "Recommendation", "Status"])
# if "emails_sent" not in st.session_state:
#     st.session_state.emails_sent = {}

# # Sidebar for API Keys
# with st.sidebar:
#     st.title("API Configuration")
    
#     google_api_key = st.text_input("Google Gemini API Key", type="password")
#     sendgrid_api_key = st.text_input("SendGrid API Key", type="password")
    
#     st.markdown("---")
#     st.markdown("### How to use")
#     st.markdown("""
#     1. Enter API keys in the sidebar
#     2. Generate or paste a job description
#     3. Upload candidate resumes (PDF)
#     4. Review the automated analysis
#     5. Approve or reject candidates
#     6. Send interview invitations
#     """)

# # Initialize agents if API keys are provided
# agents_initialized = False
# if google_api_key:
#     try:
#         # Initialize all agents
#         job_description_agent = JobDescriptionAgent(google_api_key)
#         resume_parser = ResumeParserAgent()
#         candidate_analyzer = CandidateAnalyzerAgent(google_api_key)
#         communication_agent = CommunicationAgent(google_api_key, sendgrid_api_key if sendgrid_api_key else None)
        
#         agents_initialized = True
#     except Exception as e:
#         st.sidebar.error(f"Error initializing agents: {e}")
# else:
#     st.sidebar.warning("Please enter your Google Gemini API Key to continue")

# # Main app interface
# st.title("Agentic HR Assistant Pro")
# st.markdown("Streamline your recruitment process with AI-powered assistance")

# # Create tabs for the workflow
# tab1, tab2, tab3 = st.tabs(["Job Description", "Resume Analysis", "Communication"])

# # JOB DESCRIPTION AGENT
# with tab1:
#     st.header("Job Description Agent")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         job_role = st.text_input("Job Role", placeholder="e.g., Senior Python Developer")
        
#     with col2:
#         action_type = st.selectbox(
#             "Action",
#             ["Generate New", "Refine Existing"]
#         )
    
#     # Company information (new section)
#     company_col1, company_col2 = st.columns(2)
#     with company_col1:
#         company_name = st.text_input("Company Name", placeholder="Enter your company name")
#     with company_col2:
#         company_specialization = st.text_input("Company Specialization", 
#                                              placeholder="e.g., Cloud Computing Solutions, Healthcare Technology")
    
#     if action_type == "Generate New":
#         industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Education", "Manufacturing", "Retail", "Other"])
#         experience_level = st.selectbox("Experience Level", ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior (6-10 years)", "Expert (10+ years)"])
        
#         key_skills = st.text_area("Key Skills Required (comma separated)", placeholder="e.g., Python, Django, AWS, Docker")
        
#         if st.button("Generate Job Description", disabled=not agents_initialized):
#             if not company_name:
#                 st.warning("Please enter your company name to continue.")
#             else:
#                 with st.spinner("Generating comprehensive job description..."):
#                     try:
#                         st.session_state.job_description = job_description_agent.generate_job_description(
#                             job_role, industry, experience_level, key_skills,
#                             company_name, company_specialization
#                         )
#                     except Exception as e:
#                         st.error(f"Error generating job description: {str(e)}")
    
#     else:  # Refine Existing
#         existing_jd = st.text_area("Paste your existing job description", height=200)
#         refinement_instructions = st.text_area("Refinement instructions", 
#                                               placeholder="e.g., Make it more concise, add more detail about technical requirements, etc.")
        
#         if st.button("Refine Job Description", disabled=not agents_initialized):
#             if existing_jd:
#                 with st.spinner("Refining job description..."):
#                     try:
#                         st.session_state.job_description = job_description_agent.refine_job_description(
#                             existing_jd, refinement_instructions,
#                             company_name, company_specialization
#                         )
#                     except Exception as e:
#                         st.error(f"Error refining job description: {str(e)}")
#             else:
#                 st.warning("Please paste an existing job description to refine.")
    
#     # Display the current job description with edit capability
#     if st.session_state.job_description:
#         st.markdown("### Current Job Description")
        
#         # Add validation option
#         col1, col2 = st.columns([4, 1])
#         with col2:
#             if st.button("Validate JD", disabled=not agents_initialized):
#                 with st.spinner("Validating job description..."):
#                     validation_results = job_description_agent.validate_job_description(
#                         st.session_state.job_description
#                     )
#                     st.info("Validation Results:")
#                     st.markdown(validation_results)
        
#         # Make the job description editable
#         edited_jd = st.text_area("Edit Job Description if needed:", 
#                                value=st.session_state.job_description,
#                                height=400,
#                                key="editable_job_description")
        
#         # Update the job description in session state if edited
#         if edited_jd != st.session_state.job_description:
#             st.session_state.job_description = edited_jd
        
#         if st.button("Confirm and Continue"):
#             st.success("Job description confirmed! Please proceed to the Resume Analysis tab.")

# # RESUME PARSER AND ANALYZER
# with tab2:
#     st.header("Resume Processing")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         uploaded_files = st.file_uploader("Upload candidate resumes (PDF)", 
#                                          accept_multiple_files=True, 
#                                          type=["pdf"])
    
#     with col2:
#         if st.button("Process Resumes", disabled=not agents_initialized or not st.session_state.job_description):
#             if uploaded_files:
#                 progress_bar = st.progress(0)
#                 status_text = st.empty()
                
#                 # Clear previous data
#                 new_candidates_data = []
                
#                 for i, file in enumerate(uploaded_files):
#                     try:
#                         status_text.text(f"Processing {file.name}...")
                        
#                         # Extract text from PDF using Resume Parser Agent
#                         resume_text = resume_parser.extract_text_from_pdf(file)
                        
#                         # Store in session state
#                         st.session_state.resumes[file.name] = resume_text
                        
#                         # Use Candidate Analyzer Agent to analyze the resume
#                         status_text.text(f"Analyzing {file.name}...")
                        
#                         analysis_data = candidate_analyzer.analyze_resume(
#                             resume_text, 
#                             st.session_state.job_description
#                         )
                        
#                         # Backup Email Extraction with Regex if missing
#                         if not analysis_data.get("email") or analysis_data.get("email") == "":
#                             email = resume_parser.extract_email(resume_text)
#                             if email:
#                                 analysis_data["email"] = email
#                             else:
#                                 analysis_data["email"] = "Not found"
                        
#                         # Add to candidates data
#                         new_candidates_data.append({
#                             "Name": analysis_data.get("name", "Unknown"),
#                             "Email": analysis_data.get("email", "Not found"),
#                             "Skills Match (%)": analysis_data.get("skills_match_percentage", 0),
#                             "Experience Match (%)": analysis_data.get("experience_match_percentage", 0),
#                             "Overall Score": analysis_data.get("overall_score", 0),
#                             "Key Skills": ", ".join(analysis_data.get("key_skills", [])),
#                             "Strengths": ", ".join(analysis_data.get("strengths", [])),
#                             "Weaknesses": ", ".join(analysis_data.get("weaknesses", [])),
#                             "Recommendation": analysis_data.get("recommendation", ""),
#                             "Status": "Pending"
#                         })
                        
#                         # Update progress bar
#                         progress_bar.progress((i + 1) / len(uploaded_files))
                    
#                     except Exception as e:
#                         st.error(f"Error processing {file.name}: {str(e)}")
                
#                 # Add to the existing DataFrame
#                 new_df = pd.DataFrame(new_candidates_data)
#                 st.session_state.candidates_data = pd.concat([st.session_state.candidates_data, new_df], ignore_index=True)
                
#                 status_text.text("Processing complete!")
#                 st.success(f"Successfully processed {len(uploaded_files)} resumes")
#             else:
#                 st.warning("Please upload resume files (PDF format)")
    
#     # Display candidate analysis results in an editable table
#     if not st.session_state.candidates_data.empty:
#         st.markdown("### Candidate Analysis Results")
        
#         # Add filters
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             min_score = st.slider("Minimum Overall Score", 0, 100, 0)
#         with col2:
#             recommendation_filter = st.multiselect(
#                 "Filter by Recommendation", 
#                 options=["Strong Hire", "Potential Hire", "Consider for Different Role", "Reject"],
#                 default=["Strong Hire", "Potential Hire"]
#             )
#         with col3:
#             status_filter = st.multiselect(
#                 "Filter by Status",
#                 options=["Pending", "Approved", "Rejected"],
#                 default=["Pending", "Approved"]
#             )
        
#         # Apply filters
#         filtered_df = st.session_state.candidates_data[
#             (st.session_state.candidates_data["Overall Score"] >= min_score) &
#             (st.session_state.candidates_data["Recommendation"].isin(recommendation_filter)) &
#             (st.session_state.candidates_data["Status"].isin(status_filter))
#         ]
        
#         # Create an editable data table
#         edited_df = st.data_editor(
#             filtered_df,
#             column_config={
#                 "Status": st.column_config.SelectboxColumn(
#                     "Status",
#                     help="Select candidate status",
#                     width="medium",
#                     options=["Pending", "Approved", "Rejected"],
#                 ),
#                 "Overall Score": st.column_config.ProgressColumn(
#                     "Overall Score",
#                     help="Candidate's overall match score",
#                     min_value=0,
#                     max_value=100,
#                     format="%d%%",
#                 )
#             },
#             use_container_width=True,
#             hide_index=True,
#         )
        
#         # Update the main dataframe with edited values
#         for i, row in edited_df.iterrows():
#             idx = st.session_state.candidates_data.index[
#                 st.session_state.candidates_data["Name"] == row["Name"]
#             ].tolist()
#             if idx:
#                 st.session_state.candidates_data.loc[idx[0], "Status"] = row["Status"]

# # COMMUNICATION AGENT
# with tab3:
#     st.header("Communication Agent")
    
#     # Get approved candidates who haven't been sent emails
#     approved_candidates = st.session_state.candidates_data[
#         (st.session_state.candidates_data["Status"] == "Approved") & 
#         (~st.session_state.candidates_data["Email"].isin(st.session_state.emails_sent.keys()))
#     ]
    
#     if not approved_candidates.empty:
#         st.markdown(f"### {len(approved_candidates)} Candidates Ready for Interview Invitation")
        
#         # Interview scheduling information
#         col1, col2 = st.columns(2)
        
#         with col1:
#             interview_date = st.date_input("Interview Date")
#             interview_location = st.text_input("Interview Location", placeholder="Office address or Zoom link")
        
#         with col2:
#             interview_format = st.selectbox("Interview Format", ["In-person", "Video Call", "Phone Call"])
#             email_tone = st.selectbox("Email Tone", ["Professional", "Friendly", "Enthusiastic"])
        
#         interviewer_name = st.text_input("Interviewer Name")
#         additional_details = st.text_area("Additional Details (optional)", placeholder="Any special instructions for candidates")
        
#         if st.button("Generate & Preview Emails", disabled=not agents_initialized):
#             if sendgrid_api_key:
#                 # Generate emails for all approved candidates
#                 for _, candidate in approved_candidates.iterrows():
#                     with st.expander(f"Email for {candidate['Name']}"):
#                         try:
#                             # Prepare candidate info in the format expected by the communication agent
#                             candidate_info = {
#                                 "name": candidate['Name'],
#                                 "key_skills": candidate['Key Skills'].split(", "),
#                                 "strengths": candidate['Strengths'].split(", ")
#                             }
                            
#                             # Prepare interview details
#                             interview_details = {
#                                 "date": interview_date,
#                                 "format": interview_format,
#                                 "location": interview_location,
#                                 "interviewer": interviewer_name,
#                                 "additional_details": additional_details
#                             }
                            
#                             # Generate the email
#                             email_content = communication_agent.generate_interview_email(
#                                 candidate_info,
#                                 st.session_state.job_description,
#                                 interview_details,
#                                 email_tone
#                             )
                            
#                             # Display email preview with editable fields
#                             st.markdown("#### Subject:")
#                             email_subject_edit = st.text_input("Edit Subject", email_content["subject"], key=f"subject_{candidate['Name']}")
                            
#                             st.markdown("#### Body:")
#                             email_body_edit = st.text_area("Edit Body", email_content["body"], height=400, key=f"body_{candidate['Name']}")
                            
#                             # Store the email content for sending
#                             st.session_state.emails_sent[candidate['Email']] = {
#                                 "subject": email_subject_edit,
#                                 "body": email_body_edit,
#                                 "sent": False,
#                                 "candidate_name": candidate['Name']
#                             }
                        
#                         except Exception as e:
#                             st.error(f"Error generating email: {str(e)}")
                
#                 if st.button("Send All Emails"):
#                     # Use Communication Agent to send emails
#                     try:
#                         for email, content in st.session_state.emails_sent.items():
#                             if not content["sent"]:
#                                 result = communication_agent.send_email(
#                                     to_email=email,
#                                     subject=content["subject"],
#                                     html_content=content["body"],
#                                     sender_name=interviewer_name if interviewer_name else None
#                                 )
                                
#                                 if result["success"]:
#                                     # Mark as sent
#                                     st.session_state.emails_sent[email]["sent"] = True
#                                 else:
#                                     st.error(f"Error sending email to {email}: {result['message']}")
                        
#                         st.success(f"Successfully sent {len([e for e in st.session_state.emails_sent.values() if e['sent']])} emails!")
                    
#                     except Exception as e:
#                         st.error(f"Error sending emails: {str(e)}")
#             else:
#                 st.warning("Please enter your SendGrid API Key in the sidebar to send emails")
#     else:
#         st.info("No approved candidates ready for email communication. Please approve candidates in the Resume Analysis tab.")

# # Email sending history
# if st.session_state.emails_sent:
#     with tab3:
#         st.markdown("### Email History")
        
#         email_history = []
#         for email, content in st.session_state.emails_sent.items():
#             email_history.append({
#                 "Candidate": content["candidate_name"],
#                 "Email Address": email,
#                 "Subject": content["subject"],
#                 "Status": "Sent" if content["sent"] else "Pending"
#             })
        
#         st.dataframe(pd.DataFrame(email_history), use_container_width=True, hide_index=True)

# # Footer
# st.markdown("---")
# st.markdown("Agentic HR Assistant Pro | Powered by AI")



# # main.py
# import streamlit as st
# import pandas as pd
# import os
# import json
# from datetime import datetime

# # Import our agent modules
# from job_description_agent import JobDescriptionAgent
# from resume_parser_agent import ResumeParserAgent
# from candidate_analyzer_agent import CandidateAnalyzerAgent
# from communication_agent import CommunicationAgent

# # Set page configuration
# st.set_page_config(
#     page_title="Agentic HR Assistant Pro",
#     page_icon="👔",
#     layout="wide"
# )

# # Initialize session state variables
# if "job_description" not in st.session_state:
#     st.session_state.job_description = ""
# if "resumes" not in st.session_state:
#     st.session_state.resumes = {}
# if "candidates_data" not in st.session_state:
#     st.session_state.candidates_data = pd.DataFrame(
#         columns=["Name", "Email", "Skills Match (%)", 
#                  "Experience Match (%)", "Overall Score", 
#                  "Key Skills", "Strengths", "Weaknesses", 
#                  "Recommendation", "Status", "Automated Decision"])
# if "emails_sent" not in st.session_state:
#     st.session_state.emails_sent = {}
# if "auto_processed" not in st.session_state:
#     st.session_state.auto_processed = False
# if "available_interview_slots" not in st.session_state:
#     # Initialize with some default interview slots
#     st.session_state.available_interview_slots = [
#         {"id": 1, "date": "2025-04-20", "time": "10:00 AM", "available": True},
#         {"id": 2, "date": "2025-04-20", "time": "2:00 PM", "available": True},
#         {"id": 3, "date": "2025-04-21", "time": "11:00 AM", "available": True},
#         {"id": 4, "date": "2025-04-21", "time": "3:00 PM", "available": True},
#         {"id": 5, "date": "2025-04-22", "time": "9:00 AM", "available": True}
#     ]

# # Sidebar for API Keys
# with st.sidebar:
#     st.title("API Configuration")
    
#     google_api_key = st.text_input("Google Gemini API Key", type="password")
#     sendgrid_api_key = st.text_input("SendGrid API Key", type="password")
    
#     # Automation settings
#     st.markdown("---")
#     st.markdown("### Automation Settings")
#     auto_approve_threshold = st.slider("Auto-approve candidates with score above:", 40, 90, 50)
#     auto_email_enabled = st.checkbox("Auto-generate interview emails", value=True)
#     auto_send_emails = st.checkbox("Auto-send interview emails", value=False)
    
#     st.markdown("---")
#     st.markdown("### How to use")
#     st.markdown("""
#     1. Enter API keys in the sidebar
#     2. Generate or paste a job description
#     3. Upload candidate resumes (PDF)
#     4. Review the automated analysis
#     5. The system will automatically approve candidates above threshold
#     6. Interview invitations will be auto-generated based on settings
#     """)

# # Initialize agents if API keys are provided
# agents_initialized = False
# if google_api_key:
#     try:
#         # Initialize all agents
#         job_description_agent = JobDescriptionAgent(google_api_key)
#         resume_parser = ResumeParserAgent()
#         candidate_analyzer = CandidateAnalyzerAgent(google_api_key)
#         communication_agent = CommunicationAgent(google_api_key, sendgrid_api_key if sendgrid_api_key else None)
        
#         agents_initialized = True
#     except Exception as e:
#         st.sidebar.error(f"Error initializing agents: {e}")
# else:
#     st.sidebar.warning("Please enter your Google Gemini API Key to continue")

# # Main app interface
# st.title("Agentic HR Assistant Pro")
# st.markdown("Streamline your recruitment process with AI-powered assistance")

# # Create tabs for the workflow
# tab1, tab2, tab3 = st.tabs(["Job Description", "Resume Analysis", "Communication"])

# # JOB DESCRIPTION AGENT
# with tab1:
#     st.header("Job Description Agent")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         job_role = st.text_input("Job Role", placeholder="e.g., Senior Python Developer")
        
#     with col2:
#         action_type = st.selectbox(
#             "Action",
#             ["Generate New", "Refine Existing"]
#         )
    
#     # Company information (new section)
#     company_col1, company_col2 = st.columns(2)
#     with company_col1:
#         company_name = st.text_input("Company Name", placeholder="Enter your company name")
#     with company_col2:
#         company_specialization = st.text_input("Company Specialization", 
#                                              placeholder="e.g., Cloud Computing Solutions, Healthcare Technology")
    
#     if action_type == "Generate New":
#         industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Education", "Manufacturing", "Retail", "Other"])
#         experience_level = st.selectbox("Experience Level", ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior (6-10 years)", "Expert (10+ years)"])
        
#         key_skills = st.text_area("Key Skills Required (comma separated)", placeholder="e.g., Python, Django, AWS, Docker")
        
#         if st.button("Generate Job Description", disabled=not agents_initialized):
#             if not company_name:
#                 st.warning("Please enter your company name to continue.")
#             else:
#                 with st.spinner("Generating comprehensive job description..."):
#                     try:
#                         st.session_state.job_description = job_description_agent.generate_job_description(
#                             job_role, industry, experience_level, key_skills,
#                             company_name, company_specialization
#                         )
#                     except Exception as e:
#                         st.error(f"Error generating job description: {str(e)}")
    
#     else:  # Refine Existing
#         existing_jd = st.text_area("Paste your existing job description", height=200)
#         refinement_instructions = st.text_area("Refinement instructions", 
#                                               placeholder="e.g., Make it more concise, add more detail about technical requirements, etc.")
        
#         if st.button("Refine Job Description", disabled=not agents_initialized):
#             if existing_jd:
#                 with st.spinner("Refining job description..."):
#                     try:
#                         st.session_state.job_description = job_description_agent.refine_job_description(
#                             existing_jd, refinement_instructions,
#                             company_name, company_specialization
#                         )
#                     except Exception as e:
#                         st.error(f"Error refining job description: {str(e)}")
#             else:
#                 st.warning("Please paste an existing job description to refine.")
    
#     # Display the current job description with edit capability
#     if st.session_state.job_description:
#         st.markdown("### Current Job Description")
        
#         # # Add validation option
#         # col1, col2 = st.columns([4, 1])
#         # with col2:
#         #     if st.button("Validate JD", disabled=not agents_initialized):
#         #         with st.spinner("Validating job description..."):
#         #             validation_results = job_description_agent.validate_job_description(
#         #                 st.session_state.job_description
#         #             )
#         #             st.info("Validation Results:")
#         #             st.markdown(validation_results)
        
#         # Make the job description editable
#         edited_jd = st.text_area("Edit Job Description if needed:", 
#                                value=st.session_state.job_description,
#                                height=400,
#                                key="editable_job_description")
        
#         # Update the job description in session state if edited
#         if edited_jd != st.session_state.job_description:
#             st.session_state.job_description = edited_jd

#         # Add validation option
#         col1, col2 = st.columns([1, 1])
#         with col1:
#             if st.button("Validate JD", disabled=not agents_initialized):
#                 with st.spinner("Validating job description..."):
#                     validation_results = job_description_agent.validate_job_description(
#                         st.session_state.job_description
#                     )
#                     st.info("Validation Results:")
#                     st.markdown(validation_results)
        
#         if st.button("Confirm and Continue"):
#             st.success("Job description confirmed! Please proceed to the Resume Analysis tab.")

# # RESUME PARSER AND ANALYZER
# with tab2:
#     st.header("Resume Processing")
    
#     # Add automated decision mode indicator
#     st.markdown(f"**Auto-Approval Mode**: Candidates with score >{auto_approve_threshold}% will be automatically approved")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         uploaded_files = st.file_uploader("Upload candidate resumes (PDF)", 
#                                          accept_multiple_files=True, 
#                                          type=["pdf"])
    
#     with col2:
#         if st.button("Process Resumes", disabled=not agents_initialized or not st.session_state.job_description):
#             if uploaded_files:
#                 progress_bar = st.progress(0)
#                 status_text = st.empty()
                
#                 # Clear previous data
#                 new_candidates_data = []
                
#                 for i, file in enumerate(uploaded_files):
#                     try:
#                         status_text.text(f"Processing {file.name}...")
                        
#                         # Extract text from PDF using Resume Parser Agent
#                         resume_text = resume_parser.extract_text_from_pdf(file)
                        
#                         # Store in session state
#                         st.session_state.resumes[file.name] = resume_text
                        
#                         # Use Candidate Analyzer Agent to analyze the resume
#                         status_text.text(f"Analyzing {file.name}...")
                        
#                         analysis_data = candidate_analyzer.analyze_resume(
#                             resume_text, 
#                             st.session_state.job_description
#                         )
                        
#                         # Backup Email Extraction with Regex if missing
#                         if not analysis_data.get("email") or analysis_data.get("email") == "":
#                             email = resume_parser.extract_email(resume_text)
#                             if email:
#                                 analysis_data["email"] = email
#                             else:
#                                 analysis_data["email"] = "Not found"
                        
#                         # Make automated decision based on configured threshold
#                         auto_decision = "Pending"
#                         decision_reason = ""
                        
#                         if analysis_data.get("overall_score", 0) >= auto_approve_threshold:
#                             auto_decision = "Approved"
#                             decision_reason = f"Auto-approved: Score {analysis_data.get('overall_score')}% meets threshold ({auto_approve_threshold}%)"
#                         else:
#                             auto_decision = "Pending"
#                             decision_reason = f"Manual review needed: Score {analysis_data.get('overall_score')}% below threshold ({auto_approve_threshold}%)"
                        
#                         # Add to candidates data
#                         new_candidates_data.append({
#                             "Name": analysis_data.get("name", "Unknown"),
#                             "Email": analysis_data.get("email", "Not found"),
#                             "Skills Match (%)": analysis_data.get("skills_match_percentage", 0),
#                             "Experience Match (%)": analysis_data.get("experience_match_percentage", 0),
#                             "Overall Score": analysis_data.get("overall_score", 0),
#                             "Key Skills": ", ".join(analysis_data.get("key_skills", [])),
#                             "Strengths": ", ".join(analysis_data.get("strengths", [])),
#                             "Weaknesses": ", ".join(analysis_data.get("weaknesses", [])),
#                             "Recommendation": analysis_data.get("recommendation", ""),
#                             "Status": auto_decision,
#                             "Automated Decision": decision_reason
#                         })
                        
#                         # Update progress bar
#                         progress_bar.progress((i + 1) / len(uploaded_files))
                    
#                     except Exception as e:
#                         st.error(f"Error processing {file.name}: {str(e)}")
                
#                 # Add to the existing DataFrame
#                 new_df = pd.DataFrame(new_candidates_data)
#                 st.session_state.candidates_data = pd.concat([st.session_state.candidates_data, new_df], ignore_index=True)
                
#                 status_text.text("Processing complete!")
                
#                 # Flag that we've processed candidates but haven't generated emails yet
#                 st.session_state.auto_processed = True
                
#                 st.success(f"Successfully processed {len(uploaded_files)} resumes")
                
#                 # Auto-generate emails for approved candidates if enabled
#                 if auto_email_enabled:
#                     st.info("Automatically generating interview emails for approved candidates...")
#                     # This will be handled in the Communication tab when we switch to it
#             else:
#                 st.warning("Please upload resume files (PDF format)")
    
#     # Display candidate analysis results in an editable table
#     if not st.session_state.candidates_data.empty:
#         st.markdown("### Candidate Analysis Results")
        
#         # Add filters
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             min_score = st.slider("Minimum Overall Score", 0, 100, 0)
#         with col2:
#             recommendation_filter = st.multiselect(
#                 "Filter by Recommendation", 
#                 options=["Strong Hire", "Potential Hire", "Consider for Different Role", "Reject"],
#                 default=["Strong Hire", "Potential Hire"]
#             )
#         with col3:
#             status_filter = st.multiselect(
#                 "Filter by Status",
#                 options=["Pending", "Approved", "Rejected"],
#                 default=["Pending", "Approved"]
#             )
        
#         # Apply filters
#         filtered_df = st.session_state.candidates_data[
#             (st.session_state.candidates_data["Overall Score"] >= min_score) &
#             (st.session_state.candidates_data["Recommendation"].isin(recommendation_filter)) &
#             (st.session_state.candidates_data["Status"].isin(status_filter))
#         ]
        
#         # Create an editable data table
#         edited_df = st.data_editor(
#             filtered_df,
#             column_config={
#                 "Status": st.column_config.SelectboxColumn(
#                     "Status",
#                     help="Select candidate status",
#                     width="medium",
#                     options=["Pending", "Approved", "Rejected"],
#                 ),
#                 "Overall Score": st.column_config.ProgressColumn(
#                     "Overall Score",
#                     help="Candidate's overall match score",
#                     min_value=0,
#                     max_value=100,
#                     format="%d%%",
#                 )
#             },
#             use_container_width=True,
#             hide_index=True,
#         )
        
#         # Update the main dataframe with edited values
#         for i, row in edited_df.iterrows():
#             idx = st.session_state.candidates_data.index[
#                 st.session_state.candidates_data["Name"] == row["Name"]
#             ].tolist()
#             if idx:
#                 st.session_state.candidates_data.loc[idx[0], "Status"] = row["Status"]
        
#         # Show the automated analysis summary
#         approved_count = len(st.session_state.candidates_data[st.session_state.candidates_data["Status"] == "Approved"])
#         pending_count = len(st.session_state.candidates_data[st.session_state.candidates_data["Status"] == "Pending"])
#         rejected_count = len(st.session_state.candidates_data[st.session_state.candidates_data["Status"] == "Rejected"])
        
#         st.markdown(f"### Analysis Summary")
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Approved Candidates", approved_count)
#         col2.metric("Pending Review", pending_count)
#         col3.metric("Rejected Candidates", rejected_count)

# # COMMUNICATION AGENT
# with tab3:
#     st.header("Communication Agent")
    
#     # Process auto-approved candidates if flag is set and auto-email is enabled
#     if st.session_state.auto_processed and auto_email_enabled:
#         # Reset the flag
#         st.session_state.auto_processed = False
        
#         # Get newly approved candidates who haven't been sent emails
#         auto_approved_candidates = st.session_state.candidates_data[
#             (st.session_state.candidates_data["Status"] == "Approved") & 
#             (~st.session_state.candidates_data["Email"].isin(st.session_state.emails_sent.keys()))
#         ]
        
#         if not auto_approved_candidates.empty:
#             st.success(f"🤖 Auto-generating emails for {len(auto_approved_candidates)} approved candidates")
            
#             # Get the default interview settings
#             # In a real app, these could be pulled from company settings
#             default_interview_details = {
#                 "date": datetime.now().strftime("%Y-%m-%d"),
#                 "format": "Video Call",
#                 "location": "Zoom (link will be sent upon confirmation)",
#                 "interviewer": company_name + " Hiring Team",
#                 "additional_details": "Please prepare to discuss your experiences and have questions ready about the role."
#             }
            
#             # Generate emails automatically for all auto-approved candidates
#             auto_emails_generated = 0
            
#             for _, candidate in auto_approved_candidates.iterrows():
#                 try:
#                     # Get an available interview slot
#                     available_slots = [slot for slot in st.session_state.available_interview_slots if slot["available"]]
                    
#                     if not available_slots:
#                         st.warning("No interview slots available. Please add more slots.")
#                         break
                    
#                     # Prepare candidate info
#                     candidate_info = {
#                         "name": candidate['Name'],
#                         "key_skills": candidate['Key Skills'].split(", "),
#                         "strengths": candidate['Strengths'].split(", ")
#                     }
                    
#                     # Get the best slot for this candidate using AI decision
#                     recommended_slot = candidate_analyzer.get_best_interview_time_slot(
#                         candidate_info, 
#                         available_slots
#                     )
                    
#                     # Find the slot in our list
#                     interview_slot = next((slot for slot in available_slots if slot["id"] == recommended_slot["slot_id"]), available_slots[0])
                    
#                     # Mark the slot as unavailable
#                     for i, slot in enumerate(st.session_state.available_interview_slots):
#                         if slot["id"] == interview_slot["id"]:
#                             st.session_state.available_interview_slots[i]["available"] = False
                    
#                     # Use the slot info in the interview details
#                     interview_details = default_interview_details.copy()
#                     interview_details["date"] = f"{interview_slot['date']} at {interview_slot['time']}"
                    
#                     # Generate the email
#                     email_content = communication_agent.generate_interview_email(
#                         candidate_info,
#                         st.session_state.job_description,
#                         interview_details,
#                         "Professional"
#                     )
                    
#                     # Store the email for sending
#                     st.session_state.emails_sent[candidate['Email']] = {
#                         "subject": email_content["subject"],
#                         "body": email_content["body"],
#                         "sent": False,
#                         "candidate_name": candidate['Name'],
#                         "interview_slot": interview_slot
#                     }
                    
#                     auto_emails_generated += 1
                
#                 except Exception as e:
#                     st.error(f"Error generating email for {candidate['Name']}: {str(e)}")
            
#             if auto_emails_generated > 0:
#                 st.success(f"✅ Successfully generated {auto_emails_generated} interview emails")
                
#                 # Auto-send emails if enabled
#                 if auto_send_emails and sendgrid_api_key:
#                     auto_sent_count = 0
                    
#                     for email, content in st.session_state.emails_sent.items():
#                         if not content["sent"]:
#                             try:
#                                 result = communication_agent.send_email(
#                                     to_email=email,
#                                     subject=content["subject"],
#                                     html_content=content["body"],
#                                     sender_name=default_interview_details["interviewer"]
#                                 )
                                
#                                 if result["success"]:
#                                     # Mark as sent
#                                     st.session_state.emails_sent[email]["sent"] = True
#                                     auto_sent_count += 1
#                             except Exception as e:
#                                 st.error(f"Error sending auto-email to {email}: {str(e)}")
                    
#                     if auto_sent_count > 0:
#                         st.success(f"🚀 Automatically sent {auto_sent_count} interview emails")
    
#     # Get all approved candidates who haven't been sent emails
#     approved_candidates = st.session_state.candidates_data[
#         (st.session_state.candidates_data["Status"] == "Approved") & 
#         (~st.session_state.candidates_data["Email"].isin([k for k, v in st.session_state.emails_sent.items() if v["sent"]]))
#     ]
    
#     if not approved_candidates.empty:
#         st.markdown(f"### {len(approved_candidates)} Candidates Ready for Interview Invitation")
        
#         # Interview scheduling information
#         col1, col2 = st.columns(2)
        
#         with col1:
#             interview_date = st.date_input("Interview Date")
#             interview_location = st.text_input("Interview Location", placeholder="Office address or Zoom link")
        
#         with col2:
#             interview_format = st.selectbox("Interview Format", ["In-person", "Video Call", "Phone Call"])
#             email_tone = st.selectbox("Email Tone", ["Professional", "Friendly", "Enthusiastic"])
        
#         interviewer_name = st.text_input("Interviewer Name")
#         additional_details = st.text_area("Additional Details (optional)", placeholder="Any special instructions for candidates")
        
#         if st.button("Generate & Preview Emails", disabled=not agents_initialized):
#             if sendgrid_api_key:
#                 # Generate emails for all approved candidates
#                 for _, candidate in approved_candidates.iterrows():
#                     with st.expander(f"Email for {candidate['Name']}"):
#                         try:
#                             # Prepare candidate info in the format expected by the communication agent
#                             candidate_info = {
#                                 "name": candidate['Name'],
#                                 "key_skills": candidate['Key Skills'].split(", "),
#                                 "strengths": candidate['Strengths'].split(", ")
#                             }
                            
#                             # Prepare interview details
#                             interview_details = {
#                                 "date": interview_date,
#                                 "format": interview_format,
#                                 "location": interview_location,
#                                 "interviewer": interviewer_name,
#                                 "additional_details": additional_details
#                             }
                            
#                             # Generate the email
#                             email_content = communication_agent.generate_interview_email(
#                                 candidate_info,
#                                 st.session_state.job_description,
#                                 interview_details,
#                                 email_tone
#                             )
                            
#                             # Display email preview with editable fields
#                             st.markdown("#### Subject:")
#                             email_subject_edit = st.text_input("Edit Subject", email_content["subject"], key=f"subject_{candidate['Name']}")
                            
#                             st.markdown("#### Body:")
#                             email_body_edit = st.text_area("Edit Body", email_content["body"], height=400, key=f"body_{candidate['Name']}")
                            
#                             # Store the email content for sending
#                             st.session_state.emails_sent[candidate['Email']] = {
#                                 "subject": email_subject_edit,
#                                 "body": email_body_edit,
#                                 "sent": False,
#                                 "candidate_name": candidate['Name']
#                             }
                        
#                         except Exception as e:
#                             st.error(f"Error generating email: {str(e)}")
                
#                 if st.button("Send All Emails"):
#                     # Use Communication Agent to send emails
#                     try:
#                         for email, content in st.session_state.emails_sent.items():
#                             if not content["sent"]:
#                                 result = communication_agent.send_email(
#                                     to_email=email,
#                                     subject=content["subject"],
#                                     html_content=content["body"],
#                                     sender_name=interviewer_name if interviewer_name else None
#                                 )
                                
#                                 if result["success"]:
#                                     # Mark as sent
#                                     st.session_state.emails_sent[email]["sent"] = True
#                                 else:
#                                     st.error(f"Error sending email to {email}: {result['message']}")
                        
#                         st.success(f"Successfully sent {len([e for e in st.session_state.emails_sent.values() if e['sent']])} emails!")
                    
#                     except Exception as e:
#                         st.error(f"Error sending emails: {str(e)}")
#             else:
#                 st.warning("Please enter your SendGrid API Key in the sidebar to send emails")
#     else:
#         st.info("No approved candidates ready for email communication. Please approve candidates in the Resume Analysis tab.")

# # Email sending history
# if st.session_state.emails_sent:
#     with tab3:
#         st.markdown("### Email History")
        
#         email_history = []
#         for email, content in st.session_state.emails_sent.items():
#             interview_slot_info = ""
#             if "interview_slot" in content:
#                 interview_slot_info = f"{content['interview_slot']['date']} at {content['interview_slot']['time']}"
            
#             email_history.append({
#                 "Candidate": content["candidate_name"],
#                 "Email Address": email,
#                 "Subject": content["subject"],
#                 "Interview Time": interview_slot_info,
#                 "Status": "Sent" if content["sent"] else "Pending"
#             })
        
#         st.dataframe(pd.DataFrame(email_history), use_container_width=True, hide_index=True)

# # Add a section for available interview slots management
# with tab3:
#     if st.checkbox("Manage Interview Slots"):
#         st.markdown("### Interview Slot Management")
        
#         # Show current slots
#         slots_df = pd.DataFrame(st.session_state.available_interview_slots)
#         st.dataframe(slots_df)
        
#         # Add new slots
#         st.markdown("#### Add New Interview Slot")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             new_date = st.date_input("Date")
#         with col2:
#             new_time = st.text_input("Time (e.g. 10:30 AM)")
#         with col3:
#             if st.button("Add Slot"):
#                 new_id = max([slot["id"] for slot in st.session_state.available_interview_slots]) + 1 if st.session_state.available_interview_slots else 1
#                 st.session_state.available_interview_slots.append({
#                     "id": new_id,
#                     "date": new_date.strftime("%Y-%m-%d"),
#                     "time": new_time,
#                     "available": True
#                 })
#                 st.success("New interview slot added")
#                 st.experimental_rerun()

# # Footer
# st.markdown("---")
# st.markdown("Agentic HR Assistant Pro | Powered by AI")





# main.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Import our agent modules
from job_description_agent import JobDescriptionAgent
from resume_parser_agent import ResumeParserAgent
from candidate_analyzer_agent import CandidateAnalyzerAgent
from communication_agent import CommunicationAgent

# Set page configuration
st.set_page_config(
    page_title="Agentic HR Assistant Pro",
    page_icon="👔",
    layout="wide"
)

# Initialize session state variables
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "resumes" not in st.session_state:
    st.session_state.resumes = {}
if "candidates_data" not in st.session_state:
    st.session_state.candidates_data = pd.DataFrame(
        columns=["Name", "Email", "Skills Match (%)", 
                 "Experience Match (%)", "Overall Score", 
                 "Key Skills", "Strengths", "Weaknesses", 
                 "Recommendation", "Status", "Automated Decision"])
if "emails_sent" not in st.session_state:
    st.session_state.emails_sent = {}
if "available_interview_slots" not in st.session_state:
    # Initialize with some default interview slots
    st.session_state.available_interview_slots = [
        {"id": 1, "date": "2025-04-20", "time": "10:00 AM", "available": True},
        {"id": 2, "date": "2025-04-20", "time": "2:00 PM", "available": True},
        {"id": 3, "date": "2025-04-21", "time": "11:00 AM", "available": True},
        {"id": 4, "date": "2025-04-21", "time": "3:00 PM", "available": True},
        {"id": 5, "date": "2025-04-22", "time": "9:00 AM", "available": True}
    ]

# Sidebar for API Keys and Configuration
with st.sidebar:
    st.title("API Configuration")
    
    google_api_key = st.text_input("Google Gemini API Key", type="password")
    
    # Email configuration (Using Gmail)
    st.markdown("#### Email Configuration")
    gmail_email = st.text_input("Gmail Email Address")
    gmail_password = st.text_input("Gmail App Password", type="password", 
                                 help="Use an App Password for Gmail. Generate from your Google Account > Security > App Passwords")
    
    # Automation settings
    st.markdown("---")
    st.markdown("### Automation Settings")
    auto_approve_threshold = st.slider("Auto-approve candidates with score above:", 40, 90, 50)
    auto_email_enabled = st.checkbox("Auto-generate & send interview emails", value=True)
    
    interviewer_name = st.text_input("Default Interviewer Name", placeholder="HR Manager")
    company_name = st.text_input("Company Name", "Your Company")
    
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("""
    1. Enter API keys and email credentials in the sidebar
    2. Generate or paste a job description
    3. Upload candidate resumes (PDF)
    4. The system will automatically:
       - Analyze resumes and score candidates
       - Approve candidates above threshold
       - Schedule interviews for approved candidates
       - Send interview invitations via email
    """)

# Initialize agents if API keys are provided
agents_initialized = False
if google_api_key:
    try:
        # Initialize all agents
        job_description_agent = JobDescriptionAgent(google_api_key)
        resume_parser = ResumeParserAgent()
        candidate_analyzer = CandidateAnalyzerAgent(google_api_key)
        communication_agent = CommunicationAgent(google_api_key, gmail_email, gmail_password)
        
        agents_initialized = True
    except Exception as e:
        st.sidebar.error(f"Error initializing agents: {e}")
else:
    st.sidebar.warning("Please enter your Google Gemini API Key to continue")

# Main app interface
st.title("Agentic HR Assistant Pro")
st.markdown("Streamline your recruitment process with AI-powered assistance")

# Create tabs for the workflow
tab1, tab2, tab3 = st.tabs(["Job Description", "Resume Analysis", "Communication Dashboard"])

# JOB DESCRIPTION AGENT
with tab1:
    st.header("Job Description Agent")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        job_role = st.text_input("Job Role", placeholder="e.g., Senior Python Developer")
        
    with col2:
        action_type = st.selectbox(
            "Action",
            ["Generate New", "Refine Existing"]
        )
    
    # Company information (new section)
    company_col1, company_col2 = st.columns(2)
    with company_col1:
        company_name_input = st.text_input("Company Name", placeholder="Enter your company name", value=company_name)
        if company_name_input:
            company_name = company_name_input
    with company_col2:
        company_specialization = st.text_input("Company Specialization", 
                                             placeholder="e.g., Cloud Computing Solutions, Healthcare Technology")
    
    if action_type == "Generate New":
        industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Education", "Manufacturing", "Retail", "Other"])
        experience_level = st.selectbox("Experience Level", ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior (6-10 years)", "Expert (10+ years)"])
        
        key_skills = st.text_area("Key Skills Required (comma separated)", placeholder="e.g., Python, Django, AWS, Docker")
        
        if st.button("Generate Job Description", disabled=not agents_initialized):
            if not company_name:
                st.warning("Please enter your company name to continue.")
            else:
                with st.spinner("Generating comprehensive job description..."):
                    try:
                        st.session_state.job_description = job_description_agent.generate_job_description(
                            job_role, industry, experience_level, key_skills,
                            company_name, company_specialization
                        )
                    except Exception as e:
                        st.error(f"Error generating job description: {str(e)}")
    
    else:  # Refine Existing
        existing_jd = st.text_area("Paste your existing job description", height=200)
        refinement_instructions = st.text_area("Refinement instructions", 
                                              placeholder="e.g., Make it more concise, add more detail about technical requirements, etc.")
        
        if st.button("Refine Job Description", disabled=not agents_initialized):
            if existing_jd:
                with st.spinner("Refining job description..."):
                    try:
                        st.session_state.job_description = job_description_agent.refine_job_description(
                            existing_jd, refinement_instructions,
                            company_name, company_specialization
                        )
                    except Exception as e:
                        st.error(f"Error refining job description: {str(e)}")
            else:
                st.warning("Please paste an existing job description to refine.")
    
    # Display the current job description with edit capability
    if st.session_state.job_description:
        st.markdown("### Current Job Description")
        
        # Make the job description editable
        edited_jd = st.text_area("Edit Job Description if needed:", 
                               value=st.session_state.job_description,
                               height=400,
                               key="editable_job_description")
        
        # Update the job description in session state if edited
        if edited_jd != st.session_state.job_description:
            st.session_state.job_description = edited_jd

        # Add validation option
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Validate JD", disabled=not agents_initialized):
                with st.spinner("Validating job description..."):
                    validation_results = job_description_agent.validate_job_description(
                        st.session_state.job_description
                    )
                    st.info("Validation Results:")
                    st.markdown(validation_results)
        
        if st.button("Confirm and Continue"):
            st.success("Job description confirmed! Please proceed to the Resume Analysis tab.")

# RESUME PARSER AND ANALYZER
with tab2:
    st.header("Resume Processing")
    
    # Add automated decision mode indicator
    st.markdown(f"**Auto-Approval Mode**: Candidates with score >{auto_approve_threshold}% will be automatically approved and invited to interview")
    
    # Check if email is properly configured for automated sending
    if auto_email_enabled and (not gmail_email or not gmail_password):
        st.warning("⚠️ Auto-email is enabled but Gmail credentials are missing. Please configure them in the sidebar.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader("Upload candidate resumes (PDF)", 
                                         accept_multiple_files=True, 
                                         type=["pdf"])
    
    with col2:
        if st.button("Process Resumes", disabled=not agents_initialized or not st.session_state.job_description):
            if uploaded_files:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Clear previous data
                new_candidates_data = []
                
                for i, file in enumerate(uploaded_files):
                    try:
                        status_text.text(f"Processing {file.name}...")
                        
                        # Extract text from PDF using Resume Parser Agent
                        resume_text = resume_parser.extract_text_from_pdf(file)
                        
                        # Store in session state
                        st.session_state.resumes[file.name] = resume_text
                        
                        # Use Candidate Analyzer Agent to analyze the resume
                        status_text.text(f"Analyzing {file.name}...")
                        
                        analysis_data = candidate_analyzer.analyze_resume(
                            resume_text, 
                            st.session_state.job_description
                        )
                        
                        # Backup Email Extraction with Regex if missing
                        if not analysis_data.get("email") or analysis_data.get("email") == "":
                            email = resume_parser.extract_email(resume_text)
                            if email:
                                analysis_data["email"] = email
                            else:
                                analysis_data["email"] = "Not found"
                        
                        # Make automated decision based on configured threshold
                        auto_decision = "Pending"
                        decision_reason = ""
                        
                        if analysis_data.get("overall_score", 0) >= auto_approve_threshold:
                            auto_decision = "Approved"
                            decision_reason = f"Auto-approved: Score {analysis_data.get('overall_score')}% meets threshold ({auto_approve_threshold}%)"
                        else:
                            auto_decision = "Pending"
                            decision_reason = f"Manual review needed: Score {analysis_data.get('overall_score')}% below threshold ({auto_approve_threshold}%)"
                        
                        # Add to candidates data
                        new_candidates_data.append({
                            "Name": analysis_data.get("name", "Unknown"),
                            "Email": analysis_data.get("email", "Not found"),
                            "Skills Match (%)": analysis_data.get("skills_match_percentage", 0),
                            "Experience Match (%)": analysis_data.get("experience_match_percentage", 0),
                            "Overall Score": analysis_data.get("overall_score", 0),
                            "Key Skills": ", ".join(analysis_data.get("key_skills", [])),
                            "Strengths": ", ".join(analysis_data.get("strengths", [])),
                            "Weaknesses": ", ".join(analysis_data.get("weaknesses", [])),
                            "Recommendation": analysis_data.get("recommendation", ""),
                            "Status": auto_decision,
                            "Automated Decision": decision_reason,
                            "Email Sent": False
                        })
                        
                        # Update progress bar
                        progress_bar.progress((i + 1) / len(uploaded_files))
                    
                    except Exception as e:
                        st.error(f"Error processing {file.name}: {str(e)}")
                
                # Add to the existing DataFrame
                new_df = pd.DataFrame(new_candidates_data)
                st.session_state.candidates_data = pd.concat([st.session_state.candidates_data, new_df], ignore_index=True)
                
                status_text.text("Processing complete!")
                
                # Automatic email generation and sending for approved candidates
                if auto_email_enabled and gmail_email and gmail_password:
                    # Get newly approved candidates
                    auto_approved_df = new_df[new_df["Status"] == "Approved"]
                    
                    if not auto_approved_df.empty:
                        sending_status = st.empty()
                        sending_status.info(f"🤖 Automatically scheduling interviews for {len(auto_approved_df)} approved candidates...")
                        
                        email_results = []
                        
                        # Default interview settings
                        default_interview_details = {
                            "format": "Video Call",
                            "location": "Zoom (link will be sent upon confirmation)",
                            "interviewer": f"{interviewer_name}, {company_name}",
                            "additional_details": "Please prepare to discuss your experiences and have questions ready about the role."
                        }
                        
                        for idx, candidate in auto_approved_df.iterrows():
                            try:
                                # Skip if email is invalid or missing
                                if candidate["Email"] == "Not found" or "@" not in candidate["Email"]:
                                    email_results.append({
                                        "candidate": candidate["Name"],
                                        "success": False,
                                        "message": "Invalid email address"
                                    })
                                    continue
                                
                                # Get an available interview slot
                                available_slots = [slot for slot in st.session_state.available_interview_slots if slot["available"]]
                                
                                if not available_slots:
                                    email_results.append({
                                        "candidate": candidate["Name"],
                                        "success": False,
                                        "message": "No interview slots available"
                                    })
                                    continue
                                
                                # Prepare candidate info
                                candidate_info = {
                                    "name": candidate['Name'],
                                    "key_skills": candidate['Key Skills'].split(", "),
                                    "strengths": candidate['Strengths'].split(", ")
                                }
                                
                                # Get the best slot for this candidate using AI decision
                                recommended_slot = candidate_analyzer.get_best_interview_time_slot(
                                    candidate_info, 
                                    available_slots
                                )
                                
                                # Find the slot in our list
                                interview_slot = next((slot for slot in available_slots if slot["id"] == recommended_slot["slot_id"]), available_slots[0])
                                
                                # Mark the slot as unavailable
                                for i, slot in enumerate(st.session_state.available_interview_slots):
                                    if slot["id"] == interview_slot["id"]:
                                        st.session_state.available_interview_slots[i]["available"] = False
                                
                                # Use the slot info in the interview details
                                interview_details = default_interview_details.copy()
                                interview_details["date"] = f"{interview_slot['date']} at {interview_slot['time']}"
                                
                                # Generate the email
                                email_content = communication_agent.generate_interview_email(
                                    candidate_info,
                                    st.session_state.job_description,
                                    interview_details,
                                    "Professional"
                                )
                                
                                # Send the email
                                result = communication_agent.send_email(
                                    to_email=candidate["Email"],
                                    subject=email_content["subject"],
                                    html_content=email_content["body"],
                                    sender_name=default_interview_details["interviewer"]
                                )
                                
                                # Record the results
                                email_results.append({
                                    "candidate": candidate["Name"],
                                    "success": result["success"],
                                    "message": result["message"],
                                    "interview_slot": interview_slot
                                })
                                
                                # Store the email for record keeping
                                if result["success"]:
                                    st.session_state.emails_sent[candidate['Email']] = {
                                        "subject": email_content["subject"],
                                        "body": email_content["body"],
                                        "sent": True,
                                        "candidate_name": candidate['Name'],
                                        "interview_slot": interview_slot,
                                        "date_sent": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    }
                                    
                                    # Update the DataFrame to mark email as sent
                                    for i, row in st.session_state.candidates_data.iterrows():
                                        if row["Email"] == candidate["Email"]:
                                            st.session_state.candidates_data.at[i, "Email Sent"] = True
                            
                            except Exception as e:
                                email_results.append({
                                    "candidate": candidate["Name"],
                                    "success": False,
                                    "message": str(e)
                                })
                        
                        # Display results
                        success_count = sum(1 for r in email_results if r["success"])
                        fail_count = len(email_results) - success_count
                        
                        if success_count > 0:
                            sending_status.success(f"✅ Successfully scheduled interviews for {success_count} candidates")
                        
                        if fail_count > 0:
                            st.error(f"⚠️ Failed to send {fail_count} emails. See Communication Dashboard for details.")
                
                st.success(f"Successfully processed {len(uploaded_files)} resumes")
            else:
                st.warning("Please upload resume files (PDF format)")
    
    # Display candidate analysis results in an editable table
    if not st.session_state.candidates_data.empty:
        st.markdown("### Candidate Analysis Results")
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        with col1:
            min_score = st.slider("Minimum Overall Score", 0, 100, 0)
        with col2:
            recommendation_filter = st.multiselect(
                "Filter by Recommendation", 
                options=["Strong Hire", "Potential Hire", "Consider for Different Role", "Reject"],
                default=["Strong Hire", "Potential Hire"]
            )
        with col3:
            status_filter = st.multiselect(
                "Filter by Status",
                options=["Pending", "Approved", "Rejected"],
                default=["Pending", "Approved"]
            )
        
        # Apply filters
        filtered_df = st.session_state.candidates_data[
            (st.session_state.candidates_data["Overall Score"] >= min_score) &
            (st.session_state.candidates_data["Recommendation"].isin(recommendation_filter)) &
            (st.session_state.candidates_data["Status"].isin(status_filter))
        ]
        
        # Create an editable data table
        edited_df = st.data_editor(
            filtered_df,
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Select candidate status",
                    width="medium",
                    options=["Pending", "Approved", "Rejected"],
                ),
                "Overall Score": st.column_config.ProgressColumn(
                    "Overall Score",
                    help="Candidate's overall match score",
                    min_value=0,
                    max_value=100,
                    format="%d%%",
                ),
                "Email Sent": st.column_config.CheckboxColumn(
                    "Email Sent",
                    help="Whether an interview email has been sent",
                    width="small",
                    disabled=True
                )
            },
            use_container_width=True,
            hide_index=True,
        )
        
        # Update the main dataframe with edited values and trigger email for newly approved candidates
        newly_approved = []
        
        for i, row in edited_df.iterrows():
            idx = st.session_state.candidates_data.index[
                st.session_state.candidates_data["Email"] == row["Email"]
            ].tolist()
            
            if idx:
                # Check if status has changed from Pending to Approved
                original_status = st.session_state.candidates_data.loc[idx[0], "Status"]
                if original_status != "Approved" and row["Status"] == "Approved":
                    newly_approved.append(row)
                
                # Update status
                st.session_state.candidates_data.loc[idx[0], "Status"] = row["Status"]
                
                # If rejected, add the reason
                if row["Status"] == "Rejected" and original_status != "Rejected":
                    st.session_state.candidates_data.loc[idx[0], "Automated Decision"] = "Manually rejected"
        
        # Trigger email for newly approved candidates if auto-email is enabled
        if auto_email_enabled and gmail_email and gmail_password and newly_approved:
            st.info(f"Scheduling interviews for {len(newly_approved)} newly approved candidates...")
            
            # Process will be similar to the auto-email logic above
            # This is intentionally left out to avoid redundancy in the code sample
            # In a real implementation, this would call a function that handles the email generation and sending
            
            st.button("Send Interview Invitations", key="send_new_invitations")
        
        # Show the automated analysis summary
        approved_count = len(st.session_state.candidates_data[st.session_state.candidates_data["Status"] == "Approved"])
        pending_count = len(st.session_state.candidates_data[st.session_state.candidates_data["Status"] == "Pending"])
        rejected_count = len(st.session_state.candidates_data[st.session_state.candidates_data["Status"] == "Rejected"])
        
        st.markdown(f"### Analysis Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Approved Candidates", approved_count)
        col2.metric("Pending Review", pending_count)
        col3.metric("Rejected Candidates", rejected_count)

# COMMUNICATION DASHBOARD
with tab3:
    st.header("Communication Dashboard")
    
    st.markdown("### Interview Schedule")
    
    # Create a schedule view of all interviews
    if st.session_state.emails_sent:
        interview_schedule = []
        for email, content in st.session_state.emails_sent.items():
            if "interview_slot" in content:
                interview_schedule.append({
                    "Candidate": content["candidate_name"],
                    "Email": email,
                    "Date": content["interview_slot"]["date"],
                    "Time": content["interview_slot"]["time"],
                    "Sent On": content.get("date_sent", "Unknown"),
                    "Status": "Confirmed" if content["sent"] else "Pending"
                })
        
        if interview_schedule:
            st.dataframe(pd.DataFrame(interview_schedule), use_container_width=True, hide_index=True)
        else:
            st.info("No interviews scheduled yet.")
    else:
        st.info("No interviews have been scheduled yet.")
    
    # Email management
    st.markdown("### Email History")
    
    if st.session_state.emails_sent:
        email_history = []
        for email, content in st.session_state.emails_sent.items():
            interview_slot_info = ""
            if "interview_slot" in content:
                interview_slot_info = f"{content['interview_slot']['date']} at {content['interview_slot']['time']}"
            
            email_history.append({
                "Candidate": content["candidate_name"],
                "Email Address": email,
                "Subject": content["subject"],
                "Interview Time": interview_slot_info,
                "Status": "Sent" if content["sent"] else "Pending",
                "Date Sent": content.get("date_sent", "")
            })
        
        st.dataframe(pd.DataFrame(email_history), use_container_width=True, hide_index=True)
        
        # View email content
        if st.checkbox("View Email Content"):
            email_to_view = st.selectbox("Select email to view", 
                                        [f"{content['candidate_name']} ({email})" for email, content in st.session_state.emails_sent.items()])
            
            if email_to_view:
                selected_email = email_to_view.split("(")[1].split(")")[0]
                content = st.session_state.emails_sent.get(selected_email)
                
                if content:
                    st.markdown(f"**Subject:** {content['subject']}")
                    st.markdown("**Email Body:**")
                    st.text_area("", value=content['body'], height=300, disabled=True)
    else:
        st.info("No emails have been sent yet.")
    
    # Interview slot management
    st.markdown("### Interview Slot Management")
    
    # Show current slots
    slots_df = pd.DataFrame(st.session_state.available_interview_slots)
    st.dataframe(slots_df)
    
    # Add new slots
    st.markdown("#### Add New Interview Slot")
    col1, col2, col3 = st.columns(3)
    with col1:
        new_date = st.date_input("Date")
    with col2:
        new_time = st.text_input("Time (e.g. 10:30 AM)")
    with col3:
        if st.button("Add Slot"):
            new_id = max([slot["id"] for slot in st.session_state.available_interview_slots]) + 1 if st.session_state.available_interview_slots else 1
            st.session_state.available_interview_slots.append({
                "id": new_id,
                "date": new_date.strftime("%Y-%m-%d"),
                "time": new_time,
                "available": True
            })
            st.success("New interview slot added")
            st.experimental_rerun()
    
    # Add bulk slots option
    if st.checkbox("Add Multiple Slots"):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
            days = st.number_input("Number of Days", min_value=1, max_value=14, value=5)
        with col2:
            times_input = st.text_area("Times (one per line)", "9:00 AM\n11:00 AM\n2:00 PM\n4:00 PM")
            
        if st.button("Generate Multiple Slots"):
            times = [time.strip() for time in times_input.split("\n") if time.strip()]
            
            from datetime import timedelta
            
            for day in range(days):
                current_date = start_date + timedelta(days=day)
                for time in times:
                    new_id = max([slot["id"] for slot in st.session_state.available_interview_slots]) + 1 if st.session_state.available_interview_slots else 1
                    st.session_state.available_interview_slots.append({
                        "id": new_id,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "time": time,
                        "available": True
                    })
            
            st.success(f"Added {len(times) * days} new interview slots")
            st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("Agentic HR Assistant | Powered by AI")