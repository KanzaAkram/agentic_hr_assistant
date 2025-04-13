# # communication_agent.py
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# class CommunicationAgent:
#     def __init__(self, gemini_api_key, sendgrid_api_key=None):
#         os.environ["GOOGLE_API_KEY"] = gemini_api_key
#         self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=gemini_api_key)
#         self.sendgrid_api_key = sendgrid_api_key
#         self.sg_client = SendGridAPIClient(sendgrid_api_key) if sendgrid_api_key else None
    
#     def generate_interview_email(self, candidate_info, job_description, interview_details, email_tone="Professional"):
#         """Generate a personalized interview invitation email"""
#         # Truncate the job description to avoid too long prompt
#         job_desc_truncated = job_description[:500] + "..." if len(job_description) > 500 else job_description
        
#         email_prompt = f"""
#         Create a personalized interview invitation email for a job candidate with the following details:
        
#         CANDIDATE:
#         - Name: {candidate_info['name']}
#         - Key Skills: {', '.join(candidate_info['key_skills'])}
#         - Strengths: {', '.join(candidate_info['strengths'])}
        
#         JOB DETAILS:
#         {job_desc_truncated}
        
#         INTERVIEW DETAILS:
#         - Date: {interview_details['date']}
#         - Format: {interview_details['format']}
#         - Location: {interview_details['location']}
#         - Interviewer: {interview_details['interviewer']}
#         - Additional details: {interview_details.get('additional_details', '')}
        
#         Tone should be: {email_tone}
        
#         Include:
#         1. Personal greeting with candidate's name
#         2. Expression of interest based on their specific skills and strengths
#         3. Clear interview details (date, time, format, location)
#         4. Request for confirmation
#         5. Contact information for questions
#         6. Professional signature from the interviewer
        
#         IMPORTANT: Write only the email body, no subject line.
#         """
        
#         response = self.llm.invoke(email_prompt)
#         email_body = response.content
        
#         # Generate subject line
#         job_title = job_description.split('\n')[0] if '\n' in job_description else 'the open position'
        
#         subject_prompt = f"""
#         Create a concise, professional subject line for an interview invitation email for:
#         - Candidate: {candidate_info['name']}
#         - Position: {job_title}
#         - Date: {interview_details['date']}
        
#         Return only the subject line, nothing else.
#         """
        
#         subject_response = self.llm.invoke(subject_prompt)
#         email_subject = subject_response.content.strip()
        
#         return {
#             "subject": email_subject,
#             "body": email_body
#         }
    
#     def generate_rejection_email(self, candidate_info, job_description, reason=None, feedback=True):
#         """Generate a professional rejection email with optional feedback"""
#         # Truncate the job description
#         job_desc_truncated = job_description[:300] + "..." if len(job_description) > 300 else job_description
        
#         # Create condition text for feedback section
#         feedback_instruction = "3. Provide constructive feedback based on their strengths and weaknesses" if feedback else ""
        
#         # Create condition text for reason
#         reason_text = f"REJECTION REASON: {reason}" if reason else ""
        
#         email_prompt = f"""
#         Create a professional, respectful rejection email for a job candidate with the following details:
        
#         CANDIDATE:
#         - Name: {candidate_info['name']}
        
#         JOB DETAILS:
#         {job_desc_truncated}
        
#         {reason_text}
        
#         The email should:
#         1. Be kind but clear about the decision
#         2. Thank the candidate for their time and interest
#         {feedback_instruction}
#         4. Wish them well in their job search
#         5. Leave the door open for future opportunities if appropriate
        
#         IMPORTANT: Write only the email body, no subject line.
#         """
        
#         response = self.llm.invoke(email_prompt)
#         email_body = response.content
        
#         # Generate subject line
#         job_title = job_description.split('\n')[0] if '\n' in job_description else 'the open position'
        
#         subject_prompt = f"""
#         Create a respectful subject line for a job application rejection email that doesn't explicitly mention rejection in the subject.
#         Position: {job_title}
        
#         Return only the subject line, nothing else.
#         """
        
#         subject_response = self.llm.invoke(subject_prompt)
#         email_subject = subject_response.content.strip()
        
#         return {
#             "subject": email_subject,
#             "body": email_body
#         }
    
#     def send_email(self, to_email, subject, html_content, from_email=None, sender_name=None):
#         """Send an email using SendGrid API"""
#         if not self.sg_client:
#             raise Exception("SendGrid client not initialized. Please provide a valid API key.")
        
#         from_email = from_email or "your-email@example.com"  # Change to default sender
#         if sender_name:
#             from_email = f"{sender_name} <{from_email}>"
            
#         message = Mail(
#             from_email=from_email,
#             to_emails=to_email,
#             subject=subject,
#             html_content=html_content.replace('\n', '<br>'))
        
#         try:
#             response = self.sg_client.send(message)
#             return {
#                 "status_code": response.status_code,
#                 "success": response.status_code >= 200 and response.status_code < 300,
#                 "message": "Email sent successfully" if response.status_code < 300 else f"Error: Status code {response.status_code}"
#             }
#         except Exception as e:
#             return {
#                 "status_code": 500,
#                 "success": False,
#                 "message": f"Error sending email: {str(e)}"
#             }




# communication_agent.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_google_genai import ChatGoogleGenerativeAI

class CommunicationAgent:
    def __init__(self, gemini_api_key, gmail_email=None, gmail_password=None):
        os.environ["GOOGLE_API_KEY"] = gemini_api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=gemini_api_key)
        self.gmail_email = gmail_email
        self.gmail_password = gmail_password
    
    def generate_interview_email(self, candidate_info, job_description, interview_details, email_tone="Professional"):
        """Generate a personalized interview invitation email"""
        # Truncate the job description to avoid too long prompt
        job_desc_truncated = job_description[:500] + "..." if len(job_description) > 500 else job_description
        
        email_prompt = f"""
        Create a personalized interview invitation email for a job candidate with the following details:
        
        CANDIDATE:
        - Name: {candidate_info['name']}
        - Key Skills: {', '.join(candidate_info['key_skills'])}
        - Strengths: {', '.join(candidate_info['strengths'])}
        
        JOB DETAILS:
        {job_desc_truncated}
        
        INTERVIEW DETAILS:
        - Date: {interview_details['date']}
        - Format: {interview_details['format']}
        - Location: {interview_details['location']}
        - Interviewer: {interview_details['interviewer']}
        - Additional details: {interview_details.get('additional_details', '')}
        
        Tone should be: {email_tone}
        
        Include:
        1. Personal greeting with candidate's name
        2. Expression of interest based on their specific skills and strengths
        3. Clear interview details (date, time, format, location)
        4. Request for confirmation
        5. Contact information for questions
        6. Professional signature from the interviewer
        
        IMPORTANT: Write only the email body, no subject line.
        """
        
        response = self.llm.invoke(email_prompt)
        email_body = response.content
        
        # Generate subject line
        job_title = job_description.split('\n')[0] if '\n' in job_description else 'the open position'
        
        subject_prompt = f"""
        Create a concise, professional subject line for an interview invitation email for:
        - Candidate: {candidate_info['name']}
        - Position: {job_title}
        - Date: {interview_details['date']}
        
        Return only the subject line, nothing else.
        """
        
        subject_response = self.llm.invoke(subject_prompt)
        email_subject = subject_response.content.strip()
        
        return {
            "subject": email_subject,
            "body": email_body
        }
    
    def generate_rejection_email(self, candidate_info, job_description, reason=None, feedback=True):
        """Generate a professional rejection email with optional feedback"""
        # Truncate the job description
        job_desc_truncated = job_description[:300] + "..." if len(job_description) > 300 else job_description
        
        # Create condition text for feedback section
        feedback_instruction = "3. Provide constructive feedback based on their strengths and weaknesses" if feedback else ""
        
        # Create condition text for reason
        reason_text = f"REJECTION REASON: {reason}" if reason else ""
        
        email_prompt = f"""
        Create a professional, respectful rejection email for a job candidate with the following details:
        
        CANDIDATE:
        - Name: {candidate_info['name']}
        
        JOB DETAILS:
        {job_desc_truncated}
        
        {reason_text}
        
        The email should:
        1. Be kind but clear about the decision
        2. Thank the candidate for their time and interest
        {feedback_instruction}
        4. Wish them well in their job search
        5. Leave the door open for future opportunities if appropriate
        
        IMPORTANT: Write only the email body, no subject line.
        """
        
        response = self.llm.invoke(email_prompt)
        email_body = response.content
        
        # Generate subject line
        job_title = job_description.split('\n')[0] if '\n' in job_description else 'the open position'
        
        subject_prompt = f"""
        Create a respectful subject line for a job application rejection email that doesn't explicitly mention rejection in the subject.
        Position: {job_title}
        
        Return only the subject line, nothing else.
        """
        
        subject_response = self.llm.invoke(subject_prompt)
        email_subject = subject_response.content.strip()
        
        return {
            "subject": email_subject,
            "body": email_body
        }
    
    def send_email(self, to_email, subject, html_content, from_email=None, sender_name=None):
        """Send an email using Gmail SMTP"""
        if not self.gmail_email or not self.gmail_password:
            raise Exception("Gmail credentials not provided. Please provide valid email and app password.")
        
        from_email = self.gmail_email
        
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{sender_name} <{from_email}>" if sender_name else from_email
        msg['To'] = to_email
        
        # Convert newlines to <br> tags for HTML
        html_content_formatted = html_content.replace('\n', '<br>')
        
        # Attach HTML part
        part = MIMEText(html_content_formatted, 'html')
        msg.attach(part)
        
        try:
            # Connect to Gmail SMTP server
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_email, self.gmail_password)
            
            # Send email
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            
            return {
                "status_code": 200,
                "success": True,
                "message": "Email sent successfully"
            }
        except Exception as e:
            return {
                "status_code": 500,
                "success": False,
                "message": f"Error sending email: {str(e)}"
            }