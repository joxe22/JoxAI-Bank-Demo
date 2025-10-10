# JoxAI Banking Chatbot - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Admin Panel Guide](#admin-panel-guide)
4. [Chat Widget Guide](#chat-widget-guide)
5. [Agent Workflows](#agent-workflows)
6. [Best Practices](#best-practices)

---

## Introduction

Welcome to JoxAI Banking Chatbot - an AI-powered customer service solution designed specifically for banking institutions. This guide will help you navigate and use the system effectively.

### What is JoxAI Banking Chatbot?

JoxAI is a comprehensive customer service platform that combines:
- 🤖 **AI-Powered Chat** - Intelligent responses to customer inquiries
- 👥 **Human Agent Support** - Seamless escalation to live agents
- 📊 **Analytics Dashboard** - Real-time insights and metrics
- 🎫 **Ticket Management** - Organized support ticket workflow
- 📚 **Knowledge Base** - Centralized banking information

### User Roles

| Role | Capabilities |
|------|-------------|
| **Admin** | Full system access, user management, settings configuration |
| **Supervisor** | Team management, analytics, ticket oversight |
| **Agent** | Handle tickets, chat with customers, access knowledge base |

---

## Getting Started

### Accessing the Admin Panel

1. Navigate to your deployment URL: `https://your-app.replit.app`
2. You'll see the login page
3. Enter your credentials:
   - **Username**: Your assigned username
   - **Password**: Your password
4. Click **"Sign In"**

### First Login

After your first login, you should:
1. ✅ Update your profile information
2. ✅ Familiarize yourself with the dashboard
3. ✅ Review the knowledge base
4. ✅ Test the chat widget (if agent)

---

## Admin Panel Guide

### Dashboard Overview

The main dashboard provides at-a-glance metrics:

**📊 Key Metrics:**
- Total Conversations (today/this week)
- Active Conversations (right now)
- Open Tickets
- Tickets In Progress
- Resolved Today
- Average Response Time

**📈 Charts:**
- Conversation trends over time
- Ticket status distribution
- Agent performance metrics

### Navigation Menu

| Menu Item | Description |
|-----------|-------------|
| 🏠 **Dashboard** | Overview and key metrics |
| 💬 **Conversations** | View and manage chat conversations |
| 🎫 **Tickets** | Support ticket management |
| 📚 **Knowledge Base** | Articles and documentation |
| 👥 **Customers** | Customer profiles and information |
| 📊 **Analytics** | Detailed reports and insights |
| ⚙️ **Settings** | System configuration |

---

## Conversations Page

### Viewing Conversations

1. Click **"Conversations"** in the sidebar
2. See list of all customer conversations
3. Use filters to narrow down:
   - **All**: Show all conversations
   - **Active**: Currently ongoing chats
   - **Escalated**: Conversations sent to agents
   - **Ended**: Completed conversations

### Conversation Details

Click on any conversation to see:
- **Customer Information**: User ID, start time
- **Message History**: Full chat transcript
- **AI Responses**: What the bot replied
- **Escalation Status**: If and when escalated
- **Related Ticket**: Linked support ticket (if escalated)

### Search Conversations

Use the search bar to find conversations by:
- Customer ID
- Conversation ID
- Keywords in messages

---

## Tickets Page

### Ticket List View

The tickets page shows all support tickets with:
- **Ticket ID**: Unique identifier (e.g., TKT-A1B2C3D4)
- **Customer Name**: Who submitted the ticket
- **Subject**: Brief description
- **Status**: OPEN, IN_PROGRESS, RESOLVED, CLOSED
- **Priority**: LOW, MEDIUM, HIGH, URGENT
- **Assigned To**: Which agent is handling it

### Ticket Filters

Filter tickets by:
- **Status**: Show only open, in-progress, resolved, or closed
- **Priority**: Filter by urgency level
- **Assignment**: My tickets, unassigned, or all tickets

### Ticket Details

Click on a ticket to view:
- Full customer information
- Ticket description and history
- Related conversation (if from chat escalation)
- Message thread with customer
- Resolution notes

### Working with Tickets

**Assign to Yourself:**
1. Open ticket
2. Click **"Assign to Me"**
3. Status automatically changes to IN_PROGRESS

**Update Priority:**
1. Open ticket
2. Select new priority from dropdown
3. Changes save automatically

**Update Status:**
1. Open ticket
2. Select new status
3. Add resolution notes (for RESOLVED status)
4. Click **"Update"**

**Send Messages:**
1. Open ticket
2. Scroll to message section
3. Type your message
4. Click **"Send"**
5. Customer receives notification (if configured)

---

## Knowledge Base

### Searching Articles

1. Click **"Knowledge Base"** in sidebar
2. Use search bar to find articles
3. Filter by category:
   - Account Management
   - Transfers
   - Cards
   - Loans
   - General

### Viewing Articles

Click any article to see:
- Full content
- Category and tags
- Created/updated dates
- Author information

### Creating Articles (Admin/Supervisor)

1. Click **"Create Article"**
2. Fill in:
   - **Title**: Clear, descriptive title
   - **Content**: Detailed information
   - **Category**: Select appropriate category
   - **Tags**: Add searchable keywords
3. Click **"Save"**

### Best Practices for Articles

✅ **DO:**
- Use clear, simple language
- Include step-by-step instructions
- Add relevant tags for searchability
- Keep content up-to-date

❌ **DON'T:**
- Use technical jargon
- Make assumptions about user knowledge
- Duplicate existing content
- Forget to categorize properly

---

## Customers Page

### Customer Profiles

View detailed customer information:
- Full name and contact details
- Account number
- Customer type (Individual/Business)
- Account status
- Tags and preferences
- Interaction history

### Searching Customers

Search by:
- Name
- Email
- Phone number
- Account number

### Customer Statistics

See analytics for each customer:
- Total conversations
- Total tickets
- Last interaction date
- Customer satisfaction score

---

## Analytics Page

### Available Reports

**📊 Dashboard Metrics:**
- Real-time conversation count
- Ticket statistics
- Response time averages

**📈 Conversation Analytics:**
- Total conversations (by period)
- Active vs. ended
- Escalation rate
- Average messages per conversation

**🎫 Ticket Analytics:**
- Tickets by status
- Tickets by priority
- Resolution time
- Agent workload

**👥 Agent Performance:**
- Tickets handled
- Average resolution time
- Customer satisfaction
- Active status

### Exporting Data

1. Select desired report
2. Choose date range
3. Click **"Export"** button
4. Download CSV or PDF

---

## Settings Page

### System Settings (Admin Only)

Configure global application settings:
- **Application Name**: Display name
- **Support Email**: Contact email
- **Business Hours**: Operating hours
- **Default Language**: System language

### Bot Configuration

Adjust AI chatbot behavior:
- **AI Provider**: OpenAI, Anthropic, or Mock
- **Model**: Specific AI model to use
- **Temperature**: Response creativity (0-1)
- **Max Tokens**: Response length limit
- **System Prompt**: Bot personality and instructions

### User Settings

Personal preferences:
- **Notification Preferences**: Email, SMS, in-app
- **Dashboard Layout**: Customize widget placement
- **Theme**: Light or dark mode
- **Language**: Interface language

---

## Chat Widget Guide

### For Website Visitors

The chat widget appears as a button in the bottom-right corner:

**To Start a Chat:**
1. Click the chat icon 💬
2. Widget expands to show chat interface
3. Type your question
4. Press Enter or click Send

**Sample Questions:**
- "What is my account balance?"
- "How do I transfer money?"
- "I forgot my password"
- "What are your credit card options?"

### AI Responses

The AI assistant will:
- ✅ Answer common banking questions
- ✅ Guide you through procedures
- ✅ Provide product information
- ✅ Connect you to a human agent if needed

### Escalating to Human Agent

The AI will escalate to a human agent when:
- You explicitly request it ("I want to speak to an agent")
- Your question requires account access
- The AI cannot answer confidently
- You express frustration

**What Happens When Escalated:**
1. AI notifies you about escalation
2. A support ticket is created automatically
3. Available agent receives notification
4. You'll be connected to live support

---

## Agent Workflows

### Morning Routine

1. **Login** to admin panel
2. **Check Dashboard** for overnight metrics
3. **Review Tickets** assigned to you
4. **Check Knowledge Base** for updates
5. **Set Status** to Available

### Handling New Tickets

**Step-by-Step:**
1. Ticket appears in **Tickets** page
2. Review customer information
3. Click **"Assign to Me"**
4. Read conversation history (if from chat)
5. Search **Knowledge Base** for solutions
6. Respond to customer via messages
7. Update ticket status as you progress
8. Mark as **RESOLVED** when complete

### Responding to Customers

**Best Practices:**
- ✅ Respond within 5 minutes
- ✅ Use customer's name
- ✅ Be empathetic and professional
- ✅ Provide clear, step-by-step instructions
- ✅ Follow up to ensure resolution
- ✅ Document all actions in ticket notes

**Template Responses:**
```
Hi [Customer Name],

Thank you for contacting JoxAI Bank support. I'm [Your Name], and I'm here to help you with [issue].

[Provide solution or next steps]

Is there anything else I can help you with today?

Best regards,
[Your Name]
JoxAI Bank Support Team
```

### End of Day Routine

1. **Resolve** all pending tickets (or update status)
2. **Document** unresolved issues
3. **Update** any relevant knowledge base articles
4. **Review** your performance metrics
5. **Set Status** to Offline

---

## Best Practices

### For Agents

**Communication:**
- Use professional, friendly language
- Avoid technical jargon
- Be patient and empathetic
- Confirm understanding before closing

**Efficiency:**
- Use knowledge base articles
- Create templates for common responses
- Keep tickets organized with proper status/priority
- Document solutions for future reference

**Quality:**
- Double-check information before sending
- Verify issue is resolved before closing
- Ask for feedback when appropriate
- Escalate complex issues to supervisors

### For Supervisors

**Team Management:**
- Monitor agent performance daily
- Provide constructive feedback
- Identify training opportunities
- Recognize outstanding performance

**Quality Assurance:**
- Review random ticket samples
- Ensure knowledge base is current
- Monitor customer satisfaction scores
- Address recurring issues

**Analytics:**
- Track key metrics weekly
- Identify bottlenecks
- Optimize workflows
- Report insights to management

### For Admins

**System Maintenance:**
- Review security logs regularly
- Update system settings as needed
- Manage user access and roles
- Monitor system performance

**Content Management:**
- Keep knowledge base updated
- Archive outdated articles
- Approve new content submissions
- Maintain data quality

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + K` | Quick search |
| `Ctrl/Cmd + /` | Show shortcuts |
| `T` | Go to Tickets |
| `C` | Go to Conversations |
| `D` | Go to Dashboard |
| `Esc` | Close modals |

---

## Troubleshooting

### Can't Login
- Check username/password
- Clear browser cache
- Try incognito/private mode
- Contact admin for password reset

### Ticket Not Loading
- Refresh the page
- Check internet connection
- Clear browser cache
- Contact technical support

### WebSocket Disconnected
- Check network connection
- Refresh the page
- System will auto-reconnect in 5 seconds

### AI Not Responding
- Verify AI provider is configured
- Check API key is valid
- Review system settings
- Contact administrator

---

## Getting Help

**Technical Support:**
- Email: support@joxaibank.com
- Phone: 1-800-JOXAI-HELP
- Live Chat: Available 24/7

**Documentation:**
- API Reference: `/docs/API_REFERENCE.md`
- Technical Docs: `/docs/TECHNICAL.md`
- FAQs: `/docs/FAQ.md`

---

**User Guide Version:** 1.0.0  
**Last Updated:** October 10, 2025  
**Next Review:** January 10, 2026
