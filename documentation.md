# FinServe

## Business problems and automation proposals


FinServe’s current manual workflows have bottlenecks with over half of the staff doing some sort of manual work, which consumes time and is prone to errors. These inefficiencies are limiting the company’s ability to scale and provide a seamless experience for clients. 

Fixing all at once isn't possible. Some of the company current systems might be legacy and may not integrate well with modern automation tools. Moreover, the higher the autonomy, the more control over the tool is needed. It’s crucial to ensure that any AI solution is implemented with proper human oversight and safety measures in place.

Therefore I recommend phased approach, starting with those areas that are easier to automate while still having big impact on efficiency and client satisfaction.


### I. Lead Qualification
* **Current State:** The 15-person sales team manually enter web leads into the CRM.
* **Proposed Solution:** Design and implement an AI-powered lead qualification system. When a lead enters the CRM, the system would look at their company website, parse their email inquiry, and extract key entities such as industry, estimated company size and contact intention. It would then auto-generate a concise memo. This would allow the sales team to prioritize high-quality leads and focus their efforts on closing deals rather than data entry.

### II. Client Support & Compliance
* **Current State:** FinServe's 10-person support team currently handles all client emails, calls and portal tickets individually without a centralized knowledge base or standardized templates. 

* **Proposed Solution:** Implement AI Support Co-Pilot powered by Retrieval-Augmented Generation. By ingesting FinServe's policy documents the AI has access to a single source of truth. When a new ticket arrives, the AI analyzes the query and drafts response based on internal knowledge base. Human agents then review the drafted response, verify its source citations, and send it to the client. 

### III. Preparing periodic reports
* **Current State:** Finance and risk teams manually extract data from the CRM and core banking systems into Excel spreadsheets for monthly, quarterly, and regulatory reporting. 

* **Proposed Solution:** Establish an ETL data pipeline to automatically ingest and unify data from both the CRM and core banking systems. Deploy specialized AI reporting agents capable of querying the database with designed SQL queries and preparing unified reports.


## Implementing one solution

### The motivation

Out of the three challenges, I decided to build the AI Support Co-Pilot (Solution II), and here’s why:

**High Impact**

- Manually reading emails and typing out repetitive replies is monotonous task, which is perfect for automation. 

**Guidelines and Policies**

- In finance, there are strict guidelines and policies that must be followed. Using AI to draft responses based on a centralized knowledge base ensures that all communications are compliant and consistent. 
- After that, human agents can quickly review the draft, verify the sources, and send it out, saving time without sacrificing control.


**Policies Change**
- Business rules and policies in finance can change frequently. By using a RAG approach, the AI can always access the most up-to-date information without needing to be retrained. 




## Implementation Walkthrough: AI Support Co-Pilot

### The architecture 

For a working prototype of the AI Support Co-Pilot, I decided to use Python for the frontend dashboard and n8n for the backend orchestration.

Using Python's Streamlit I quickly created interactive dashboard where the staff can view tickets and edit the drafted responses. Meanwhile, n8n allowed me to easily connect different services (like Google Sheets for the knowledge base and Gemini for the LLM) and manage the flow of data between them with a visual interface. 

This modular design makes it easier to maintain and scale the system as needed, allowing for future enhancements or integrations without significant disruption and staff retraining.


### Workflow in action

Here is how the system processes a customer inquiry:

1. Ticket Selection: The support agent logs into the Streamlit dashboard and selects an open ticket. The app sends the ticket details via a secure Webhook to the n8n backend.

2. Knowledge Retrieval: n8n catches the webhook and queries the knowledge base (Google Sheets) to find the current, approved company policy relevant to the customer's issue.

3. AI Processing: The LLM analyzes the ticket against the retrieved policy to determine the category, assess customer sentiment, and draft response. If no policy matches, the AI triggers a safety flag rather than hallucinating an answer. 

4. Human Validation: The AI's structured output is sent back to the Streamlit UI. The agent reviews the RAG source and edits the draft if necessary. 


## Future Enhancements (If Given More Time)

If given additional time to work on this Proof of Concept I would focus on the following improvements:

- **Vector Database Integration**
Currently, the system uses Google Sheets to simulate knowledge retrieval. In a real-world scenario, company policies might reside in hundreds of files. That's why I would switch to a dedicated Vector Database. This would allow the AI Agent to perform advanced semantic searches across massive datasets.

- **Connecting to mail and ticketing systems**
Right now the app saves the AI-generated response to a local text file. If given more time I could build another n8n pipeline to automatically send the reponse to the client or to the manager in case of escalation. The AI Co-Pilot could also be extended to automatically update the ticket status in the CRM after the response is sent.

To move the prototype closer to a production-ready solution these are the key areas I would focus on:

- **Native CRM & Ticketing System Integration**
This prototype uses mock data and local text files for simplicity, but in a production environment the AI Support Co-Pilot would need to integrate directly with FinServe’s existing CRM and ticketing systems.

- **Data Privacy & PII Masking**
In the financial sector, sending unmasked customer data to external LLMs (in my case Gemini API) is a severe compliance risk. To address this, the LLM inference should be moved to a private cloud or on-premises servers. 

