# 【Mimosa】A Body-Space Correlation Model:
## Computing Micro Postures for Interactive Façade Design in Workspace
## Overview
Mimosa is an MR-based immersive workspace interaction system that bridges human micro-postures with interactive façade control. Guided by Human-Centred Design (HCD), it creates dedicated, adaptive office zones in public spaces (e.g., parks, cafes) via virtual dynamic facades—no physical construction required. The core is a body-space correlation model that maps micro-postures → working states (focus/fatigue) → facade openness, enabling real-time, human-responsive spatial adjustments.
## Core Objective
Establish a bidirectional mapping mechanism between human micro-postures and facade control parameters. Validate the model through MR experiments to optimize workspace comfort and efficiency, redefining the relationship between urban public spaces, technology, and workstyles.
## Repository Structure
This repo contains key code, scripts, and design files supporting the Mimosa system:
1. Stroop Test Programs
   - `stroop_test_Chinese`: Chinese-version Stroop test app for measuring user attention/focus.
   - `stroop_test_English`: English-version Stroop test app for cross-linguistic experimental flexibility.
   - Purpose: Collect ground-truth data of working states (focus/fatigue) to train the correlation model.

2. Data Fitting Scripts
   - `拟合_F-face_final`: Final fitting script for the relationship between facial features and working states.
   - `拟合_F-face二次函数_notgood`
   - `拟合_Focus-Openness`: Fitting script for mapping focus levels to facade openness.
   - `拟合_score-openness`: Fitting script for linking Stroop test scores to facade openness.
   - `计算绝对开敞度`: Script to calculate absolute facade openness values.
   - Purpose: Derive quantitative formulas for the two core mappings (micro-postures → working states; working states → openness).

3. Posture & Skeleton Extraction
   - `面部姿态提取`: Code for extracting facial micro-posture features (supporting working state recognition).
   - Purpose: Capture fine-grained human postural data as the input of the correlation model.
4. Parametric Modeling (Grasshopper)
   - `0609体块生成`: Grasshopper definition for basic facade module generation.
   - `Test-现场测试所用`: Grasshopper definition for on-site MR experiment validation.
   - `体块生成（中心旋转版）0609`: Grasshopper definition for facade module generation with center-rotation functionality.
   - `虚拟办公仓`: Grasshopper definition for virtual office cabin modeling.
   - Purpose: Parametric design of the virtual dynamic facade (composed of independent rotating micro-panels).
## Dependencies
- For Stroop test apps: Python 3.x (or relevant runtime based on development framework).
- For data fitting: Python (numpy, scipy, pandas).
- For parametric modeling: Rhino 7+/Grasshopper.
- For MR experiments: Compatible MR headset (e.g., HoloLens) and corresponding development toolkit.
## Usage
- Use Stroop test programs to collect user focus/fatigue data (ground truth).
- Run posture extraction code to capture micro-postural features from experimental participants.
- Apply data fitting scripts to derive mapping formulas between micro-postures, working states, and facade openness.
- Use Grasshopper definitions to generate parametric facade models.
- Validate the integrated system via MR experiments (refer to Test-现场测试所用 for on-site setup).
