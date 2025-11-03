# HubSpot MCP Setup Guide

This guide will help you set up the Model Context Protocol (MCP) server for HubSpot integration.

## What is MCP?

Model Context Protocol (MCP) is a standardized protocol that allows AI assistants to connect with various services and tools. This setup enables your application to interact with HubSpot's API through MCP.

## Prerequisites

- Node.js and npm installed (for running the MCP server)
- A HubSpot account with API access
- HubSpot Private App with appropriate scopes

## Setup Instructions

### 1. Get HubSpot Access Token

You have two options for authentication:

#### Option A: Private Apps (Recommended)

**Finding Private Apps:**
1. Click the ⚙️ **Settings** icon in HubSpot (top right)
2. In the left sidebar, go to **Integrations** → **Private Apps**
3. Or use direct URL: `https://app.hubspot.com/private-apps/YOUR_ACCOUNT_ID`

**Creating a Private App:**
1. Click "Create a private app"
2. Give it a name (e.g., "MCP Integration")
3. Select the scopes you need:
   - **CRM**: Read/Write for contacts, companies, deals
   - **Standard**: As needed for your use case
4. Create the app and copy the access token

**Requirements:**
- Need **Super Admin** permissions
- Available on all HubSpot tiers (Free, Starter, Professional, Enterprise)

**Can't find Private Apps?**
- Check your user role: Settings → Users & Teams
- Must be a Super Admin to see this option
- If still not visible, contact your HubSpot admin or use Option B below

#### Option B: OAuth Access Token (Alternative)

If Private Apps aren't available:

1. Go to Settings → Integrations → **Connected Apps**
2. Look for existing OAuth integrations
3. Or create a developer app at: https://developers.hubspot.com/
4. Use the OAuth flow to generate an access token

**Note:** OAuth tokens expire and require refresh token handling, so Private Apps are preferred for MCP integration.

### 2. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your HubSpot access token:
   ```
   HUBSPOT_ACCESS_TOKEN=your_actual_token_here
   ```

### 3. Install Dependencies

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configure Your MCP Client

The HubSpot MCP server configuration is located in `mcp-config/hubspot-config.json`.

To use this with Claude Desktop or other MCP-compatible clients:

1. Copy the configuration from `mcp-config/hubspot-config.json`
2. Add it to your MCP client's configuration file
3. Make sure the `HUBSPOT_ACCESS_TOKEN` environment variable is set

#### For Claude Desktop:

Add to your Claude Desktop config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### 5. Verify the Setup

Once configured, your MCP client should be able to:
- Read and write HubSpot CRM data
- Access contacts, companies, and deals
- Perform searches and queries
- Update HubSpot records

## Configuration Details

The MCP server uses the following command:
```
npx -y @hubspot/mcp-server-hubspot
```

This automatically downloads and runs the latest HubSpot MCP server.

## Troubleshooting

### Can't Find Private Apps in HubSpot?

**Check your navigation:**
1. Settings (⚙️) → Integrations → Private Apps
2. Look for "Private Apps" in the left sidebar under Integrations section
3. If you see "Connected Apps" and "Legacy Apps" but not "Private Apps", try:
   - Checking your permissions (must be Super Admin)
   - Using the direct URL: `https://app.hubspot.com/private-apps/YOUR_ACCOUNT_ID`
   - Contacting your HubSpot account admin

**Permission Check:**
- Go to Settings → Users & Teams
- Find your user account
- Verify you have "Super Admin" role
- Regular users cannot create Private Apps

**Alternative if Private Apps unavailable:**
- Use OAuth authentication (Option B above)
- Ask your HubSpot admin to create a Private App for you
- Use a developer account at https://developers.hubspot.com/

### Error: "Command not found: npx"
- Install Node.js from https://nodejs.org/

### Error: "Invalid access token"
- Verify your token in `.env` matches the one from HubSpot
- Check that your Private App has the necessary scopes
- Ensure the token hasn't expired
- For OAuth tokens, check if token needs refresh

### Error: "Permission denied"
- Review your Private App scopes in HubSpot
- Add the required scopes and regenerate the token
- Ensure you have CRM access permissions in your HubSpot account

## Available MCP Tools

Once connected, you can use various HubSpot operations through MCP:
- `hubspot_get_contact` - Retrieve contact information
- `hubspot_search_contacts` - Search for contacts
- `hubspot_create_contact` - Create new contacts
- `hubspot_update_contact` - Update existing contacts
- Similar operations for companies, deals, and other CRM objects

## Security Notes

- Never commit your `.env` file to version control
- Rotate your access tokens regularly
- Use the minimum required scopes for your Private App
- Keep your HubSpot access token secure

## Resources

- [HubSpot MCP Server Documentation](https://github.com/hubspot/mcp-server-hubspot)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [HubSpot API Documentation](https://developers.hubspot.com/docs/api/overview)
