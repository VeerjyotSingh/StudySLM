#problem faced PDF may or maynot have a text layer
#need to check if the text given by pymupdf is real or just noise and use ocr if it fails

import time
import pymupdf
import os
from tqdm import tqdm
import re
import unicodedata
from nostril import ng
from nostril import nonsense_detector as nd

pdfDir = "/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT PDF"
textDir = "/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT Text"


def isNonsenseText(text):
    text = re.sub(r"[^a-zA-Z]", "", text)
    if nd.nonsense(text):
        return True
    else:
        return False

def readPDFAndWriteClean(fileName):
    doc = pymupdf.open("/Users/veerjyotsingh/Veerjyot/Computer/IOS app development/StudySLM/NCERT PDF/"+fileName)
    correctedLines = []
    for page in doc:
        rawText = page.get_text()
        lines = rawText.splitlines()

        for line in lines:
            line = unicodedata.normalize("NFKD", line)
            line = re.sub(r"[^a-zA-Z0-9\s.,;:!?()\[\]{}'\"-]", "", line)
            line = re.sub(r"\s+", " ", line).strip()
            if len(re.sub(r"[^a-zA-Z]", "", line)) > 10 and not isNonsenseText(line):
                if len(line) >= 5 and len(line.split()) > 2:
                    correctedLines.append(line + "\n")
    return correctedLines

def writeCorrectedLines(filename,correctedLines,outputPath=textDir):
    outName = filename.replace('.pdf', '.txt')
    outputPath = os.path.join(outputPath, outName)
    with open(outputPath, "w", encoding="utf-8") as f:
        f.writelines(correctedLines)
        
if __name__ == "__main__":
    print("Starting the job")
    start = time.time()

    pdfFiles = [f for f in os.listdir(pdfDir) if f.endswith(".pdf")]
    badFiles = []
    for filename in tqdm(pdfFiles, desc="Processing NCERT PDFs"):
        if filename.endswith(".pdf"):
            correctedLines = readPDFAndWriteClean(filename)
            if len(correctedLines) > 100:
                writeCorrectedLines(filename, correctedLines)
            else:
                badFiles.append(filename)

    end = time.time()
    print("✅ All PDFs processed.")
    print("⌛️Processing time: {:.2f} seconds.".format(end-start))
    print(badFiles)