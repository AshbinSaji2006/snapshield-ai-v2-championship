# Third-party notices

Direct project dependencies are pinned in `requirements.txt` and `frontend/package-lock.json`. Transitive packages retain their upstream notices.

| Dependency | Version | License |
|---|---:|---|
| FastAPI | 0.141.1 | MIT |
| Starlette | 1.6.0 | BSD-3-Clause |
| Uvicorn | 0.35.0 | BSD-3-Clause |
| Pydantic | 2.11.7 | MIT |
| python-multipart | 0.0.32 | Apache-2.0 |
| Pillow | 12.3.0 | HPND |
| scikit-learn | 1.7.1 | BSD-3-Clause |
| NumPy | 2.2.6 | BSD-3-Clause |
| joblib | 1.5.3 | BSD-3-Clause |
| ONNX | 1.22.0 | Apache-2.0 |
| ONNX Runtime | 1.30.0 | MIT |
| Hugging Face Tokenizers | 0.23.1 | Apache-2.0 |
| RapidOCR ONNX Runtime | 1.4.4 | Apache-2.0 |
| OpenCV Python | 5.0.0.93 | Apache-2.0; bundled codecs/components may have separate terms |
| qrcode | 8.2 | BSD-3-Clause |
| Matplotlib | 3.10.8 | PSF-based license |
| httpx2 | 2.12.0 | BSD-3-Clause |
| pytest | 9.1.1 | MIT |
| pytest-asyncio | 1.4.0 | Apache-2.0 |
| psutil | 7.0.0 | BSD-3-Clause |
| PyInstaller | 6.16.0 | GPL-2.0-or-later with bootloader exception |
| React / React DOM | 19.3.0 | MIT |
| lucide-react | 1.45.0 | ISC |
| Vite | 8.3.0 | MIT |
| TypeScript | 7.0.2 | Apache-2.0 |
| oxlint | 1.82.0 | MIT |
| `@vitejs/plugin-react` | 6.1.1 | MIT |

Datasets: UCI SMS Spam Collection, DOI 10.24432/C5CC84, and the 2022 Mendeley SMS Spam Dataset, DOI 10.17632/f45bkkt8pr.1, are used under CC BY 4.0. See `DATASETS.md` and `docs/v2/DATA_PROTOCOL.md`.

Deep Guard derives from `google/bert_uncased_L-2_H-128_A-2` revision `30b0a37ccaaa32f332884b96992754e246e48c5f`, Apache-2.0. The vendored Public Suffix List snapshot is from <https://publicsuffix.org/list/public_suffix_list.dat>, licensed MPL-2.0; its source hash and acquisition metadata are in `backend/resources/public_suffix_list.provenance.json`.

RapidOCR includes local model data collected into the packaged release. Review its upstream model/license notices before commercial redistribution. Snapdragon is a trademark of Qualcomm Incorporated; project use does not imply endorsement.
