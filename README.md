# GAPE: Graph-Augmented Policy Enforcement for Agentic AI

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![ArXiv](https://img.shields.io/badge/arXiv-2512.xxxxx-b31b1b.svg)](https://arxiv.org)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-TSLAM--4B-yellow)](https://huggingface.co/NetoAISolutions/TSLAM-4B)

Reference implementation for the paper **"Graph-Augmented Policy Enforcement (GAPE) for Safe Agentic AI in 5G Autonomous Networks"**.
This repository contains the reference implementation of the GAPE core logic and a representative subset of the 88 SHACL policies described in the paper (covering all 4 constraint classes). Vendor-specific proprietary rules are excluded.

## 🏗 Architecture
GAPE is a neuro-symbolic framework that sandwiches a probabilistic agent (TSLAM-4B) between a deterministic Network Knowledge Graph (NKG) and SHACL-based policy validation.

## 🚀 Reproducibility Guide
To reproduce the results in **Table 1 (Safety Performance)**:

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt


