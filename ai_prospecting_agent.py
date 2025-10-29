import json
from typing import Dict, List, Optional
from anthropic import Anthropic


class AIProspectingAgent:
    """AI-powered prospecting agent using Claude."""

    def __init__(self, api_key: str):
        """Initialize AI agent with Anthropic API key.

        Args:
            api_key: Anthropic API key
        """
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def analyze_contact(self, contact: Dict, associations: Dict = None) -> Dict:
        """Analyze a contact and provide prospecting insights.

        Args:
            contact: Contact data from HubSpot
            associations: Associated companies and deals

        Returns:
            Dictionary with analysis results
        """
        # Prepare contact information
        props = contact.get("properties", {})
        contact_info = f"""
Contact Information:
- Name: {props.get('firstname', 'N/A')} {props.get('lastname', 'N/A')}
- Email: {props.get('email', 'N/A')}
- Phone: {props.get('phone', 'N/A')}
- Company: {props.get('company', 'N/A')}
- Job Title: {props.get('jobtitle', 'N/A')}
- Website: {props.get('website', 'N/A')}
- Lifecycle Stage: {props.get('lifecyclestage', 'N/A')}
- Lead Status: {props.get('hs_lead_status', 'N/A')}
"""

        if associations:
            if associations.get("companies"):
                contact_info += "\nAssociated Companies:\n"
                for company in associations["companies"]:
                    company_props = company.get("properties", {})
                    contact_info += f"- {company_props.get('name', 'N/A')}: {company_props.get('industry', 'N/A')}, {company_props.get('numberofemployees', 'N/A')} employees\n"

        prompt = f"""You are an expert sales prospecting assistant. Analyze this contact and provide insights for prospecting.

{contact_info}

Please provide:
1. Lead Quality Score (1-10): Rate this lead's potential value
2. Key Insights: Important observations about this prospect
3. Potential Pain Points: What challenges might they be facing?
4. Recommended Approach: How should a salesperson engage with this prospect?
5. Next Best Actions: Specific actions to take (3-5 concrete steps)
6. Email Subject Lines: 3 compelling subject line ideas for outreach
7. Talking Points: Key topics to discuss with this prospect

Format your response as a structured analysis."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            analysis = message.content[0].text

            return {
                "success": True,
                "analysis": analysis,
                "contact_name": f"{props.get('firstname', '')} {props.get('lastname', '')}".strip()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def score_lead(self, contact: Dict, associations: Dict = None) -> Dict:
        """Score a lead based on available information.

        Args:
            contact: Contact data from HubSpot
            associations: Associated companies and deals

        Returns:
            Dictionary with lead score and reasoning
        """
        props = contact.get("properties", {})

        context = f"""
Contact: {props.get('firstname', 'N/A')} {props.get('lastname', 'N/A')}
Job Title: {props.get('jobtitle', 'N/A')}
Company: {props.get('company', 'N/A')}
Lifecycle Stage: {props.get('lifecyclestage', 'N/A')}
Lead Status: {props.get('hs_lead_status', 'N/A')}
"""

        if associations and associations.get("companies"):
            company = associations["companies"][0]
            company_props = company.get("properties", {})
            context += f"""
Company Size: {company_props.get('numberofemployees', 'N/A')} employees
Industry: {company_props.get('industry', 'N/A')}
Revenue: {company_props.get('annualrevenue', 'N/A')}
"""

        prompt = f"""You are a lead scoring expert. Score this lead from 1-100 based on the available information.

{context}

Provide:
1. Overall Score (1-100)
2. Score Breakdown:
   - Job Title/Seniority (0-25 points)
   - Company Fit (0-25 points)
   - Engagement Level (0-25 points)
   - Timing/Readiness (0-25 points)
3. Brief Reasoning: Explain the score
4. Priority Level: Hot, Warm, or Cold

Be concise but specific."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "success": True,
                "scoring": message.content[0].text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def generate_email(self, contact: Dict, purpose: str = "introduction",
                      context: str = "") -> Dict:
        """Generate a personalized outreach email.

        Args:
            contact: Contact data from HubSpot
            purpose: Purpose of email (introduction, follow-up, etc.)
            context: Additional context for email generation

        Returns:
            Dictionary with email content
        """
        props = contact.get("properties", {})

        contact_context = f"""
Recipient: {props.get('firstname', 'N/A')} {props.get('lastname', 'N/A')}
Job Title: {props.get('jobtitle', 'N/A')}
Company: {props.get('company', 'N/A')}
"""

        prompt = f"""You are an expert sales email writer. Write a personalized, compelling email for this prospect.

{contact_context}

Email Purpose: {purpose}
Additional Context: {context if context else 'None provided'}

Requirements:
- Keep it concise (150-200 words max)
- Personalize based on their role and company
- Focus on value, not features
- Include a clear call-to-action
- Professional but conversational tone
- Avoid being pushy or sales-y

Provide:
1. Subject Line (compelling and specific)
2. Email Body (properly formatted)
3. Alternative Subject Line (as backup option)"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "success": True,
                "email": message.content[0].text,
                "recipient": f"{props.get('firstname', '')} {props.get('lastname', '')}".strip()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def research_company(self, company: Dict) -> Dict:
        """Analyze a company and provide prospecting insights.

        Args:
            company: Company data from HubSpot

        Returns:
            Dictionary with company research
        """
        props = company.get("properties", {})

        company_info = f"""
Company: {props.get('name', 'N/A')}
Domain: {props.get('domain', 'N/A')}
Industry: {props.get('industry', 'N/A')}
Size: {props.get('numberofemployees', 'N/A')} employees
Revenue: {props.get('annualrevenue', 'N/A')}
Location: {props.get('city', 'N/A')}, {props.get('state', 'N/A')}, {props.get('country', 'N/A')}
"""

        prompt = f"""You are a business research analyst. Provide insights about this company for prospecting purposes.

{company_info}

Based on the available information, provide:
1. Company Profile: Brief overview
2. Potential Needs: What solutions might they need based on their industry/size?
3. Decision Makers: What roles should we target?
4. Market Position: Likely market position and maturity
5. Engagement Strategy: How to approach this company
6. Key Topics: What topics would resonate with this company?
7. Red Flags/Considerations: Any concerns or things to be aware of

Be specific and actionable."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "success": True,
                "research": message.content[0].text,
                "company_name": props.get('name', 'Unknown')
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def suggest_next_actions(self, contact: Dict, associations: Dict = None,
                           recent_activity: str = "") -> Dict:
        """Suggest next best actions for a prospect.

        Args:
            contact: Contact data from HubSpot
            associations: Associated companies and deals
            recent_activity: Description of recent interactions

        Returns:
            Dictionary with action recommendations
        """
        props = contact.get("properties", {})

        context = f"""
Contact: {props.get('firstname', 'N/A')} {props.get('lastname', 'N/A')}
Company: {props.get('company', 'N/A')}
Job Title: {props.get('jobtitle', 'N/A')}
Lifecycle Stage: {props.get('lifecyclestage', 'N/A')}
Lead Status: {props.get('hs_lead_status', 'N/A')}

Recent Activity: {recent_activity if recent_activity else 'No recent activity logged'}
"""

        prompt = f"""You are a sales strategy advisor. Based on this prospect information, recommend the next best actions.

{context}

Provide a prioritized action plan:
1. Immediate Actions (next 24-48 hours): 2-3 specific tasks
2. Short-term Actions (next week): 2-3 tasks
3. Research Tasks: What information to gather
4. Preparation: How to prepare for engagement
5. Success Metrics: How to measure progress

Be specific, actionable, and prioritized. Focus on moving the deal forward."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "success": True,
                "actions": message.content[0].text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def batch_analyze_contacts(self, contacts: List[Dict]) -> Dict:
        """Analyze multiple contacts and provide comparative insights.

        Args:
            contacts: List of contact data from HubSpot

        Returns:
            Dictionary with batch analysis results
        """
        if not contacts:
            return {"success": False, "error": "No contacts provided"}

        contacts_summary = "Contacts to analyze:\n\n"
        for i, contact in enumerate(contacts[:10], 1):  # Limit to 10 for token management
            props = contact.get("properties", {})
            contacts_summary += f"{i}. {props.get('firstname', 'N/A')} {props.get('lastname', 'N/A')} - "
            contacts_summary += f"{props.get('jobtitle', 'N/A')} at {props.get('company', 'N/A')}\n"
            contacts_summary += f"   Stage: {props.get('lifecyclestage', 'N/A')}, Status: {props.get('hs_lead_status', 'N/A')}\n\n"

        prompt = f"""You are a sales team manager. Analyze these contacts and provide strategic guidance.

{contacts_summary}

Provide:
1. Top Priority Contacts: Which 3 contacts should be prioritized and why?
2. Contact Segmentation: Group these contacts into logical segments
3. Overall Insights: Patterns or trends you notice
4. Team Action Plan: How should the team allocate resources?
5. Quick Wins: Which contacts are easiest to engage?

Be strategic and specific."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "success": True,
                "batch_analysis": message.content[0].text,
                "contacts_analyzed": len(contacts[:10])
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
