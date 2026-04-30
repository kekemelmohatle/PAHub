def industry_descriptions():
    """
    Centralized industry-specific messaging templates.
    Extend this dictionary to add more industries easily.
    """
    return {
        "retail": {
            "intro": "In retail, {topic} is transforming customer engagement.",
            "bullets": [
                "Predict demand to avoid stockouts",
                "Personalize offers based on shopping behavior",
                "Automate loyalty campaigns"
            ]
        },
        "finance": {
            "intro": "In finance, {topic} enables smarter client engagement.",
            "bullets": [
                "Automate client onboarding",
                "Deliver personalized financial insights",
                "Enhance fraud detection with analytics"
            ]
        },
        "healthcare": {
            "intro": "In healthcare, {topic} improves patient communication and efficiency.",
            "bullets": [
                "Automate patient outreach",
                "Personalize wellness campaigns",
                "Track engagement for better outcomes"
            ]
        },
        "technology": {
            "intro": "In technology, {topic} accelerates innovation and customer adoption.",
            "bullets": [
                "Automate customer onboarding",
                "Enhance product recommendations",
                "Streamline support with AI chatbots"
            ]
        },
        "education": {
            "intro": "In education, {topic} enhances learning and student engagement.",
            "bullets": [
                "Personalize learning experiences",
                "Automate administrative tasks",
                "Track student progress with analytics"
            ]
        },
        "manufacturing": {
            "intro": "In manufacturing, {topic} improves efficiency and quality control.",
            "bullets": [
                "Predict equipment maintenance needs",
                "Optimize supply chain operations",
                "Enhance production quality with AI"
            ]
        },
        "hospitality": {
            "intro": "In hospitality, {topic} elevates guest experiences.",
            "bullets": [
                "Personalize guest offers",
                "Automate booking and check-in",
                "Enhance service with real-time feedback"
            ]
        },
        "real estate": {
            "intro": "In real estate, {topic} transforms client engagement.",
            "bullets": [
                "Automate property recommendations",
                "Enhance client communication",
                "Streamline transaction processes"
            ]
        },
        "nonprofit": {
            "intro": "In nonprofit organizations, {topic} boosts outreach and donor engagement.",
            "bullets": [
                "Automate donor communication",
                "Personalize fundraising campaigns",
                "Track impact with analytics"
            ]
        },
        "default": {
            "intro": "In today’s competitive market, {topic} is driving success.",
            "bullets": [
                "Automate repetitive marketing tasks",
                "Use AI-driven insights to target the right audience",
                "Personalize campaigns to boost loyalty",
                "Track performance with real-time analytics"
            ]
        }
    }


def ai_marketing_engine(user_topic, contact=None):
    """
    Generate a professional AI-suggested marketing email tailored to industry and contact info.
    """
    disclaimer = "\n\n[NOTICE: this content is AI suggested. Review for accuracy.]"
    industry = contact.get("industry", "").lower() if contact else None
    name = contact.get("name", None) if contact else None
    greeting = f"Dear {name}," if name else "Dear Valued Partner,"
    subject_line = f"Unlock Growth in {industry.title() if industry else 'Your Business'}: {user_topic}"

    templates = industry_descriptions()
    template = templates.get(industry, templates["default"])

    body = (
        f"{greeting}\n\n"
        f"{template['intro'].format(topic=user_topic)}\n\n"
        + "\n".join([f"- {point}" for point in template["bullets"]])
        + "\n"
    )

    return f"Subject: {subject_line}\n\n{body}{disclaimer}"
