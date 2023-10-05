import imaplib
import email
from email.header import decode_header
import time

# Ganti dengan detail server email Anda
IMAP_SERVER = "mail.bariqfirjatullah.my.id"
IMAP_PORT = 993
EMAIL_ADDRESS = "owner@bariqfirjatullah.my.id"
PASSWORD = "aku089619"
MAILBOX = "inbox"


def read_emails():
    # Connect to the server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login to the mailbox
    mail.login(EMAIL_ADDRESS, PASSWORD)

    # Select the mailbox
    mail.select(MAILBOX)

    # Search for emails and get the latest 3 email IDs
    status, email_ids = mail.search(None, "ALL")
    email_id_list = email_ids[0].split()[-3:]  # Ambil 3 ID terbaru

    for email_id in email_id_list:
        # Fetch the email
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, _ = decode_header(msg["Subject"])[0]
        from_, _ = decode_header(msg["From"])[0]

        print("Subject:", subject)
        print("From:", from_)

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if "attachment" in content_type:
                    filename = part.get_filename()
                    print("Attachment:", filename)

        print("=" * 30)

    # Logout and close the connection
    mail.logout()


def main():
    while True:
        read_emails()

        # Tunda selama beberapa detik sebelum membaca email lagi
        # time.sleep(30)  # Ganti angka sesuai kebutuhan

        # Menambahkan opsi refresh
        refresh = input("Apakah Anda ingin memuat ulang email? (yes/no): ")
        if refresh.lower() == "yes":
            read_emails()


if __name__ == "__main__":
    main()