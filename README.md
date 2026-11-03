# Document Recognition

Recognition of identity documents on fully synthetic data: a generator draws fictional ID
cards and labels every field automatically, a YOLO detector finds the fields on photo-like
images, and OCR reads them. No real documents or personal data are used.

[Русская версия](README.ru.md)

> Work in progress.

## Pipeline

1. **Synthetic documents.** Fictional ID card templates filled with random names, dates and
   numbers. Field boxes come straight from the renderer, so labels are exact and free.
2. **Phone photo augmentation.** Perspective, rotation, blur, glare, noise and JPEG artifacts.
3. **Field detection.** YOLO trained on some templates and tested on a template it has never seen.
4. **OCR.** Detected fields are read with EasyOCR, quality is measured with the character error rate (CER).

## Why synthetic data

Passports and ID cards contain personal data, and a face photo is biometric data. Training on
real documents requires a legal basis and protected storage, so research projects use
generated documents instead (see the MIDV-2020 dataset).

## Repository layout

```
.
├── src/            # generator, training and evaluation code
├── tests/          # pytest tests
├── docs/           # report images
├── requirements.txt
└── LICENSE
```

## Setup

```bash
pip install -r requirements.txt
```

## License

[MIT](LICENSE)
