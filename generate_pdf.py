"""Generate a PDF of the bouncing ball source code using Python's standard library."""
from pathlib import Path

source = Path(__file__).with_name("ball.py")
output = Path(__file__).with_name("bouncing-ball.pdf")


def escape(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


lines = source.read_text(encoding="utf-8").splitlines()
if len(lines) > 50 or any(len(line) > 95 for line in lines):
    raise SystemExit("Code is too long for this one-page PDF")

commands = ["BT /F1 16 Tf 48 750 Td (Bouncing Ball - Python Source Code) Tj ET"]
for index, line in enumerate(lines):
    commands.append(f"BT /F2 9 Tf 48 {715 - 13 * index} Td ({escape(line)}) Tj ET")
stream = ("\n".join(commands) + "\n").encode("latin-1", errors="replace")
objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>",
    b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"endstream",
]
pdf = bytearray(b"%PDF-1.4\n")
offsets = [0]
for number, obj in enumerate(objects, 1):
    offsets.append(len(pdf))
    pdf.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
xref = len(pdf)
pdf.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
for offset in offsets[1:]:
    pdf.extend(f"{offset:010d} 00000 n \n".encode())
pdf.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
output.write_bytes(pdf)
print(f"Created {output.name}")
