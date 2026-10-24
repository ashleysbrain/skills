# Algorithm Integrity Audit Procedure — 2026-06-14

This document outlines the steps to independently verify key components of the proprietary TWC scoring system.

## 1. Nutrition Label Verification
- Query the `nutrition_daily` table for recent entries.
- For each entry, compute the expected label using the `nutrition_label` function from `8d360-nutrition-engine.py`.
- Compare the stored label with the expected label.
- Any mismatch indicates a storage or computation error.

## 2. Interaction Matrix Verification
- Extract key coupling values from the `interaction_matrix` table:
  ```sql
  SELECT dim1, dim2, value 
  FROM interaction_matrix 
  WHERE (dim1='PSY' AND dim2='INT') OR (dim1='INT' AND dim2='PSY')
     OR (dim1='PHY' AND dim2='VOC') OR (dim1='VOC' AND dim2='PHY')
     OR (dim1='SOC' AND dim2='SPI') OR (dim1='SPI' AND dim2='SOC')
     OR (dim1='ENV' AND dim2='PHY') OR (dim1='PHY' AND dim2='ENV');
  ```
- Compare each value to the proprietary specification:
  - PSY↔INT/INT↔PSY: Expected 0.85
  - PHY↔VOC/VOC↔PHY: Expected 0.78
  - SOC↔SPI/SPI↔SOC: Expected 0.72
  - ENV↔PHY/PHY↔ENV: Expected 0.68
- If any value deviates by more than 0.10 from the expected value, flag as an implementation gap.

## 3. Pipeline Coverage Verification
- Query the `daily_scorecard` table for the last 31 days.
- Count rows where `twc_score IS NOT NULL AND source NOT IN ('cron','carryforward')` → real scored days.
- Count total distinct dates in the same period.
- Calculate coverage = (real scored days / total days) × 100%.
- If coverage < 50%, investigate the scoring pipeline.

## 4. Label Storage Verification (for rescores)
- After writing rescore results to the database, verify that labels in `nutrition_daily`, `sexual_health_daily`, and `daily_scorecard` match the output of the respective label functions for the stored composites.