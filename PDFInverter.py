from PIL import Image
import PIL.ImageOps
import sys
import os, fitz


pdffile = "pdf.pdf"
doc = fitz.open(pdffile)
pagelist = []

for i in range(len(doc)):
    page = doc.loadPage(i)  # number of page
    zoom_x = 3.0  # horizontal zoom
    zoom_y = 3.0  # vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension
    pix = page.get_pixmap(matrix=mat)  # use 'mat' instead of the identity matrix
    pix.invertIRect()
    output = f"page{i}.png"
    pagelist.append(output)
    pix.writePNG(pagelist[i])

imglist = []

doc = fitz.open()  # PDF with the pictures
imgdir = os.getcwd()  # where the pics are
for file in os.listdir(imgdir):
    if file.endswith(".png"):
        imglist.append(os.listdir(imgdir))
imgcount = len(imglist)  # pic count

for f in range(imgcount):
    img = fitz.open(f"page{f}.png")  # open pic as document
    rect = img[0].rect  # pic dimension
    pdfbytes = img.convert_to_pdf()  # make a PDF stream
    img.close()  # no longer needed
    imgPDF = fitz.open("pdfinv", pdfbytes)  # open stream as PDF
    page = doc.new_page(width=rect.width,  # new page with ...
                        height=rect.height)  # pic dimension
    page.show_pdf_page(rect, imgPDF, 0)  # image fills the page

doc.save("pdfinv.pdf")
