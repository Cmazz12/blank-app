# HubSpot MCP Setup Guide

This guide will help you set up the Model Context Protocol (MCP) server for HubSpot integration.

## What is MCP?

Model Context Protocol (MCP) is a standardized protocol that allows AI assistants to connect with various services and tools. This setup enables your application to interact with HubSpot's API through MCP.

## Prerequisites

- Node.js and npm installed (for running the MCP server)
- A HubSpot account with API access
- HubSpot Private App with appropriate scopes

## Setup Instructions

### 1. Create a HubSpot Private App

1. Go to your HubSpot account: https://app.hubspot.com/settings/integrations/private-apps
2. Click "Create a private app"
3. Give it a name (e.g., "MCP Integration")
4. Select the scopes you need (e.g., CRM read/write, contacts, companies, deals)
5. Create the app and copy the access token

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

### Error: "Command not found: npx"
- Install Node.js from https://nodejs.org/

### Error: "Invalid access token"
- Verify your token in `.env` matches the one from HubSpot
- Check that your Private App has the necessary scopes
- Ensure the token hasn't expired

### Error: "Permission denied"
- Review your Private App scopes in HubSpot
- Add the required scopes and regenerate the token

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
