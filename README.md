# Davita Example Medical Labels Dataset

A synthetic pharmacy prescription bottle label image dataset containing **400 unique images** (**200 flat sticker labels** and **200 3D cylindrically curved pill bottle labels**) along with full ground-truth JSON metadata and OCR bounding boxes.

> **Privacy Note:** All 400 records are 100% synthetically generated. No real patient Protected Health Information (PHI) or Personally Identifiable Information (PII) is present. Every single image has a guaranteed-unique Patient Name, Rx Number, Date of Birth, Street Address, and Pharmacy Phone Number.

## Repository Structure

```text
├── flat/                              # 200 flat pharmacy sticker images (flat_label_001.png - flat_label_200.png)
├── curved/                            # 200 3D curved pill bottle images (curved_bottle_001.png - curved_bottle_200.png)
├── annotations/
│   └── dataset_annotations.json       # Complete ground-truth metadata & text bounding boxes for all 400 images
└── generate_dataset_400.py            # Python script used to synthesize the dataset
```

## Dataset Highlights

- **5 Distinct Sticker Shapes, Sizes & Layout Forms:**
  1. Wide Standard Pharmacy Label (`960×620`) with right-side perforated auxiliary warnings & barcode
  2. Square Thermal Label (`780×720`) with top barcode banner & bottom horizontal auxiliary stickers
  3. Tall Vertical Vial Sticker (`680×860`) with stacked bottom-right warning labels
  4. Split Clinical Layout (`1000×560`) with left auxiliary/barcode column & right prescription block
  5. Compact Outpatient Thermal Sticker (`840×520`)
- **6 Distinct 3D Container Shapes, Sizes & Colors:**
  - Standard Amber Vial, Tall Slim Amber Vial, Wide-Mouth Short Pill Jar, Opaque White HDPE Bottle, Translucent Emerald Green Vial, and Cobalt Blue / Dark Amber Specialty Vial.
- **12 Pharmacy Brand Styles & 50+ Real FDA Medication Profiles** (Drug name, strength, dosage form, generic equivalent, manufacturer, NDC code, and pill imprint description).
