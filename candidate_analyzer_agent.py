import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI

class CandidateAnalyzerAgent:
    def __init__(self, api_key):
        os.environ["GOOGLE_API_KEY"] = api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)

    
    
    def analyze_resume(self, resume_text, job_description):
        """Analyze a resume against a job description"""
        analysis_prompt = f"""
        You are an expert HR analyst. Analyze the following resume against the job description.
        
        JOB DESCRIPTION:
        {job_description}
        
        RESUME:
        {resume_text}
        
        Provide your analysis in valid JSON format with these fields:
        - name: The candidate's full name
        - email: The candidate's email address (extract it accurately)
        - skills_match_percentage: A numerical score (0-100) representing how well the candidate's skills match the requirements
        - experience_match_percentage: A numerical score (0-100) representing how well the candidate's experience matches the requirements
        - overall_score: A numerical score (0-100) reflecting the candidate's overall suitability
        - key_skills: List of the candidate's top 5 most relevant skills
        - strengths: 3 key strengths relative to the position
        - weaknesses: 3 key areas for improvement relative to the position
        - recommendation: One of ["Strong Hire", "Potential Hire", "Consider for Different Role", "Reject"]
        
        Return ONLY the JSON without any other text.
        """
        
        response = self.llm.invoke(analysis_prompt)
        
        # Extract and parse the JSON
        json_str = response.content
        
        # Clean up the JSON string if needed
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        try:
            analysis_result = json.loads(json_str)
            
            # Add automatic decision based on score
            analysis_result["auto_decision"] = self._make_automatic_decision(analysis_result)
            
            return analysis_result
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing analysis response: {str(e)}")
    
    def _make_automatic_decision(self, analysis_result):
        """Make an automatic decision based on candidate analysis"""
        overall_score = analysis_result.get("overall_score", 0)
        recommendation = analysis_result.get("recommendation", "")
        
        # Automated decision criteria
        if overall_score >= 50 and recommendation in ["Strong Hire", "Potential Hire"]:
            return {
                "status": "Approved",
                "reason": f"Automatically approved with score of {overall_score}%. Candidate has sufficient qualifications for the role.",
                "needs_interview": True
            }
        elif overall_score >= 40 and overall_score < 50 and recommendation != "Reject":
            return {
                "status": "Pending",
                "reason": f"Score of {overall_score}% is close to threshold. Manual review recommended.",
                "needs_interview": False
            }
        else:
            return {
                "status": "Rejected",
                "reason": f"Score of {overall_score}% is below threshold or recommendation is '{recommendation}'.",
                "needs_interview": False
            }
    
    def rank_candidates(self, candidates_data, weights=None):
        """Rank candidates based on their analysis scores and optional custom weights"""
        if weights is None:
            # Default weights for different factors
            weights = {
                "skills_match_percentage": 0.4,
                "experience_match_percentage": 0.3,
                "overall_score": 0.3
            }
        
        for candidate in candidates_data:
            weighted_score = (
                candidate.get("skills_match_percentage", 0) * weights["skills_match_percentage"] +
                candidate.get("experience_match_percentage", 0) * weights["experience_match_percentage"] +
                candidate.get("overall_score", 0) * weights["overall_score"]
            )
            candidate["weighted_score"] = weighted_score
        
        # Sort candidates by weighted score
        ranked_candidates = sorted(candidates_data, key=lambda x: x.get("weighted_score", 0), reverse=True)
        return ranked_candidates
    
    def get_best_interview_time_slot(self, candidate_profile, available_slots):
        """Recommend the best interview time slot based on candidate profile and availability"""
        prompt = f"""
        You are an intelligent HR scheduling assistant. Based on the candidate profile below, 
        recommend the most suitable interview time slot from the available options.
        
        CANDIDATE PROFILE:
        - Name: {candidate_profile.get('name', 'Unknown')}
        - Overall Score: {candidate_profile.get('overall_score', 0)}
        - Key Skills: {', '.join(candidate_profile.get('key_skills', []))}
        - Experience: {candidate_profile.get('experience_match_percentage', 0)}%
        
        AVAILABLE TIME SLOTS:
        {json.dumps(available_slots, indent=2)}
        
        Consider factors like:
        1. Priority for higher-scoring candidates
        2. Matching with the right interviewer expertise
        3. Optimal time of day based on candidate profile
        
        Return your recommendation as a JSON with:
        - slot_id: The ID of the recommended slot
        - reasoning: Brief explanation of why this slot is recommended
        """
        
        response = self.llm.invoke(prompt)
        
        try:
            # Extract JSON from response
            json_str = response.content
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            
            return json.loads(json_str)
        except Exception as e:
            # Fall back to first available slot if there's an error
            if available_slots and len(available_slots) > 0:
                return {
                    "slot_id": available_slots[0].get("id"),
                    "reasoning": "Fallback to first available slot due to processing error."
                }
            else:
                return {
                    "slot_id": None,
                    "reasoning": "No available slots found."
                }