# HubSpot AI Prospecting Agent

An AI-powered prospecting assistant that integrates with your HubSpot account to help you identify, analyze, and engage with leads more effectively using Claude AI.

## Features

### Contact Intelligence
- **Smart Search**: Search and filter contacts by name, email, company, or other criteria
- **AI Analysis**: Get deep insights about prospects including lead quality scoring, pain points, and engagement strategies
- **Lead Scoring**: Automatically score leads based on multiple factors with AI-powered reasoning
- **Next Action Recommendations**: Receive specific, prioritized action plans for each prospect

### Email Generation
- **Personalized Outreach**: Generate compelling, personalized emails tailored to each prospect
- **Multiple Templates**: Choose from various email purposes (introduction, follow-up, meeting request, etc.)
- **Context-Aware**: Include custom context to make emails even more relevant

### Company Research
- **Company Profiles**: Search and analyze companies in your HubSpot database
- **Market Insights**: Get AI-powered insights about company needs, decision makers, and engagement strategies
- **Industry Analysis**: Understand company positioning and potential pain points

### Batch Analysis
- **Bulk Contact Analysis**: Analyze multiple contacts at once to identify patterns
- **Priority Ranking**: Get recommendations on which leads to prioritize
- **Strategic Planning**: Develop team-wide action plans based on your contact database

## Setup

### Prerequisites
- Python 3.11+
- HubSpot account with API access
- Anthropic API key

### Installation

1. Clone the repository and navigate to the directory:
   ```bash
   cd blank-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API keys:

   **Option A: Using environment variables**

   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```
   HUBSPOT_API_KEY=your_hubspot_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

   **Option B: Using the UI**

   You can also enter your API keys directly in the application sidebar when you run it.

### Getting API Keys

#### HubSpot API Key
1. Go to your HubSpot account
2. Navigate to Settings → Integrations → Private Apps
3. Create a new private app or use an existing one
4. Copy the access token
5. Required scopes:
   - `crm.objects.contacts.read`
   - `crm.objects.companies.read`
   - `crm.objects.deals.read`

#### Anthropic API Key
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key

## Usage

### Running the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Quick Start Guide

1. **Connect Your Accounts**
   - Enter your HubSpot and Anthropic API keys in the sidebar
   - Click "Connect"
   - Wait for the green "Connected" status

2. **Search for Contacts**
   - Go to the "Search Contacts" tab
   - Enter a search term or click "Get Recent Contacts"
   - Browse through your contacts

3. **Analyze a Contact**
   - Click "Analyze" on any contact
   - Go to the "Contact Analysis" tab
   - Choose from:
     - Full Analysis: Complete prospecting insights
     - Lead Score: Quantitative lead quality assessment
     - Next Actions: Specific action recommendations

4. **Generate an Email**
   - Select a contact
   - Go to the "Email Generator" tab
   - Choose the email purpose
   - Add optional context
   - Click "Generate Email"

5. **Research Companies**
   - Go to the "Company Research" tab
   - Search for companies
   - Click "Research Company" for AI-powered insights

6. **Batch Analysis**
   - Load contacts from the Search tab
   - Go to the "Batch Analysis" tab
   - Click "Analyze All Contacts"
   - Get strategic insights about your entire pipeline

## Architecture

### Components

- **`streamlit_app.py`**: Main Streamlit UI application
- **`hubspot_client.py`**: HubSpot API integration layer
- **`ai_prospecting_agent.py`**: AI agent using Claude for intelligent analysis
- **`requirements.txt`**: Python dependencies

### Technology Stack

- **Frontend**: Streamlit
- **HubSpot Integration**: hubspot-api-client
- **AI Engine**: Anthropic Claude (claude-3-5-sonnet-20241022)
- **Environment Management**: python-dotenv

## AI Capabilities

The AI agent uses Claude to provide:

1. **Lead Quality Assessment**: Scores leads 1-100 with detailed reasoning
2. **Insight Generation**: Identifies key opportunities and pain points
3. **Personalization**: Creates highly personalized outreach messages
4. **Strategic Planning**: Develops actionable prospecting strategies
5. **Pattern Recognition**: Identifies trends across multiple contacts
6. **Company Analysis**: Researches companies and suggests engagement approaches

## Security Best Practices

- Never commit your `.env` file to version control
- Use private apps in HubSpot with minimal required scopes
- Rotate API keys regularly
- Store API keys securely
- Review generated content before sending to prospects

## Troubleshooting

### Common Issues

**Connection Error**
- Verify your API keys are correct
- Check that your HubSpot private app has required scopes
- Ensure you have an active internet connection

**No Contacts Found**
- Verify you have contacts in your HubSpot account
- Check your search criteria
- Ensure your HubSpot API key has `crm.objects.contacts.read` scope

**AI Analysis Fails**
- Verify your Anthropic API key is valid
- Check your API usage limits
- Ensure the contact has sufficient data for analysis

**Rate Limiting**
- HubSpot has API rate limits; wait a moment and try again
- Consider implementing caching for frequently accessed data

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

See LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review HubSpot API documentation: https://developers.hubspot.com/
- Review Anthropic API documentation: https://docs.anthropic.com/

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Anthropic Claude](https://www.anthropic.com/)
- Integrates with [HubSpot CRM](https://www.hubspot.com/)
