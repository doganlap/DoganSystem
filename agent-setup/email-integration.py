"""
Email Integration for ERPNext Multi-Agent System
Handles email sending, receiving, and management for business needs
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging
import os
from dotenv import load_dotenv
import requests

from agent_orchestrator import ERPNextClient

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailManager:
    """Manages email operations for business needs"""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        imap_server: Optional[str] = None,
        imap_port: Optional[int] = None,
        use_tls: bool = True
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.imap_server = imap_server or smtp_server
        self.imap_port = imap_port or 993
        self.use_tls = use_tls

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        html: bool = False
    ) -> Dict[str, Any]:
        """Send an email"""
        try:
            msg = MIMEMultipart('alternative' if html else 'mixed')
            msg['From'] = self.smtp_username
            msg['To'] = to
            msg['Subject'] = subject

            if cc:
                msg['Cc'] = ', '.join(cc)

            # Add body
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            # Add attachments
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    with open(attachment['path'], 'rb') as f:
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {attachment["filename"]}'
                    )
                    msg.attach(part)

            # Send email
            recipients = [to]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg, to_addrs=recipients)

            logger.info(f"Email sent successfully to {to}")
            return {
                "success": True,
                "message": "Email sent successfully",
                "to": to,
                "subject": subject,
                "sent_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def read_emails(
        self,
        folder: str = "INBOX",
        limit: int = 10,
        unread_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Read emails from mailbox"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.smtp_username, self.smtp_password)
            mail.select(folder)

            # Search criteria
            search_criteria = "UNSEEN" if unread_only else "ALL"
            status, messages = mail.search(None, search_criteria)

            email_ids = messages[0].split()
            emails = []

            # Limit results
            for email_id in email_ids[-limit:]:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)

                # Extract email data
                email_data = {
                    "id": email_id.decode(),
                    "from": email_message["From"],
                    "to": email_message["To"],
                    "subject": email_message["Subject"],
                    "date": email_message["Date"],
                    "read": "UNSEEN" not in search_criteria
                }

                # Extract body
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            email_data["body"] = part.get_payload(decode=True).decode()
                            break
                        elif part.get_content_type() == "text/html":
                            if "body" not in email_data:
                                email_data["body"] = part.get_payload(decode=True).decode()
                                email_data["html"] = True
                else:
                    email_data["body"] = email_message.get_payload(decode=True).decode()

                emails.append(email_data)

            mail.close()
            mail.logout()

            return emails
        except Exception as e:
            logger.error(f"Error reading emails: {str(e)}")
            return []

    def mark_as_read(self, email_id: str, folder: str = "INBOX") -> bool:
        """Mark email as read"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.smtp_username, self.smtp_password)
            mail.select(folder)
            mail.store(email_id, '+FLAGS', '\\Seen')
            mail.close()
            mail.logout()
            return True
        except Exception as e:
            logger.error(f"Error marking email as read: {str(e)}")
            return False


class ERPNextEmailIntegration:
    """Integrates email with ERPNext for business needs"""

    def __init__(self, erpnext_client: ERPNextClient, email_manager: EmailManager):
        self.erpnext = erpnext_client
        self.email = email_manager

    def send_quotation_email(
        self,
        quotation_name: str,
        recipient_email: str,
        custom_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send quotation via email"""
        try:
            # Get quotation from ERPNext
            quotation = self.erpnext.get("Quotation", filters={"name": quotation_name})

            if not quotation.get("data"):
                return {"success": False, "error": "Quotation not found"}

            quote_data = quotation["data"][0]

            # Create email body
            subject = f"Quotation: {quote_data.get('title', quotation_name)}"
            body = custom_message or f"""
Dear Customer,

Please find attached our quotation for your reference.

Quotation Details:
- Quotation Number: {quotation_name}
- Customer: {quote_data.get('customer_name', 'N/A')}
- Total Amount: {quote_data.get('grand_total', 'N/A')}
- Valid Until: {quote_data.get('valid_till', 'N/A')}

Please feel free to contact us if you have any questions.

Best regards,
Sales Team
"""

            # Send email
            result = self.email.send_email(
                to=recipient_email,
                subject=subject,
                body=body
            )

            # Log in ERPNext
            if result["success"]:
                self._log_email_communication(
                    reference_doctype="Quotation",
                    reference_name=quotation_name,
                    recipient=recipient_email,
                    subject=subject
                )

            return result
        except Exception as e:
            logger.error(f"Error sending quotation email: {str(e)}")
            return {"success": False, "error": str(e)}

    def send_invoice_email(
        self,
        invoice_name: str,
        recipient_email: str,
        custom_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send invoice via email"""
        try:
            # Get invoice from ERPNext
            invoice = self.erpnext.get("Sales Invoice", filters={"name": invoice_name})

            if not invoice.get("data"):
                return {"success": False, "error": "Invoice not found"}

            invoice_data = invoice["data"][0]

            # Create email body
            subject = f"Invoice: {invoice_name}"
            body = custom_message or f"""
Dear Customer,

Please find attached invoice for your payment.

Invoice Details:
- Invoice Number: {invoice_name}
- Customer: {invoice_data.get('customer_name', 'N/A')}
- Total Amount: {invoice_data.get('grand_total', 'N/A')}
- Due Date: {invoice_data.get('due_date', 'N/A')}

Payment instructions are included in the invoice.

Thank you for your business.

Best regards,
Accounts Team
"""

            # Send email
            result = self.email.send_email(
                to=recipient_email,
                subject=subject,
                body=body
            )

            # Log in ERPNext
            if result["success"]:
                self._log_email_communication(
                    reference_doctype="Sales Invoice",
                    reference_name=invoice_name,
                    recipient=recipient_email,
                    subject=subject
                )

            return result
        except Exception as e:
            logger.error(f"Error sending invoice email: {str(e)}")
            return {"success": False, "error": str(e)}

    def send_customer_welcome_email(
        self,
        customer_name: str,
        recipient_email: str
    ) -> Dict[str, Any]:
        """Send welcome email to new customer"""
        try:
            # Get customer from ERPNext
            customer = self.erpnext.get("Customer", filters={"name": customer_name})

            if not customer.get("data"):
                return {"success": False, "error": "Customer not found"}

            customer_data = customer["data"][0]

            subject = "Welcome to Our Company!"
            body = f"""
Dear {customer_data.get('customer_name', 'Valued Customer')},

Welcome to our company! We're excited to have you as our customer.

Your customer account has been created:
- Customer ID: {customer_name}
- Customer Name: {customer_data.get('customer_name', 'N/A')}

We look forward to serving you and providing excellent service.

If you have any questions, please don't hesitate to contact us.

Best regards,
Customer Service Team
"""

            result = self.email.send_email(
                to=recipient_email,
                subject=subject,
                body=body
            )

            return result
        except Exception as e:
            logger.error(f"Error sending welcome email: {str(e)}")
            return {"success": False, "error": str(e)}

    def process_incoming_emails(self) -> List[Dict[str, Any]]:
        """Process incoming emails and create leads/contacts in ERPNext"""
        emails = self.email.read_emails(unread_only=True, limit=20)
        processed = []

        for email_data in emails:
            try:
                # Extract email information
                sender_email = email_data["from"]
                subject = email_data["subject"]
                body = email_data["body"]

                # Check if contact exists
                contacts = self.erpnext.get(
                    "Contact",
                    filters={"email_id": sender_email}
                )

                if not contacts.get("data"):
                    # Create new contact/lead
                    # Extract name from email
                    name = sender_email.split("@")[0].replace(".", " ").title()

                    # Create lead
                    lead_data = {
                        "lead_name": name,
                        "email_id": sender_email,
                        "source": "Email",
                        "status": "Open"
                    }

                    lead_result = self.erpnext.post("Lead", lead_data)
                    processed.append({
                        "email_id": email_data["id"],
                        "action": "created_lead",
                        "lead_name": lead_result.get("data", {}).get("name")
                    })

                # Mark email as read
                self.email.mark_as_read(email_data["id"])

            except Exception as e:
                logger.error(f"Error processing email {email_data.get('id')}: {str(e)}")
                processed.append({
                    "email_id": email_data.get("id"),
                    "action": "error",
                    "error": str(e)
                })

        return processed

    def send_notification_email(
        self,
        recipient_email: str,
        notification_type: str,
        message: str,
        reference_doctype: Optional[str] = None,
        reference_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send business notification email"""
        subject_map = {
            "order_confirmed": "Order Confirmation",
            "payment_received": "Payment Received",
            "shipment_sent": "Shipment Sent",
            "invoice_due": "Invoice Payment Due",
            "custom": "Business Notification"
        }

        subject = subject_map.get(notification_type, "Business Notification")

        body = f"""
{message}

"""

        if reference_doctype and reference_name:
            body += f"Reference: {reference_doctype} - {reference_name}\n"

        body += """
Thank you for your business.

Best regards,
Business System
"""

        return self.email.send_email(
            to=recipient_email,
            subject=subject,
            body=body
        )

    def _log_email_communication(
        self,
        reference_doctype: str,
        reference_name: str,
        recipient: str,
        subject: str
    ):
        """Log email communication in ERPNext"""
        try:
            # Create communication log
            communication_data = {
                "communication_type": "Communication",
                "reference_doctype": reference_doctype,
                "reference_name": reference_name,
                "recipients": recipient,
                "subject": subject,
                "sent_or_received": "Sent",
                "communication_date": datetime.now().isoformat()
            }

            self.erpnext.post("Communication", communication_data)
        except Exception as e:
            logger.warning(f"Could not log communication: {str(e)}")


class EmailAgent:
    """Email-enabled agent for business email management"""

    def __init__(
        self,
        erpnext_email: ERPNextEmailIntegration,
        agent_name: str
    ):
        self.erpnext_email = erpnext_email
        self.agent_name = agent_name

    def handle_email_request(self, request: str) -> Dict[str, Any]:
        """Handle email-related requests"""
        request_lower = request.lower()

        if "send quotation" in request_lower or "quote" in request_lower:
            # Extract quotation name and email from request
            # This is simplified - in production, use NLP to extract
            return {"action": "send_quotation", "message": "Please provide quotation name and recipient email"}

        elif "send invoice" in request_lower:
            return {"action": "send_invoice", "message": "Please provide invoice name and recipient email"}

        elif "process emails" in request_lower or "check emails" in request_lower:
            processed = self.erpnext_email.process_incoming_emails()
            return {
                "action": "process_emails",
                "processed_count": len(processed),
                "details": processed
            }

        elif "read emails" in request_lower:
            emails = self.erpnext_email.email.read_emails(limit=10)
            return {
                "action": "read_emails",
                "count": len(emails),
                "emails": emails
            }

        else:
            return {"action": "unknown", "message": "Email request not recognized"}
