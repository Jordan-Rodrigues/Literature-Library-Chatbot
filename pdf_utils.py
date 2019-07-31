from PyPDF2 import PdfFileWriter, PdfFileReader
import PyPDF2
import requests
import io
from wand.image import Image

all_urls = ['https://literature.rockwellautomation.com/idc/groups/literature/documents/rn/1441-rn002_-en-p.pdf',
        'https://literature.rockwellautomation.com/idc/groups/literature/documents/in/800mr-in001_-en-e.pdf',
        'https://literature.rockwellautomation.com/idc/groups/literature/documents/td/1500-td220_-en-e.pdf']

url = 'https://literature.rockwellautomation.com/idc/groups/literature/documents/rn/1441-rn002_-en-p.pdf'
all_content = [] # List to hold strings from all pages in a PDF



def get_text(url):

        r = requests.get(url) # Grab URL
        pdf_file = io.BytesIO(r.content) # Downloads PDF file as a byte stream (only in memory never saved locally)
        #pdf_file = open(file_name, 'rb') # Opens PDF file from directory
        read_pdf = PdfFileReader(pdf_file) # Reads in PDF
        number_of_pages = read_pdf.getNumPages() # Gets number of pages

        for pages in range(number_of_pages): # loops through all pages in PDF
                page = read_pdf.getPage(pages)
                page_content = page.extractText() #.replace('\n', '') # Extracts text from current page & cleans up newlines
                all_content.append(page_content.encode('utf-8')) # Adds string of text from current page to list

        return number_of_pages, all_content


def get_image(url,page_num, resolution = 70, save=False, save_name=""):
        
        # in order to use this method, see installation instructions here https://stackoverflow.com/questions/13984357/pythonmagick-cant-find-my-pdf-files
        r = requests.get(url) # Grab URL
        pdf_file = io.BytesIO(r.content) # Downloads PDF file as a byte stream (only in memory never saved locally)
        src_pdf = PdfFileReader(pdf_file) # Reads in PDF
        dst_pdf = PyPDF2.PdfFileWriter()
        dst_pdf.addPage(src_pdf.getPage(page_num)) # get page_num

        pdf_bytes = io.BytesIO()
        dst_pdf.write(pdf_bytes)
        pdf_bytes.seek(0)

        img = Image(file = pdf_bytes, resolution = resolution)
        single = Image(img.sequence[0])
        single.convert("png")

        if save:
                img.save(filename=save_name)
        return single

save_image(get_image(url,1))