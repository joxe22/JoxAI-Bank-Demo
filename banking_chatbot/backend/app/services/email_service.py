import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from datetime import datetime
import time

from app.models.db_notification import NotificationType, NotificationStatus, NotificationCategory


class EmailService:
    """
    Email notification service for sending transactional emails.
    Supports SMTP configuration via environment variables.
    """
    
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_user)
        self.from_name = os.getenv("FROM_NAME", "JoxAI Banking Chatbot")
        
        # Check if email is configured
        self.is_configured = bool(self.smtp_user and self.smtp_password)
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Send an email via SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            body: Plain text email body
            html_body: Optional HTML version of email body
        
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        if not self.is_configured:
            return False, "Email not configured. Set SMTP_USER and SMTP_PASSWORD environment variables."
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach plain text
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach HTML if provided
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    def send_ticket_assigned_notification(
        self,
        agent_email: str,
        agent_name: str,
        ticket_id: str,
        customer_name: str,
        subject: str,
        priority: str
    ) -> tuple[bool, Optional[str]]:
        """Send notification when a ticket is assigned to an agent."""
        
        email_subject = f"New Ticket Assigned: {ticket_id}"
        
        plain_body = f"""
Hello {agent_name},

A new support ticket has been assigned to you:

Ticket ID: {ticket_id}
Customer: {customer_name}
Subject: {subject}
Priority: {priority}

Please review and respond to this ticket as soon as possible.

Best regards,
JoxAI Banking Chatbot System
"""
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 20px; }}
        .ticket-info {{ background-color: white; padding: 15px; margin: 15px 0; border-left: 4px solid #007bff; }}
        .ticket-info p {{ margin: 5px 0; }}
        .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>New Ticket Assigned</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{agent_name}</strong>,</p>
            <p>A new support ticket has been assigned to you:</p>
            
            <div class="ticket-info">
                <p><strong>Ticket ID:</strong> {ticket_id}</p>
                <p><strong>Customer:</strong> {customer_name}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Priority:</strong> <span style="color: {'#dc3545' if priority == 'HIGH' or priority == 'URGENT' else '#ffc107' if priority == 'MEDIUM' else '#28a745'};">{priority}</span></p>
            </div>
            
            <p>Please review and respond to this ticket as soon as possible.</p>
        </div>
        <div class="footer">
            <p>JoxAI Banking Chatbot System</p>
        </div>
    </div>
</body>
</html>
"""
        
        return self.send_email(agent_email, email_subject, plain_body, html_body)
    
    def send_ticket_status_changed_notification(
        self,
        email: str,
        name: str,
        ticket_id: str,
        old_status: str,
        new_status: str,
        subject: str
    ) -> tuple[bool, Optional[str]]:
        """Send notification when ticket status changes."""
        
        email_subject = f"Ticket {ticket_id} Status Updated"
        
        plain_body = f"""
Hello {name},

Your support ticket status has been updated:

Ticket ID: {ticket_id}
Subject: {subject}
Previous Status: {old_status}
New Status: {new_status}

Best regards,
JoxAI Banking Chatbot System
"""
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; }}
        .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 20px; }}
        .status-change {{ background-color: white; padding: 15px; margin: 15px 0; }}
        .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Ticket Status Updated</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{name}</strong>,</p>
            <p>Your support ticket status has been updated:</p>
            
            <div class="status-change">
                <p><strong>Ticket ID:</strong> {ticket_id}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Previous Status:</strong> {old_status}</p>
                <p><strong>New Status:</strong> {new_status}</p>
            </div>
        </div>
        <div class="footer">
            <p>JoxAI Banking Chatbot System</p>
        </div>
    </div>
</body>
</html>
"""
        
        return self.send_email(email, email_subject, plain_body, html_body)
    
    def send_ticket_escalated_notification(
        self,
        email: str,
        name: str,
        ticket_id: str,
        customer_name: str,
        reason: str
    ) -> tuple[bool, Optional[str]]:
        """Send notification when conversation is escalated to ticket."""
        
        email_subject = f"Urgent: New Escalated Ticket {ticket_id}"
        
        plain_body = f"""
Hello {name},

A customer conversation has been escalated to a support ticket:

Ticket ID: {ticket_id}
Customer: {customer_name}
Escalation Reason: {reason}
Priority: HIGH

This ticket requires immediate attention.

Best regards,
JoxAI Banking Chatbot System
"""
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; }}
        .content {{ background-color: #f9f9f9; padding: 20px; margin-top: 20px; }}
        .urgent {{ background-color: #fff3cd; padding: 15px; margin: 15px 0; border-left: 4px solid #dc3545; }}
        .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚠️ Urgent: New Escalated Ticket</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{name}</strong>,</p>
            <p>A customer conversation has been escalated to a support ticket:</p>
            
            <div class="urgent">
                <p><strong>Ticket ID:</strong> {ticket_id}</p>
                <p><strong>Customer:</strong> {customer_name}</p>
                <p><strong>Escalation Reason:</strong> {reason}</p>
                <p><strong>Priority:</strong> <span style="color: #dc3545;">HIGH</span></p>
            </div>
            
            <p><strong>This ticket requires immediate attention.</strong></p>
        </div>
        <div class="footer">
            <p>JoxAI Banking Chatbot System</p>
        </div>
    </div>
</body>
</html>
"""
        
        return self.send_email(email, email_subject, plain_body, html_body)


# Singleton instance
email_service = EmailService()
