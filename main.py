import streamlit
import pandas as pd
import fitz
import re
import os
def createTOCFile(bookName,toc_list):
    TOCFILE = open(bookName+"\Slice_Data.txt","x")
    TOCFILE.write(bookName+"\n")
    for chapter in toc_list:
        TOCFILE.write(str(chapter[0])+" | "+chapter[1]+" | "+str(chapter[2])+"\n")
    TOCFILE.close()
def validFilename(filename:str):
    validify = re.sub('\W+',"_",filename)
    return validify
#end is not included
def createSubPDF(reader,start,end,filename:str,bookName):
    newPDF = fitz.open()
    newPDF.insert_pdf(reader,start-1,end-2)
    
    newPDF.save(bookName+"\\"+("_").join(filename.split(" "))+".pdf")


def simplifyToc(Toc):
    toc_simplified=[]
    toc_simplified.append([1,"Cover",0])
    for part in Toc:
        if part[0]==1:
            toc_simplified.append(part)
    toc_simplified.append([1,"End",totalPages])
    return toc_simplified
#Title
streamlit.title("PDF SLICER")

#get PDF file
pdf_file = streamlit.file_uploader("PDF",type="pdf")

if pdf_file != None:
    streamlit.toast("Uploaded.")
    Reader = fitz.open(filetype="pdf",stream=pdf_file.read())

    streamlit.toast("Loaded.")

    totalPages = Reader.page_count
    toc_l1=simplifyToc(Reader.get_toc())
    Dataframe = pd.DataFrame(toc_l1)

    streamlit.header("Preview")
    streamlit.table(Dataframe)
    streamlit.write(f"There will be {len(toc_l1)-2} Sliced PDFs.")

    buttonSlice = streamlit.button("Slice")    
    folderName = validFilename(pdf_file.name)
    if buttonSlice:
        os.mkdir(folderName)
        createTOCFile(folderName,toc_l1)
        for i in range(len(toc_l1)-1):
            createSubPDF(Reader,toc_l1[i][2],toc_l1[i+1][2],validFilename(toc_l1[i][1]),folderName)
        
        


    
