import os
import json
from datetime import datetime, timedelta
import csv

#
============================================================
# PART 1: DATA PERSISTENCE LAYER (CRM)
# This module manages the "Source of Truth"for user  data.
#
============================================================

class CRMSystem:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.data = self._load_db()

    def _load_db(self):
        # Initializes or loads the lightweight JSON database.
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
                    # Saves current memory state to physical storage.
                    for key, value in default_data.items():
                        if key in loaded_data:
                            if isinstance(value, dict) and isinstance(loaded_data[key], dict):
                                # Recursively merge for nested dictionaries (like analytics)
                                value.update(loaded_data[key])
                            else:
                                # For lists or other types, just take the loaded value
                                default_data[key] = loaded_data[key]
                except json.JSONDecodeError:
                    # Handle case where database.json is empty or corrupted
                    print(f"Warning: Could not decode {self.filename}. Initializing with default data.")
        return default_data

    def _sync(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    # --- Contacts ---
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

        # Auto welcome campaign
        # Note: ai_marketing_engine requires a contact dict, even if empty for default greeting
        welcome_email = ai_marketing_engine("Welcome to our Marketing Hub", contact)
        self.save_campaign("Welcome Campaign", welcome_email)

        return f"Added {name} to CRM and created a welcome campaign."

    # --- Companies ---
    def save_company(self, name, industry):
        company = {
            "id": len(self.data["companies"]) + 1,
            "name": name,
            "industry": industry,
            "date_added": str(datetime.now().date())
        }
        self.data["companies"].append(company)
        self._sync()
        return f"Company {name} added."

    # --- Deals ---
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

    # --- Campaigns ---
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

        # Analytics
        self.data["analytics"]["total_campaigns"] += 1
        if scheduled_date:
            self.data["analytics"]["scheduled_campaigns"] += 1
        else:
            self.data["analytics"]["immediate_campaigns"] += 1

        self._sync()

    # --- Analytics ---
    def record_email_sent(self):
        self.data["analytics"]["emails_sent"] += 1
        self._sync()

    def record_open(self):
        self.data["analytics"]["opens"] += 1
        self._sync()

    def record_click(self):
        self.data["analytics"]["clicks"] += 1
        self._sync()

    # --- Export ---
    def export_contacts_csv(self, filename="contacts.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "company", "date_added"])
            writer.writeheader()
            writer.writerows(self.data["contacts"])
        return f"Contacts exported to {filename}"

    def export_campaigns_csv(self, filename="campaigns.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "topic", "status", "scheduled_date", "date_created", "email_body"])
            writer.writeheader()
            writer.writerows(self.data["campaigns"])
        return f"Campaigns exported to {filename}"

#
=============================================================== 
# PART 2: AI LOGIC LAYER
# Processes any -defined marketing topic.
#
=================================================================
def ai_marketing_engine(user_topic, contact=None):
    disclaimer = "\n\n[NOTICE: this content is AI suggested. Review for accuracy.]"
    subject_line = f"Unlock Growth: {user_topic}"
    greeting = f"Dear {contact['name']}" if contact and 'name' in contact else "Dear Valued Partner,"

    body = (
        f"Subject: {subject_line}\n\n"
        f"{greeting}\n\n"
        f"In today’s competitive market, {user_topic} is becoming a critical driver of success. "
        f"Businesses that adopt AI marketing tools are seeing measurable improvements in sales, "
        f"customer engagement, and campaign efficiency.\n\n"
        f"Here’s how our solutions can help you:\n"
        f"- Automate repetitive marketing tasks to save time\n"
        f"- Use AI-driven insights to target the right audience\n"
        f"- Personalize campaigns to boost customer loyalty\n"
        f"- Track performance with real-time analytics\n\n"
        f"By leveraging these tools, you can focus on growing your business while our platform handles "
        f"the complexity of modern marketing.\n\n"
        f"👉 Ready to see how {user_topic} can transform your sales strategy? "
        f"Schedule a free consultation today.\n\n"
        f"Best regards,\n"
        f"AI Marketing Partner"
    )
    return body + disclaimer

#
====================================================================== 
# PART 3: USER INTERFACE
#Handles interaction and navigation. 
#
=======================================================================
def main():
    hub = CRMSystem()
    print("--- AI MARKETING HUB ---")

    while True:
        print("\n1. Add Contact\n2. Add Company\n3. Add Deal\n4. Generate Marketing Email\n5. Schedule Campaign\n6. View Database\n7. View Analytics\n8. Export Data\n9. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            name = input("Contact Name: ")
            email = input("Contact Email: ")
            company = input("Company (optional): ")
            print(hub.save_contact(name, email, company))

        elif choice == "2":
            name = input("Company Name: ")
            industry = input("Industry: ")
            print(hub.save_company(name, industry))

        elif choice == "3":
            while True:
                try:
                    contact_id_input = input("Contact ID for deal: ")
                    contact_id = int(contact_id_input)
                    break
                except ValueError:
                    print("Invalid input. Please enter a numerical Contact ID (e.g., 1, 2).")
            stage = input("Deal Stage (Prospect/Qualified/Closed): ")
            value = input("Deal Value: ")
            print(hub.save_deal(contact_id, stage, value))

        elif choice == "4":
            topic = input("Enter campaign topic: ")
            # Ensure a contact is available for personalized emails or provide a default
            contact = hub.data["contacts"][-1] if hub.data["contacts"] else {}
            email_body = ai_marketing_engine(topic, contact)
            hub.save_campaign(topic, email_body)
            hub.record_email_sent()
            print("\n" + email_body)

        elif choice == "5":
            topic = input("Enter campaign topic: ")
            while True: # Loop until valid input is received
                try:
                    days_input = input("Schedule campaign after how many days? ")
                    days = int(days_input)
                    if days < 0:
                        print("Please enter a non-negative number of days.")
                        continue
                    break # Exit loop if conversion is successful and days is valid
                except ValueError:
                    print("Invalid input. Please enter a whole number for the number of days (e.g., 7).")
            scheduled_date = datetime.now() + timedelta(days=days)
            # Ensure a contact is available for personalized emails or provide a default
            contact = hub.data["contacts"][-1] if hub.data["contacts"] else {}
            email_body = ai_marketing_engine(topic, contact)
            hub.save_campaign(topic, email_body, scheduled_date)
            print(f"Campaign '{topic}' scheduled for {scheduled_date.date()}.")

        elif choice == "6":
            print("\n--- Contacts ---")
            for c in hub.data["contacts"]:
                print(c)
            print("\n--- Companies ---")
            for comp in hub.data["companies"]:
                print(comp)
            print("\n--- Deals ---")
            for d in hub.data["deals"]:
                print(d)
            print("\n--- Campaigns ---")
            for camp in hub.data["campaigns"]:
                print(camp)

        elif choice == "7":
            print("\n--- Analytics Dashboard ---")
            analytics = hub.data["analytics"]
            for k, v in analytics.items():
                print(f"{k}: {v}")

        elif choice == "8":
            print(hub.export_contacts_csv())
            print(hub.export_campaigns_csv())

        elif choice == "9":
            print("Shutting down...")
            break

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
