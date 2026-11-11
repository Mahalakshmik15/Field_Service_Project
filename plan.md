# Plan: AI-Powered Field Service Report Summarizer

## Architecture & Technology Stack
- **Language:** Python 3
- **AI / LLM Integration:** Context engineering approach utilizing structured system prompts to enforce Northgate FM’s delivery guidelines and security constraints.
- **Data Source:** `Data/service_reports.jsonl` (unvalidated JSON lines).

## Implementation Strategy
1. **Data Ingestion Module:** Parse line-by-line JSON objects safely with robust error handling.
2. **Context Engineering Pipeline:** Design a strict system prompt that maps raw report fields into the required customer-portal schema while applying security filtering.
3. **Validation & Export:** Automatically evaluate outputs and export structured summaries to `outputs/summaries.txt`.