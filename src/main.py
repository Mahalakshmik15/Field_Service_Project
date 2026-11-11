import os
import json
# import openai  # Uncomment when you have your API key set up

def load_data():
    reports = []
    data_path = os.path.join(os.path.dirname(__file__), "Data", "service_reports.jsonl")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    reports.append(json.loads(line.strip()))
    return reports

def generate_ai_summary(report):
    """
    Context engineering approach: Passes the raw report through a strict 
    system prompt enforcing customer-portal visibility and security redaction.
    """
    system_prompt = """
    You are an expert AI Service Delivery Assistant for Northgate FM. 
    Your task is to convert internal engineering field reports into clean, 
    customer-facing portal summaries.
    
    STRICT RULES:
    1. The reader is a client facilities contact (plain language, no technical jargon).
    2. NEVER include internal identifiers, technician names, technician IDs, personal phone numbers, or home/personal addresses.
    3. SECURITY CRITICAL: NEVER include site access information such as key locations, door codes, or alarm codes. 
    4. If a report is internally inconsistent, contradictory, or lacks enough information, explicitly state that the report is incomplete and under review rather than guessing.
    
    Required Output Format:
    - Asset & Date: [Asset Name] on [YYYY-MM-DD]
    - What Was Found: [Summary of findings]
    - What Was Done: [Summary of resolution]
    - Parts Fitted: [List parts or 'None']
    - Recommendations / Outstanding: [Details or 'None noted']
    - Time on Site: [Hours]
    """

    user_prompt = f"""
    Please summarize the following field service report:
    {json.dumps(report, indent=2)}
    """

    # --- AI Integration Placeholder ---
    # In your actual implementation, call your LLM client here:
    # client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # response = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_prompt}
    #     ],
    #     temperature=0.0
    # )
    # summary_text = response.choices[0].message.content
    
    # Mock AI response format for local demonstration:
    summary_text = f"""
========================================
AI-GENERATED SUMMARY: {report.get('report_id')}
========================================
- Asset & Date: {report.get('asset')} on {report.get('arrived_at', '').split('T')[0]}
- What Was Found: {report.get('technician_notes')}
- What Was Done: {report.get('resolution')}
- Parts Fitted: {', '.join(report.get('parts_used', [])) if report.get('parts_used') else 'None'}
- Recommendations / Outstanding: None noted
- Time on Site: {report.get('stated_duration_hours')} hours
----------------------------------------
"""
    return summary_text

def main():
    print("--- Starting AI-Powered Field Service Report Summarizer ---")
    reports = load_data()
    print(f"Loaded {len(reports)} reports. Processing through AI context pipeline...")
    
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "outputs"), exist_ok=True)
    output_path = os.path.join(os.path.dirname(__file__), "..", "outputs", "summaries.txt")
    
    all_summaries = []
    for report in reports:
        summary = generate_ai_summary(report)
        all_summaries.append(summary)
        print(summary)
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_summaries))
    
    print(f"\nSuccessfully generated and saved all AI summaries to {output_path}")

if __name__ == "__main__":
    main()