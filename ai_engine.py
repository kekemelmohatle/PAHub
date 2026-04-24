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
