import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

st.set_page_config(page_title="Fix My PDF", layout="centered")
st.title("📄 Fix My PDF")
st.caption("Merge • Split • Unlock • Rotate • Extract • Watermark • Compress")

# ======================================================================================================================
# UI
# ======================================================================================================================
operation = st.selectbox(
    "Choose Operation",
    [
        "Merge PDFs",
        "Split PDF",
        "Unlock PDF",
        "Rotate PDF",
        "Extract Pages",
        "Add Watermark",
        "Compress PDF"
    ]
)

uploaded_files = st.file_uploader(
    "Upload PDF file(s)",
    type=["pdf"],
    accept_multiple_files=True
)

password = st.text_input("PDF Password (if applicable)", type="password")

def safe_decrypt(reader, pwd):
    if reader.is_encrypted:
        if not pwd or not reader.decrypt(pwd):
            raise ValueError("Incorrect or missing PDF password")

def download_button(data, name):
    st.download_button(
        "⬇️ Download Result",
        data=data,
        file_name=name,
        mime="application/pdf"
    )

# ======================================================================================================================
# OPERATIONS
# ======================================================================================================================
try:
    # =====| MERGE |=====
    if operation == "Merge PDFs" and uploaded_files:
        writer = PdfWriter()
        for f in uploaded_files:
            reader = PdfReader(f)
            safe_decrypt(reader, password)
            for page in reader.pages:
                writer.add_page(page)

        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        st.success("PDFs merged successfully!")
        download_button(buf, "merged.pdf")

    # =====| SPLIT |=====
    elif operation == "Split PDF" and uploaded_files:
        reader = PdfReader(uploaded_files[0])
        safe_decrypt(reader, password)

        if len(reader.pages) < 2:
            st.error("PDF must have at least 2 pages to split.")
        else:
            page_no = st.number_input(
                "Split after page number",
                min_value=1,
                max_value=len(reader.pages) - 1
            )

            w1, w2 = PdfWriter(), PdfWriter()
            for i, page in enumerate(reader.pages):
                (w1 if i < page_no else w2).add_page(page)

            b1, b2 = io.BytesIO(), io.BytesIO()
            w1.write(b1); b1.seek(0)
            w2.write(b2); b2.seek(0)

            st.success("PDF split successfully!")
            download_button(b1, "split_part_1.pdf")
            download_button(b2, "split_part_2.pdf")

    # =====| UNLOCK |=====
    elif operation == "Unlock PDF" and uploaded_files:
        reader = PdfReader(uploaded_files[0])
        if not reader.is_encrypted:
            st.info("PDF is already unlocked.")
        else:
            safe_decrypt(reader, password)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            buf = io.BytesIO()
            writer.write(buf)
            buf.seek(0)
            st.success("PDF unlocked successfully!")
            download_button(buf, "unlocked.pdf")

    # =====| ROTATE |=====
    elif operation == "Rotate PDF" and uploaded_files:
        angle = st.selectbox("Rotate Angle", [90, 180, 270])
        reader = PdfReader(uploaded_files[0])
        safe_decrypt(reader, password)

        writer = PdfWriter()
        for page in reader.pages:
            page.rotate(angle)
            writer.add_page(page)

        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        st.success("PDF rotated successfully!")
        download_button(buf, "rotated.pdf")
    # =====| EXTRACT |=====
    elif operation == "Extract Pages" and uploaded_files:
        pages_input = st.text_input(
            "Pages (e.g. 1,3,5-7)",
            value="1"   # ✅ default value
        )

        reader = PdfReader(uploaded_files[0])
        safe_decrypt(reader, password)

        writer = PdfWriter()
        total_pages = len(reader.pages)

        for part in pages_input.split(","):
            part = part.strip()
            if "-" in part:
                start, end = map(int, part.split("-"))
                if start < 1 or end > total_pages:
                    raise ValueError("Page range out of bounds")
                for i in range(start - 1, end):
                    writer.add_page(reader.pages[i])
            else:
                page = int(part)
                if page < 1 or page > total_pages:
                    raise ValueError("Page number out of bounds")
                writer.add_page(reader.pages[page - 1])

        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        st.success("Pages extracted successfully!")
        download_button(buf, "extracted_pages.pdf")

    # =====| WATERMARK |=====
    elif operation == "Add Watermark" and uploaded_files:
        watermark_text = st.text_input("Watermark Text")
        if not watermark_text:
            st.warning("Please enter watermark text.")
        else:
            reader = PdfReader(uploaded_files[0])
            safe_decrypt(reader, password)

            wm_buf = io.BytesIO()
            c = canvas.Canvas(wm_buf, pagesize=A4)
            c.setFont("Helvetica", 40)
            c.setFillAlpha(0.2)
            c.drawCentredString(300, 400, watermark_text)
            c.save()
            wm_buf.seek(0)

            wm_page = PdfReader(wm_buf).pages[0]
            writer = PdfWriter()

            for page in reader.pages:
                page.merge_page(wm_page)
                writer.add_page(page)

            buf = io.BytesIO()
            writer.write(buf)
            buf.seek(0)
            st.success("Watermark added successfully!")
            download_button(buf, "watermarked.pdf")

    # =====| COMPRESS |=====
    elif operation == "Compress PDF" and uploaded_files:
        reader = PdfReader(uploaded_files[0])
        safe_decrypt(reader, password)

        writer = PdfWriter()
        writer.add_metadata(reader.metadata)

        for page in reader.pages:
            writer.add_page(page)

        # Lossless compression
        writer.compress_content_streams = True

        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)

        st.success("PDF compressed successfully (lossless).")
        download_button(buf, "compressed.pdf")

    else:
        st.info("Upload PDF file(s) to begin.")

except ValueError as ve:
    st.error(f"❌ {ve}")

except Exception as e:
    st.error("⚠️ An unexpected error occurred. Please check inputs or PDF file.")
