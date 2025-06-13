import pymupdf

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

readPDF('nrt(1).pdf')
cleanText('nrt(1).pdf')