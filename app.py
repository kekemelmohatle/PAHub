import gradio as gr
from crm_system import CRMSystem
from ai_engine import ai_marketing_engine
from datetime import datetime, timedelta

hub = CRMSystem()

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

def generate_email(topic):
    contact = hub.data["contacts"][-1] if hub.data["contacts"] else {}
    email_body = ai_marketing_engine(topic, contact)
    hub.save_campaign(topic, email_body)
    hub.record_email_sent()
    return email_body

def schedule_campaign(topic, days):
    try:
        days = int(days)
    except ValueError:
        return "Days must be a number."
    scheduled_date = datetime.now() + timedelta(days=days)
    contact = hub.data["contacts"][-1] if hub.data["contacts"] else {}
    email_body = ai_marketing_engine(topic, contact)
    hub.save_campaign(topic, email_body, scheduled_date)
    return f"Campaign '{topic}' scheduled for {scheduled_date.date()}."

def process_scheduled():
    return hub.process_scheduled_campaigns()

def view_analytics():
    return hub.data["analytics"]

with gr.Blocks() as demo:
    gr.Markdown("# 🏢 PAHub – AI CRM & Marketing Hub")

    with gr.Tab("Contacts"):
        name = gr.Textbox(label="Name")
        email = gr.Textbox(label="Email")
        company = gr.Textbox(label="Company (optional)")
        out_contact = gr.Textbox(label="Result")
        btn_contact = gr.Button("Add Contact")
        btn_contact.click(add_contact, [name, email, company], out_contact)

    with gr.Tab("Companies"):
        cname = gr.Textbox(label="Company Name")
        industry = gr.Textbox(label="Industry")
        out_company = gr.Textbox(label="Result")
        btn_company = gr.Button("Add Company")
        btn_company.click(add_company, [cname, industry], out_company)

    with gr.Tab("Deals"):
        cid = gr.Textbox(label="Contact ID")
        stage = gr.Textbox(label="Stage")
        value = gr.Textbox(label="Value")
        out_deal = gr.Textbox(label="Result")
        btn_deal = gr.Button("Add Deal")
        btn_deal.click(add_deal, [cid, stage, value], out_deal)

    with gr.Tab("Campaigns"):
        topic = gr.Textbox(label="Campaign Topic")
        out_email = gr.Textbox(label="Generated Email", lines=10)
        btn_email = gr.Button("Generate Immediate Campaign")
        btn_email.click(generate_email, [topic], out_email)

        topic_sched = gr.Textbox(label="Campaign Topic")
        days = gr.Textbox(label="Schedule after (days)")
        out_sched = gr.Textbox(label="Result")
        btn_sched = gr.Button("Schedule Campaign")
        btn_sched.click(schedule_campaign, [topic_sched, days], out_sched)

        btn_process = gr.Button("Process Scheduled Campaigns")
        btn_process.click(process_scheduled, None, None)

    with gr.Tab("Analytics"):
        out_analytics = gr.JSON(label="Analytics Dashboard")
        btn_analytics = gr.Button("View Analytics")
        btn_analytics.click(view_analytics, None, out_analytics)

    # Always-visible disclaimer at the bottom
    gr.Markdown(
        "### Disclaimer\n"
        "[NOTICE: This content is AI suggested. Review for accuracy before use.]"
    )

demo.launch()
