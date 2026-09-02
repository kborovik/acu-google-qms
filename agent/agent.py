from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-flash-latest",
    name="coa_agent",
    description="Certificate of Analysis ingestion for Acumatica QMS lot-release.",
    instruction=(
        "You assist with Certificate of Analysis (CoA) ingestion and "
        "Acumatica QMS lot-release workflows."
    ),
)
