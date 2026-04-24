import os
import json
from datetime import datetime, timedelta
import csv
from ai_engine import ai_marketing_engine

class CRMSystem:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.data = self._load_db()

    def _load_db(self):
        default_data = {
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
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    loaded_data = json.load(f)
                    default_data.update(loaded_data)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode {self.filename}. Initializing with default data.")
        return default_data

    def _sync(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def save_contact(self, name, email, company=None):
        contact = {
            "id": len(self.data["contacts"]) + 1,
            "name": name,
            "email": email,
            "company": company,
            "date_added": str(datetime.now().date()),
        }
        self.data["contacts"].append(contact)
        self._sync()

        welcome_email = ai_marketing_engine("Welcome to our Marketing Hub", contact)
        self.save_campaign("Welcome Campaign", welcome_email)
        return f"Added {name} to CRM and created a welcome campaign."

    # ... (rest of methods: save_company, save_deal, save_campaign, record_email_sent, export functions)
