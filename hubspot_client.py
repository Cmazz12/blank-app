import os
from typing import List, Dict, Optional
from hubspot import HubSpot
from hubspot.crm.contacts import ApiException as ContactsApiException
from hubspot.crm.companies import ApiException as CompaniesApiException
from hubspot.crm.deals import ApiException as DealsApiException


class HubSpotClient:
    """HubSpot API client for prospecting operations."""

    def __init__(self, api_key: str):
        """Initialize HubSpot client with API key.

        Args:
            api_key: HubSpot API key or access token
        """
        self.client = HubSpot(access_token=api_key)

    def search_contacts(self, query: str = None, limit: int = 10, filters: Dict = None) -> List[Dict]:
        """Search for contacts in HubSpot.

        Args:
            query: Search query string
            limit: Maximum number of results to return
            filters: Additional filters for the search

        Returns:
            List of contact dictionaries
        """
        try:
            if query:
                # Search by query string
                search_request = {
                    "filterGroups": [
                        {
                            "filters": [
                                {
                                    "propertyName": "email",
                                    "operator": "CONTAINS_TOKEN",
                                    "value": query
                                }
                            ]
                        },
                        {
                            "filters": [
                                {
                                    "propertyName": "firstname",
                                    "operator": "CONTAINS_TOKEN",
                                    "value": query
                                }
                            ]
                        },
                        {
                            "filters": [
                                {
                                    "propertyName": "lastname",
                                    "operator": "CONTAINS_TOKEN",
                                    "value": query
                                }
                            ]
                        },
                        {
                            "filters": [
                                {
                                    "propertyName": "company",
                                    "operator": "CONTAINS_TOKEN",
                                    "value": query
                                }
                            ]
                        }
                    ],
                    "properties": [
                        "firstname", "lastname", "email", "phone", "company",
                        "jobtitle", "website", "lifecyclestage", "hs_lead_status"
                    ],
                    "limit": limit
                }
            elif filters:
                # Use custom filters
                search_request = {
                    "filterGroups": [filters],
                    "properties": [
                        "firstname", "lastname", "email", "phone", "company",
                        "jobtitle", "website", "lifecyclestage", "hs_lead_status"
                    ],
                    "limit": limit
                }
            else:
                # Get recent contacts
                search_request = {
                    "properties": [
                        "firstname", "lastname", "email", "phone", "company",
                        "jobtitle", "website", "lifecyclestage", "hs_lead_status",
                        "createdate"
                    ],
                    "limit": limit,
                    "sorts": [{"propertyName": "createdate", "direction": "DESCENDING"}]
                }

            response = self.client.crm.contacts.search_api.do_search(
                public_object_search_request=search_request
            )

            contacts = []
            for result in response.results:
                contact = {
                    "id": result.id,
                    "properties": result.properties
                }
                contacts.append(contact)

            return contacts

        except ContactsApiException as e:
            print(f"Error searching contacts: {e}")
            return []

    def get_contact(self, contact_id: str) -> Optional[Dict]:
        """Get a specific contact by ID.

        Args:
            contact_id: HubSpot contact ID

        Returns:
            Contact dictionary or None
        """
        try:
            contact = self.client.crm.contacts.basic_api.get_by_id(
                contact_id=contact_id,
                properties=[
                    "firstname", "lastname", "email", "phone", "company",
                    "jobtitle", "website", "lifecyclestage", "hs_lead_status",
                    "address", "city", "state", "zip", "country",
                    "numemployees", "annualrevenue", "industry"
                ]
            )
            return {
                "id": contact.id,
                "properties": contact.properties
            }
        except ContactsApiException as e:
            print(f"Error getting contact: {e}")
            return None

    def search_companies(self, query: str = None, limit: int = 10) -> List[Dict]:
        """Search for companies in HubSpot.

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            List of company dictionaries
        """
        try:
            if query:
                search_request = {
                    "filterGroups": [
                        {
                            "filters": [
                                {
                                    "propertyName": "name",
                                    "operator": "CONTAINS_TOKEN",
                                    "value": query
                                }
                            ]
                        },
                        {
                            "filters": [
                                {
                                    "propertyName": "domain",
                                    "operator": "CONTAINS_TOKEN",
                                    "value": query
                                }
                            ]
                        }
                    ],
                    "properties": [
                        "name", "domain", "industry", "city", "state",
                        "country", "phone", "numberofemployees", "annualrevenue"
                    ],
                    "limit": limit
                }
            else:
                search_request = {
                    "properties": [
                        "name", "domain", "industry", "city", "state",
                        "country", "phone", "numberofemployees", "annualrevenue"
                    ],
                    "limit": limit,
                    "sorts": [{"propertyName": "createdate", "direction": "DESCENDING"}]
                }

            response = self.client.crm.companies.search_api.do_search(
                public_object_search_request=search_request
            )

            companies = []
            for result in response.results:
                company = {
                    "id": result.id,
                    "properties": result.properties
                }
                companies.append(company)

            return companies

        except CompaniesApiException as e:
            print(f"Error searching companies: {e}")
            return []

    def get_company(self, company_id: str) -> Optional[Dict]:
        """Get a specific company by ID.

        Args:
            company_id: HubSpot company ID

        Returns:
            Company dictionary or None
        """
        try:
            company = self.client.crm.companies.basic_api.get_by_id(
                company_id=company_id,
                properties=[
                    "name", "domain", "industry", "city", "state", "country",
                    "phone", "numberofemployees", "annualrevenue", "description",
                    "type", "founded_year", "linkedin_company_page"
                ]
            )
            return {
                "id": company.id,
                "properties": company.properties
            }
        except CompaniesApiException as e:
            print(f"Error getting company: {e}")
            return None

    def search_deals(self, limit: int = 10) -> List[Dict]:
        """Search for deals in HubSpot.

        Args:
            limit: Maximum number of results to return

        Returns:
            List of deal dictionaries
        """
        try:
            search_request = {
                "properties": [
                    "dealname", "amount", "dealstage", "pipeline",
                    "closedate", "createdate", "dealtype"
                ],
                "limit": limit,
                "sorts": [{"propertyName": "createdate", "direction": "DESCENDING"}]
            }

            response = self.client.crm.deals.search_api.do_search(
                public_object_search_request=search_request
            )

            deals = []
            for result in response.results:
                deal = {
                    "id": result.id,
                    "properties": result.properties
                }
                deals.append(deal)

            return deals

        except DealsApiException as e:
            print(f"Error searching deals: {e}")
            return []

    def get_contact_associations(self, contact_id: str) -> Dict:
        """Get all associations for a contact (companies, deals, etc).

        Args:
            contact_id: HubSpot contact ID

        Returns:
            Dictionary of associations
        """
        associations = {
            "companies": [],
            "deals": []
        }

        try:
            # Get associated companies
            companies = self.client.crm.contacts.associations_api.get_all(
                contact_id=contact_id,
                to_object_type="companies"
            )
            if companies.results:
                for company in companies.results:
                    company_data = self.get_company(company.id)
                    if company_data:
                        associations["companies"].append(company_data)

            # Get associated deals
            deals = self.client.crm.contacts.associations_api.get_all(
                contact_id=contact_id,
                to_object_type="deals"
            )
            if deals.results:
                for deal in deals.results:
                    associations["deals"].append({"id": deal.id})

        except Exception as e:
            print(f"Error getting associations: {e}")

        return associations
