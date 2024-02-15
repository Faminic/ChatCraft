from fpdf import FPDF
import re

def create_chat_history_pdf(messages, recipient):
    full_chat_history = []
    for message in messages:
        if message["role"] == "user":
            full_chat_history.append(f'You: {message["content"]}')
        else:
            full_chat_history.append(f'{recipient}: {message["content"]}')
        full_chat_history.append('----------------------------------------------------------------------------------------------')
    
    file_name = "chat_history.pdf"
    new_pdf = FPDF()
    new_pdf.add_page()
    new_pdf.set_font("Arial", size=20)
    new_pdf.cell(200, 10, txt="Chat History", ln=1, align="C")
    new_pdf.set_font("Arial", size=15)
    
    for item in full_chat_history:
        item = re.sub(r'[^\x00-\x7F]', ' ', item).strip() #remove non-ascii characters
        item = re.sub(r'\n\s*\n', '\n\n', item) #remove extra newlines
        new_pdf.multi_cell(200, 10, txt=item, align="L")

    new_pdf.output(name = file_name, dest='F')