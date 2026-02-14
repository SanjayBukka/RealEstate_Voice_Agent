"""
Appointment Agent - Handles scheduling and email notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import re

class AppointmentAgent:
    def __init__(self):
        # SMTP Configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "sanjaybukka11@gmail.com"
        self.app_password = "etxi imqy gici aqxr"
        
        # Field Visit Officer
        self.field_officer_email = "praveen19121@gmail.com"
        self.field_officer_name = "Praveen"
        
        # Company info
        self.company_name = "Premium Real Estate Services"
        self.company_phone = "+1 (469) 555-1234"
    
    def send_email(self, to_email, subject, html_body, plain_body=None):
        """Send email using SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.company_name} <{self.sender_email}>"
            msg['To'] = to_email
            
            # Plain text version
            if plain_body:
                part1 = MIMEText(plain_body, 'plain')
                msg.attach(part1)
            
            # HTML version
            part2 = MIMEText(html_body, 'html')
            msg.attach(part2)
            
            # Connect and send
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.sendmail(self.sender_email, to_email, msg.as_string())
            server.quit()
            
            print(f"✅ Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {str(e)}")
            return False
    
    def schedule_site_visit(self, customer_info, property_info, visit_time="morning"):
        """Schedule a site visit and send confirmation emails"""
        
        # Get customer details
        customer_name = customer_info.get('name', 'Valued Customer')
        customer_email = customer_info.get('email', '')
        customer_phone = customer_info.get('phone', 'Not provided')
        
        # Get property details
        property_name = property_info.get('name', 'Property')
        property_address = property_info.get('address', '')
        property_price = property_info.get('price', '')
        property_type = property_info.get('type', 'property')
        
        # Calculate visit date (next business day)
        visit_date = datetime.now() + timedelta(days=1)
        if visit_date.weekday() == 5:  # Saturday
            visit_date += timedelta(days=2)
        elif visit_date.weekday() == 6:  # Sunday
            visit_date += timedelta(days=1)
        
        # Set visit time
        if visit_time.lower() == "morning":
            visit_time_str = "9:00 AM - 11:00 AM"
        elif visit_time.lower() == "afternoon":
            visit_time_str = "2:00 PM - 4:00 PM"
        else:
            visit_time_str = "10:00 AM - 12:00 PM"
        
        visit_date_str = visit_date.strftime("%A, %B %d, %Y")
        
        # Generate booking reference
        booking_ref = f"SV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        results = {
            'booking_ref': booking_ref,
            'visit_date': visit_date_str,
            'visit_time': visit_time_str,
            'customer_email_sent': False,
            'officer_email_sent': False
        }
        
        # Send customer confirmation email
        if customer_email:
            customer_sent = self._send_customer_confirmation(
                customer_name, customer_email, booking_ref,
                property_name, property_address, property_price,
                visit_date_str, visit_time_str
            )
            results['customer_email_sent'] = customer_sent
        
        # Send field officer notification
        officer_sent = self._send_officer_notification(
            customer_name, customer_email, customer_phone,
            booking_ref, property_name, property_address,
            property_price, property_type, visit_date_str, visit_time_str
        )
        results['officer_email_sent'] = officer_sent
        
        return results
    
    def _send_customer_confirmation(self, name, email, booking_ref, 
                                     property_name, address, price,
                                     visit_date, visit_time):
        """Send confirmation email to customer"""
        
        subject = f"🏠 Site Visit Confirmed - {booking_ref}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .booking-ref {{ background: #e3f2fd; padding: 15px; border-radius: 8px; text-align: center; margin: 20px 0; }}
                .property-card {{ background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                .btn {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; display: inline-block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏠 Site Visit Confirmed!</h1>
                    <p>Thank you for choosing {self.company_name}</p>
                </div>
                <div class="content">
                    <p>Dear <strong>{name}</strong>,</p>
                    
                    <p>Great news! Your property site visit has been confirmed. Here are your booking details:</p>
                    
                    <div class="booking-ref">
                        <small>Booking Reference</small>
                        <h2 style="margin: 5px 0; color: #667eea;">{booking_ref}</h2>
                    </div>
                    
                    <div class="property-card">
                        <h3 style="margin-top: 0;">📍 Property Details</h3>
                        <div class="detail-row">
                            <span>Property:</span>
                            <strong>{property_name}</strong>
                        </div>
                        <div class="detail-row">
                            <span>Address:</span>
                            <strong>{address}</strong>
                        </div>
                        <div class="detail-row">
                            <span>Price:</span>
                            <strong>{price}</strong>
                        </div>
                    </div>
                    
                    <div class="property-card">
                        <h3 style="margin-top: 0;">📅 Visit Schedule</h3>
                        <div class="detail-row">
                            <span>Date:</span>
                            <strong>{visit_date}</strong>
                        </div>
                        <div class="detail-row">
                            <span>Time:</span>
                            <strong>{visit_time}</strong>
                        </div>
                        <div class="detail-row">
                            <span>Your Agent:</span>
                            <strong>{self.field_officer_name}</strong>
                        </div>
                    </div>
                    
                    <h3>📝 What to Bring</h3>
                    <ul>
                        <li>Valid ID proof</li>
                        <li>This confirmation email</li>
                        <li>Any questions you may have</li>
                    </ul>
                    
                    <p style="background: #fff3e0; padding: 15px; border-radius: 8px;">
                        <strong>⚠️ Important:</strong> Please arrive 10 minutes early. If you need to reschedule, 
                        contact us at least 24 hours in advance.
                    </p>
                    
                    <p>If you have any questions, feel free to reach out:</p>
                    <p>📞 {self.company_phone}<br>
                    📧 {self.sender_email}</p>
                    
                    <p>We look forward to meeting you!</p>
                    
                    <p>Best regards,<br>
                    <strong>{self.company_name}</strong></p>
                </div>
                <div class="footer">
                    <p>© 2026 {self.company_name}. All rights reserved.</p>
                    <p>This is an automated confirmation email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_body = f"""
        Site Visit Confirmation - {booking_ref}
        
        Dear {name},
        
        Your site visit has been confirmed!
        
        BOOKING DETAILS:
        - Reference: {booking_ref}
        - Property: {property_name}
        - Address: {address}
        - Price: {price}
        
        VISIT SCHEDULE:
        - Date: {visit_date}
        - Time: {visit_time}
        - Agent: {self.field_officer_name}
        
        Please arrive 10 minutes early and bring a valid ID.
        
        Contact: {self.company_phone}
        
        Best regards,
        {self.company_name}
        """
        
        return self.send_email(email, subject, html_body, plain_body)
    
    def _send_officer_notification(self, customer_name, customer_email, 
                                    customer_phone, booking_ref,
                                    property_name, address, price,
                                    property_type, visit_date, visit_time):
        """Send notification email to field visit officer"""
        
        subject = f"🔔 New Site Visit Assignment - {booking_ref}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #28a745; color: white; padding: 25px; text-align: center; border-radius: 10px 10px 0 0; }}
                .urgent {{ background: #dc3545; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; padding: 20px; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .label {{ color: #666; font-size: 12px; text-transform: uppercase; }}
                .value {{ font-size: 16px; font-weight: bold; color: #333; margin-bottom: 10px; }}
                .highlight {{ background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; }}
                .footer {{ text-align: center; padding: 15px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔔 New Site Visit Assignment</h1>
                    <p>A new customer is scheduled to visit!</p>
                </div>
                <div class="content">
                    <p>Hi <strong>{self.field_officer_name}</strong>,</p>
                    
                    <p>You have been assigned a new site visit. Please review the details below:</p>
                    
                    <div class="highlight">
                        <strong>📅 Visit Schedule</strong><br>
                        Date: <strong>{visit_date}</strong><br>
                        Time: <strong>{visit_time}</strong><br>
                        Reference: <strong>{booking_ref}</strong>
                    </div>
                    
                    <div class="info-box">
                        <h3 style="margin-top: 0; color: #667eea;">👤 Customer Information</h3>
                        <div class="label">Name</div>
                        <div class="value">{customer_name}</div>
                        <div class="label">Email</div>
                        <div class="value">{customer_email}</div>
                        <div class="label">Phone</div>
                        <div class="value">{customer_phone}</div>
                    </div>
                    
                    <div class="info-box">
                        <h3 style="margin-top: 0; color: #667eea;">🏠 Property Details</h3>
                        <div class="label">Property Type</div>
                        <div class="value">{property_type.title()}</div>
                        <div class="label">Property</div>
                        <div class="value">{property_name}</div>
                        <div class="label">Address</div>
                        <div class="value">{address}</div>
                        <div class="label">Price</div>
                        <div class="value">{price}</div>
                    </div>
                    
                    <h3>📋 Action Items</h3>
                    <ul>
                        <li>Review property details before the visit</li>
                        <li>Prepare necessary documents and keys</li>
                        <li>Arrive 15 minutes before scheduled time</li>
                        <li>Contact customer if any changes occur</li>
                    </ul>
                    
                    <p style="background: #e8f5e9; padding: 15px; border-radius: 8px;">
                        <strong>✅ Customer has been notified</strong> - A confirmation email has been sent to the customer with your name as the assigned agent.
                    </p>
                    
                    <p>Please confirm your availability by replying to this email.</p>
                    
                    <p>Best regards,<br>
                    <strong>{self.company_name} - Booking System</strong></p>
                </div>
                <div class="footer">
                    <p>This is an automated notification from the Real Estate AI Agent system.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_body = f"""
        NEW SITE VISIT ASSIGNMENT - {booking_ref}
        
        Hi {self.field_officer_name},
        
        You have a new site visit scheduled:
        
        VISIT SCHEDULE:
        - Date: {visit_date}
        - Time: {visit_time}
        - Reference: {booking_ref}
        
        CUSTOMER INFORMATION:
        - Name: {customer_name}
        - Email: {customer_email}
        - Phone: {customer_phone}
        
        PROPERTY DETAILS:
        - Type: {property_type}
        - Property: {property_name}
        - Address: {address}
        - Price: {price}
        
        Please confirm your availability.
        
        {self.company_name} - Booking System
        """
        
        return self.send_email(self.field_officer_email, subject, html_body, plain_body)


# Test function
if __name__ == "__main__":
    agent = AppointmentAgent()
    
    # Test data
    customer_info = {
        'name': 'Sanjay',
        'email': 'sanjaybukka28@gmail.com',
        'phone': '+1 (469) 555-9999'
    }
    
    property_info = {
        'name': 'Luxury Apartment in Downtown Dallas',
        'address': '123 Main Street, Downtown Dallas, TX 75201',
        'price': '$1,800,000',
        'type': 'apartment'
    }
    
    result = agent.schedule_site_visit(customer_info, property_info, 'morning')
    print(f"\nBooking Result: {result}")
