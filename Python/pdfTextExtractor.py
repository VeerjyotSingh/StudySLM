import time
import pymupdf
import os
from tqdm import tqdm

pdf_dir = "/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT PDF"
text_dir = "/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT Text"


def readPDF(fileName):
    outName = fileName.replace('.pdf', '.txt')
    doc = pymupdf.open("/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT PDF/"+fileName)
    out = open("/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT Text/"+outName,"wb")
    for page in doc:
        text = page.get_text().encode("utf8")
        out.write(text)
        out.write(bytes((12,)))
    out.close()

def cleanText(fileName):
    fileName = fileName.replace('.pdf', '.txt')
    file = open("/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT Text/"+fileName,"r")
    lines = file.readlines()
    correctedlines = []
    for line in lines:
        if len(line.strip()) < 5:
            continue
        else:
            correctedlines.append(line.strip() + "\n")
    file.close()
    file = open("/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT Text/" + fileName, "w")
    file.writelines(correctedlines)
    file.close()

print("Starting the job")
start = time.time()

pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

for filename in tqdm(pdf_files, desc="Processing NCERT PDFs"):
    if filename.endswith(".pdf"):
        readPDF(filename)
        cleanText(filename)

end = time.time()
print("✅ All PDFs processed.")
print("Processing time: {:.2f} seconds.".format(end-start))