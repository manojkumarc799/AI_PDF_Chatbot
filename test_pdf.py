from utils.pdf_processor import extract_text_from_pdf, create_chunks


pdf_path = "uploads/My ATS Friendly Resume.pdf"


pages = extract_text_from_pdf(pdf_path)

print("Number of pages:", len(pages))

for page in pages[:2]:
    print("\nPAGE:", page["page"])
    print(page["text"][:500])


chunks = create_chunks(pages)

print("\nNumber of chunks:", len(chunks))

for chunk in chunks[:3]:
    print("\nCHUNK")
    print("Page:", chunk["page"])
    print(chunk["text"][:300])