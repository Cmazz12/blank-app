import streamlit as st
import os
from dotenv import load_dotenv
from hubspot_client import HubSpotClient
from ai_prospecting_agent import AIProspectingAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="HubSpot AI Prospecting Agent",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if 'hubspot_client' not in st.session_state:
    st.session_state.hubspot_client = None
if 'ai_agent' not in st.session_state:
    st.session_state.ai_agent = None
if 'selected_contact' not in st.session_state:
    st.session_state.selected_contact = None
if 'contacts' not in st.session_state:
    st.session_state.contacts = []


def initialize_clients(hubspot_key: str, anthropic_key: str):
    """Initialize HubSpot and AI clients."""
    try:
        st.session_state.hubspot_client = HubSpotClient(hubspot_key)
        st.session_state.ai_agent = AIProspectingAgent(anthropic_key)
        return True
    except Exception as e:
        st.error(f"Error initializing clients: {str(e)}")
        return False


def display_contact_card(contact: dict):
    """Display a contact card with key information."""
    props = contact.get("properties", {})

    col1, col2 = st.columns([3, 1])

    with col1:
        name = f"{props.get('firstname', 'N/A')} {props.get('lastname', 'N/A')}"
        st.subheader(name)
        st.write(f"**Company:** {props.get('company', 'N/A')}")
        st.write(f"**Title:** {props.get('jobtitle', 'N/A')}")
        st.write(f"**Email:** {props.get('email', 'N/A')}")
        st.write(f"**Phone:** {props.get('phone', 'N/A')}")

    with col2:
        stage = props.get('lifecyclestage', 'N/A')
        status = props.get('hs_lead_status', 'N/A')
        st.metric("Lifecycle Stage", stage)
        st.metric("Lead Status", status)


def main():
    st.title("🎯 HubSpot AI Prospecting Agent")
    st.markdown("### Your AI-powered assistant for intelligent prospecting")

    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        hubspot_key = st.text_input(
            "HubSpot API Key",
            type="password",
            value=os.getenv("HUBSPOT_API_KEY", ""),
            help="Enter your HubSpot private app access token"
        )

        anthropic_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=os.getenv("ANTHROPIC_API_KEY", ""),
            help="Enter your Anthropic API key for Claude"
        )

        if st.button("🔌 Connect", type="primary"):
            if hubspot_key and anthropic_key:
                with st.spinner("Connecting to APIs..."):
                    if initialize_clients(hubspot_key, anthropic_key):
                        st.success("Connected successfully!")
            else:
                st.error("Please provide both API keys")

        st.divider()

        # Connection status
        if st.session_state.hubspot_client and st.session_state.ai_agent:
            st.success("🟢 Connected")
        else:
            st.warning("🔴 Not connected")
            st.info("💡 **Getting Started:**\n\n1. Get your HubSpot API key from: Settings → Integrations → Private Apps\n2. Get your Anthropic API key from: console.anthropic.com")

    # Check if clients are initialized
    if not st.session_state.hubspot_client or not st.session_state.ai_agent:
        st.info("👈 Please configure your API keys in the sidebar to get started")
        return

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Search Contacts",
        "👤 Contact Analysis",
        "✉️ Email Generator",
        "🏢 Company Research",
        "📊 Batch Analysis"
    ])

    # Tab 1: Search Contacts
    with tab1:
        st.header("Search Contacts")

        col1, col2 = st.columns([3, 1])

        with col1:
            search_query = st.text_input(
                "Search by name, email, or company",
                placeholder="Enter search term..."
            )

        with col2:
            search_limit = st.number_input("Results", min_value=1, max_value=50, value=10)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Search Contacts", type="primary", use_container_width=True):
                with st.spinner("Searching HubSpot..."):
                    contacts = st.session_state.hubspot_client.search_contacts(
                        query=search_query if search_query else None,
                        limit=search_limit
                    )
                    st.session_state.contacts = contacts

        with col2:
            if st.button("📋 Get Recent Contacts", use_container_width=True):
                with st.spinner("Fetching contacts..."):
                    contacts = st.session_state.hubspot_client.search_contacts(
                        limit=search_limit
                    )
                    st.session_state.contacts = contacts

        # Display results
        if st.session_state.contacts:
            st.success(f"Found {len(st.session_state.contacts)} contacts")

            for i, contact in enumerate(st.session_state.contacts):
                with st.expander(
                    f"{contact['properties'].get('firstname', 'N/A')} "
                    f"{contact['properties'].get('lastname', 'N/A')} - "
                    f"{contact['properties'].get('company', 'N/A')}"
                ):
                    display_contact_card(contact)

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if st.button("📊 Analyze", key=f"analyze_{i}"):
                            st.session_state.selected_contact = contact
                            st.switch_page
                            st.rerun()

                    with col2:
                        if st.button("✉️ Generate Email", key=f"email_{i}"):
                            st.session_state.selected_contact = contact
                            st.rerun()

                    with col3:
                        if st.button("📋 View Full Details", key=f"details_{i}"):
                            st.json(contact['properties'])
        else:
            st.info("No contacts found. Try searching or loading recent contacts.")

    # Tab 2: Contact Analysis
    with tab2:
        st.header("AI Contact Analysis")

        if st.session_state.selected_contact:
            contact = st.session_state.selected_contact
            display_contact_card(contact)

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("🎯 Full Analysis", type="primary", use_container_width=True):
                    with st.spinner("Analyzing contact with AI..."):
                        # Get associations
                        associations = st.session_state.hubspot_client.get_contact_associations(
                            contact['id']
                        )

                        # Analyze
                        result = st.session_state.ai_agent.analyze_contact(
                            contact, associations
                        )

                        if result['success']:
                            st.markdown("### 📊 AI Analysis")
                            st.markdown(result['analysis'])
                        else:
                            st.error(f"Error: {result.get('error', 'Unknown error')}")

            with col2:
                if st.button("⭐ Lead Score", use_container_width=True):
                    with st.spinner("Scoring lead..."):
                        associations = st.session_state.hubspot_client.get_contact_associations(
                            contact['id']
                        )

                        result = st.session_state.ai_agent.score_lead(
                            contact, associations
                        )

                        if result['success']:
                            st.markdown("### ⭐ Lead Score")
                            st.markdown(result['scoring'])
                        else:
                            st.error(f"Error: {result.get('error', 'Unknown error')}")

            with col3:
                if st.button("🎬 Next Actions", use_container_width=True):
                    with st.spinner("Generating action plan..."):
                        associations = st.session_state.hubspot_client.get_contact_associations(
                            contact['id']
                        )

                        result = st.session_state.ai_agent.suggest_next_actions(
                            contact, associations
                        )

                        if result['success']:
                            st.markdown("### 🎬 Recommended Actions")
                            st.markdown(result['actions'])
                        else:
                            st.error(f"Error: {result.get('error', 'Unknown error')}")
        else:
            st.info("👈 Select a contact from the Search tab to analyze")

            # Contact selector
            if st.session_state.contacts:
                st.markdown("### Or select from recent searches:")

                contact_options = {
                    f"{c['properties'].get('firstname', 'N/A')} {c['properties'].get('lastname', 'N/A')} - "
                    f"{c['properties'].get('company', 'N/A')}": c
                    for c in st.session_state.contacts
                }

                selected = st.selectbox(
                    "Choose a contact",
                    options=list(contact_options.keys())
                )

                if st.button("Analyze Selected Contact"):
                    st.session_state.selected_contact = contact_options[selected]
                    st.rerun()

    # Tab 3: Email Generator
    with tab3:
        st.header("AI Email Generator")

        if st.session_state.selected_contact:
            contact = st.session_state.selected_contact
            props = contact.get('properties', {})

            st.info(f"Generating email for: **{props.get('firstname', 'N/A')} "
                   f"{props.get('lastname', 'N/A')}** at **{props.get('company', 'N/A')}**")

            col1, col2 = st.columns(2)

            with col1:
                email_purpose = st.selectbox(
                    "Email Purpose",
                    [
                        "introduction",
                        "follow-up",
                        "value proposition",
                        "meeting request",
                        "content share",
                        "re-engagement"
                    ]
                )

            with col2:
                st.write("")  # Spacing

            additional_context = st.text_area(
                "Additional Context (optional)",
                placeholder="Add any specific details about your product, recent interactions, or key points to mention...",
                height=100
            )

            if st.button("✨ Generate Email", type="primary"):
                with st.spinner("Crafting personalized email..."):
                    result = st.session_state.ai_agent.generate_email(
                        contact,
                        purpose=email_purpose,
                        context=additional_context
                    )

                    if result['success']:
                        st.success("Email generated successfully!")
                        st.markdown("### 📧 Generated Email")
                        st.markdown(result['email'])

                        # Copy to clipboard button
                        st.code(result['email'], language=None)
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
        else:
            st.info("👈 Select a contact from the Search tab first")

    # Tab 4: Company Research
    with tab4:
        st.header("Company Research")

        col1, col2 = st.columns([3, 1])

        with col1:
            company_search = st.text_input(
                "Search for a company",
                placeholder="Enter company name or domain..."
            )

        with col2:
            company_limit = st.number_input("Results", min_value=1, max_value=20, value=5, key="company_limit")

        if st.button("🔍 Search Companies", type="primary"):
            with st.spinner("Searching companies..."):
                companies = st.session_state.hubspot_client.search_companies(
                    query=company_search if company_search else None,
                    limit=company_limit
                )

                if companies:
                    st.success(f"Found {len(companies)} companies")

                    for i, company in enumerate(companies):
                        props = company['properties']

                        with st.expander(
                            f"{props.get('name', 'N/A')} - {props.get('industry', 'N/A')}"
                        ):
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write(f"**Domain:** {props.get('domain', 'N/A')}")
                                st.write(f"**Industry:** {props.get('industry', 'N/A')}")
                                st.write(f"**Size:** {props.get('numberofemployees', 'N/A')} employees")

                            with col2:
                                st.write(f"**Revenue:** {props.get('annualrevenue', 'N/A')}")
                                st.write(f"**Location:** {props.get('city', 'N/A')}, {props.get('state', 'N/A')}")
                                st.write(f"**Phone:** {props.get('phone', 'N/A')}")

                            if st.button("🔬 Research Company", key=f"research_{i}"):
                                with st.spinner("Analyzing company..."):
                                    result = st.session_state.ai_agent.research_company(company)

                                    if result['success']:
                                        st.markdown("### 🔬 Company Analysis")
                                        st.markdown(result['research'])
                                    else:
                                        st.error(f"Error: {result.get('error', 'Unknown error')}")
                else:
                    st.warning("No companies found")

    # Tab 5: Batch Analysis
    with tab5:
        st.header("Batch Contact Analysis")

        st.markdown("""
        Analyze multiple contacts at once to identify patterns, prioritize leads,
        and develop a strategic action plan.
        """)

        if st.session_state.contacts:
            st.info(f"📊 Currently loaded: **{len(st.session_state.contacts)}** contacts")

            # Show preview of contacts
            with st.expander("👥 Preview Loaded Contacts"):
                for contact in st.session_state.contacts[:10]:
                    props = contact['properties']
                    st.write(
                        f"• {props.get('firstname', 'N/A')} {props.get('lastname', 'N/A')} - "
                        f"{props.get('jobtitle', 'N/A')} at {props.get('company', 'N/A')}"
                    )

                if len(st.session_state.contacts) > 10:
                    st.write(f"... and {len(st.session_state.contacts) - 10} more")

            if st.button("🚀 Analyze All Contacts", type="primary"):
                with st.spinner("Analyzing contacts with AI..."):
                    result = st.session_state.ai_agent.batch_analyze_contacts(
                        st.session_state.contacts
                    )

                    if result['success']:
                        st.success(f"Analyzed {result['contacts_analyzed']} contacts")
                        st.markdown("### 📊 Batch Analysis Results")
                        st.markdown(result['batch_analysis'])
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
        else:
            st.info("👈 Load contacts from the Search tab first to perform batch analysis")


if __name__ == "__main__":
    main()
