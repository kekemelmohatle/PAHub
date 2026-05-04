---
title: PAHub
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.13.0
app_file: app.py
pinned: false
---

# PAHub 👀
AI-Powered CRM & Marketing Hub

## Project Overview
PAHub is a modular Python-based application designed to provide **free and accessible marketing tools for small businesses**.  
It combines a **Customer Relationship Management (CRM) system** with a **dynamic AI Marketing Engine** that helps users generate marketing content and manage business relationships efficiently.

## Key Features
### CRM System
- Add and manage contacts, companies, and deals
- Automatic timestamp tracking for records
- Simple and lightweight data handling

### AI Marketing Engine 
- Generates personalized marketing emails
- accepts user-defined topics for content creation
- Flexible prompt-based AI system

### Responsible AI Design
- Built-in ethical disclaimers for AI-generated content
- Ensures transparency in generated outputs

### Data Export
- Export CRM data to CSV format for reporting and analysis

## System Architecture
### **Logic Layer**
Built using Python with a modular structure to seperate functionality (CRM, AI engine, data handling).
### **Data Layer**
Uses lightweight **JSON file storage** instead of a database for beter performance on low-resource systems.
##3 **AI Engine**:
A dynamic prompt-based system that generates marketing content based on user input.

## Tech Stack
- Python
- Gradio (UI Framework)
- JSON (data storage)
- Hugging Face Spaces (Deployment Platform)

## why PAHub?
PAHub is built with the vision of:
- Making business tools **accessible to everyone**
- Removing the need for expensive SaaS subscriptions
- Bringing **AI-powerd marketing to small businesses**
- Running efficiently even on low-end systems

## Live Demo 
https://kekemel-pahub.hf.space

## Installation (local Setup)
'''bash
git clone https://github.com/kekemelmohatle/PAHub.git
cd PAHub
pip install -r requirements.txt
python app.py

## Founder & Developer 
Kekeletso Mohatle (South Africa) 
