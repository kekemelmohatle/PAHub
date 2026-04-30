import json
from datetime import datetime
from ai_engine import ai_marketing_engine

class CRMSystem:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.data = {
            "contacts": [],
            "companies": [],
            "deals": [],
            "campaigns": [],
            "analytics": {
                "total_campaigns": 0,
                "scheduled_campaigns": 0,
                "immediate_campaigns": 0,
                "emails_sent": 0,
                "opens": 0,
                "clicks": 0
            }
        }

    def _sync(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def save_contact(self, name, email, company=None):
        contact = {
            "id": len(self.data["contacts"]) + 1,
            "name": name,
            "email": email,
            "company": company,
            "industry": None,
            "date_added": str(datetime.now().date())
        }
        if company:
            for comp in self.data["companies"]:
                if comp["name"].lower() == company.lower():
                    contact["industry"] = comp["industry"]
                    break
        self.data["contacts"].append(contact)
        self._sync()
        return f"Added {name} to CRM."

    def save_company(self, name, industry):
        company = {
            "id": len(self.data["companies"]) + 1,
            "name": name,
            "industry": industry,
            "date_added": str(datetime.now().date())
        }
        self.data["companies"].append(company)
        self._sync()
        return f"Company {name} in {industry} added."

    def save_deal(self, contact_id, stage, value):
        deal = {
            "id": len(self.data["deals"]) + 1,
            "contact_id": contact_id,
            "stage": stage,
            "value": value,
            "date_created": str(datetime.now())
        }
        self.data["deals"].append(deal)
        self._sync()
        return f"Deal for contact {contact_id} added in stage {stage} worth {value}."

    def save_campaign(self, topic, email_body, scheduled_date=None):
        campaign = {
            "id": len(self.data["campaigns"]) + 1,
            "topic": topic,
            "email_body": email_body,
            "date_created": str(datetime.now()),
            "scheduled_date": str(scheduled_date) if scheduled_date else None,
            "status": "Scheduled" if scheduled_date else "Immediate"
        }
        self.data["campaigns"].append(campaign)
        self.data["analytics"]["total_campaigns"] += 1
        if scheduled_date:
            self.data["analytics"]["scheduled_campaigns"] += 1
        else:
            self.data["analytics"]["immediate_campaigns"] += 1
        self._sync()

    def record_email_sent(self):
        self.data["analytics"]["emails_sent"] += 1
        self._sync()

    def process_scheduled_campaigns(self):
        now = datetime.now()
        for campaign in self.data["campaigns"]:
            if campaign["status"] == "Scheduled" and campaign["scheduled_date"]:
                try:
                    scheduled_time = datetime.fromisoformat(campaign["scheduled_date"])
                except ValueError:
                    continue
                if scheduled_time <= now:
                    campaign["status"] = "Sent"
                    self.data["analytics"]["emails_sent"] += 1
        self._sync()
        return "Processed scheduled campaigns."


# --- Enhancements added on top of your existing CRMSystem code ---
class CRMSystem(CRMSystem):
    """
    Extended CRMSystem with helper methods, metadata, and enriched analytics.
    """

    field_info = {
        "name": "Enter the full name of the contact (e.g., John Doe).",
        "email": "Provide a valid email address (e.g., john@example.com).",
        "company": "Optional: Add the company this contact belongs to.",
        "cname": "Enter the official company name.",
        "industry": "Specify the industry (e.g., Retail, Finance, Healthcare).",
        "cid": "Provide the numeric ID of the contact linked to this deal.",
        "stage": "Enter the deal stage (e.g., Prospect, Negotiation, Closed).",
        "value": "Enter the deal value (e.g., 5000).",
        "topic": "Enter the subject or theme of the campaign.",
        "days": "Enter the number of days from today to schedule the campaign.",
    }

    def get_contact_by_id(self, contact_id: int):
        for contact in self.data["contacts"]:
            if contact["id"] == contact_id:
                return contact
        return None

    def get_company_by_name(self, name: str):
        for company in self.data["companies"]:
            if company["name"].lower() == name.lower():
                return company
        return None

    def analytics_summary(self):
        return {
            "Total Campaigns": self.data["analytics"]["total_campaigns"],
            "Immediate Campaigns": self.data["analytics"]["immediate_campaigns"],
            "Scheduled Campaigns": self.data["analytics"]["scheduled_campaigns"],
            "Emails Sent": self.data["analytics"]["emails_sent"],
            "Total Contacts": len(self.data["contacts"]),
            "Total Companies": len(self.data["companies"]),
            "Total Deals": len(self.data["deals"]),
        }
