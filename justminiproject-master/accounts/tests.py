import smtplib

def test_smtp_connection():
    try:
        # Establish an SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        
        # Start TLS encryption
        server.starttls()
        
        # Login to the SMTP server using your email credentials
        server.login('jamesharrypotter8@gmail.com', 'Narendra@123')
        
        # Close the connection
        server.quit()
        
        print("SMTP connection test successful!")
    except Exception as e:
        print("SMTP connection test failed:", str(e))



print(test_smtp_connection())
