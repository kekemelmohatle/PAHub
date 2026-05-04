import gradio as gr
from crm_system import CRMSystem
from ai_engine import ai_marketing_engine
from datetime import datetime, timedelta

hub = CRMSystem()

# ✅ Custom CSS for logo background + gradient overlays
custom_css = """
body {
    background: url('assets/logo.png') no-repeat center center fixed;
    background-size: cover;
}

/* Default container overlay (transparent so other sections show logo directly) */
.gradio-container {
    background-color: rgba(0,0,0,0.0);
    color: #ffffff;
}

/* Gradient overlay only for Dashboard + Analytics sections */
.dashboard-overlay, .analytics-overlay {
    background: linear-gradient(
        rgba(0, 0, 128, 0.7),   /* deep blue with 70% transparency */
        rgba(0, 128, 0, 0.7)    /* green with 70% transparency */
    );
    border-radius: 8px;
    padding: 15px;
    color: #ffffff;
}
"""

def add_contact(name, email, company=""):
    return hub.save_contact(name, email, company)

def add_company(name, industry):
    return hub.save_company(name, industry)

def add_deal(contact_id, stage, value):
    try:
        contact_id = int(contact_id)
    except ValueError:
        return "Contact ID must be a number."
    return hub.save_deal(contact_id, stage, value)

def generate_email_with_industry(topic, industry):
    contact = {"industry": industry} if industry else {}
    email_body = ai_marketing_engine(topic, contact)
    hub.save_campaign(topic, email_body)
    hub.record_email_sent()
    return email_body

def schedule_campaign_with_industry(topic, days, industry):
    try:
        days = int(days)
    except ValueError:
        return "Days must be a number."
    scheduled_date = datetime.now() + timedelta(days=days)
    contact = {"industry": industry} if industry else {}
    email_body = ai_marketing_engine(topic, contact)
    hub.save_campaign(topic, email_body, scheduled_date)
    return f"Campaign '{topic}' scheduled for {scheduled_date.date()}."

def process_scheduled():
    return hub.process_scheduled_campaigns()

def view_analytics():
    return hub.analytics_summary()

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🏢 PAHub – AI CRM & Marketing Hub")
    gr.Markdown("Welcome to PAHub. Use the sidebar to navigate between sections.")

    with gr.Row():
        with gr.Column(scale=1):
            nav = gr.Radio(
                choices=[
                    "📊 Dashboard",
                    "👤 Contacts",
                    "🏢 Companies",
                    "💼 Deals",
                    "📣 Campaigns",
                    "📈 Analytics"
                ],
                label="Navigation",
                value="📊 Dashboard",
                interactive=True
            )

        with gr.Column(scale=4):
            content = gr.Group()

            with gr.Column(visible=True, elem_classes=["dashboard-overlay"]) as dashboard_section:
                gr.Markdown("### 📊 Dashboard Overview")
                gr.Markdown("""
                PAHub is a tool made for **small businesses**.  
                It helps you keep track of people you know (contacts), the companies you work with, and the deals you make.  
                You can also send messages to customers, plan them for later, and see how your business is doing.  
                **Who it's for:**  
                - Small business owners  
                - Teams who want an easy way to stay organized  
                - Anyone who needs a simple system to manage customers and business growth  
                """)

                gr.HTML("""
                <div style="margin-top:20px; font-size:14px; color:#111827;">
                    <strong>Disclaimer:</strong>
                    <em>[NOTICE: This content is AI suggested. Review for accuracy before use.]</em>
                </div>
                """)

            with gr.Column(visible=False) as contacts_section:
                name = gr.Textbox(label="Name", info=hub.field_info["name"])
                email = gr.Textbox(label="Email", info=hub.field_info["email"])
                company = gr.Textbox(label="Company (optional)", info=hub.field_info["company"])
                out_contact = gr.Textbox(label="Result")
                btn_contact = gr.Button("Add Contact")
                btn_contact.click(add_contact, [name, email, company], out_contact)

            with gr.Column(visible=False) as companies_section:
                cname = gr.Textbox(label="Company Name", info=hub.field_info["cname"])
                industry = gr.Textbox(label="Industry", info=hub.field_info["industry"])
                out_company = gr.Textbox(label="Result")
                btn_company = gr.Button("Add Company")
                btn_company.click(add_company, [cname, industry], out_company)

            with gr.Column(visible=False) as deals_section:
                cid = gr.Textbox(label="Contact ID", info=hub.field_info["cid"])
                stage = gr.Textbox(label="Stage", info=hub.field_info["stage"])
                value = gr.Textbox(label="Value", info=hub.field_info["value"])
                out_deal = gr.Textbox(label="Result")
                btn_deal = gr.Button("Add Deal")
                btn_deal.click(add_deal, [cid, stage, value], out_deal)

            with gr.Column(visible=False) as campaigns_section:
                topic = gr.Textbox(label="Campaign Topic", info=hub.field_info["topic"])
                industry_input = gr.Textbox(label="Industry (optional)", info=hub.field_info["industry"])
                out_email = gr.Textbox(label="Generated Email", lines=12)
                btn_email = gr.Button("Generate Immediate Campaign")
                btn_email.click(generate_email_with_industry, [topic, industry_input], out_email)

                topic_sched = gr.Textbox(label="Campaign Topic")
                days = gr.Textbox(label="Schedule after (days)", info=hub.field_info["days"])
                industry_sched = gr.Textbox(label="Industry (optional)")
                out_sched = gr.Textbox(label="Result")
                btn_sched = gr.Button("Schedule Campaign")
                btn_sched.click(schedule_campaign_with_industry, [topic_sched, days, industry_sched], out_sched)

                btn_process = gr.Button("Process Scheduled Campaigns")
                btn_process.click(process_scheduled, None, None)

        
            with gr.Column(visible=False, elem_classes=["analytics-overlay"]) as analytics_section:
                out_analytics = gr.JSON(label="Analytics Dashboard")
                btn_analytics = gr.Button("View Analytics")
                btn_analytics.click(view_analytics, None, out_analytics)

    def show_section(choice):
        return {
            dashboard_section: gr.update(visible=choice == "📊 Dashboard"),
            contacts_section: gr.update(visible=choice == "👤 Contacts"),
            companies_section: gr.update(visible=choice == "🏢 Companies"),
            deals_section: gr.update(visible=choice == "💼 Deals"),
            campaigns_section: gr.update(visible=choice == "📣 Campaigns"),
            analytics_section: gr.update(visible=choice == "📈 Analytics"),
        }

    nav.change(show_section, nav, [dashboard_section, contacts_section, companies_section, deals_section, campaigns_section, analytics_section])

demo.launch(theme=gr.themes.Base(primary_hue="blue", secondary_hue="green"))
