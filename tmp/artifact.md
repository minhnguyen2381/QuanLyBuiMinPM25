# Template distillation contract

## Reference

- Reference DOCX: `C:/Users/hasbr/Downloads/PPNCKH_LeHoan.docx`
- SHA-256: `4c602f6771c4d529852e0552299e3a7263724b146a5def4fee6b6001f8dc7862`
- Inspected with `python-docx`, `section_audit.py`, and `style_lint.py`.
- Render with packaged LibreOffice renderer could not run because `soffice` was not available in the environment.

## Page system

- A4 portrait.
- Margins copied from the reference pattern and normalized for the new report: left 3.0 cm; right/top/bottom 2.0 cm.
- Reference uses 3 sections, portrait, first page with distinct first-page header behavior.
- New report keeps A4 portrait and simple footer page number field.

## Typography and hierarchy

- Main font: Times New Roman.
- Body text: 13 pt, justified, first-line indent about 1.0 cm, 1.25 line spacing.
- Chapter headings: centered, uppercase, bold.
- Section headings: left aligned, bold.
- Captions: centered, italic, Times New Roman 12 pt.

## Components

- Cover page follows the reference pattern: ministry/university block, report title, topic title, metadata table, Hanoi/year line.
- Front matter follows the reference pattern: danh mục hình ảnh, danh mục bảng biểu, mục lục.
- Body follows numbered chapter structure.
- Tables use Word `Table Grid`.
- Figures are centered with Vietnamese captions.

## Content flow

- Chapter 1: introduction, objectives, research questions, scope.
- Chapter 2: theoretical background and data-analysis methodology.
- Chapter 3: data and exploratory analysis.
- Chapter 4: ARIMA/Random Forest modeling and evaluation.
- Chapter 5: discussion, implications, limitations, conclusion.
- References at the end.

## Fidelity notes

- The report is a new document derived from the reference style system, not an in-place replacement of the original topic.
- Original reference DOCX remains unchanged.
- Exact page-by-page visual fidelity could not be verified with LibreOffice due missing `soffice`; structural inspection and DOCX generation checks are required.
