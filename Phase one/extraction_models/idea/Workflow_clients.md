# **The Workflow**

This workflow incorporates two models per client, `init` and the actual model, to ensure proper control and resource efficiency.

---

## **Model Initialization**

- Each client has two models:
  - **`init` Model**: Acts as a gatekeeper to ensure that the client’s functionality is required before processing begins.  
  - **Actual Model**: Executes the primary processing task.  

- **How It Works**:
  - The `init` model detects whether the client should activate. It returns a `True` value if functionality is required.
  - Only when `True` is received from the `init` model, the user's prompt is passed to the actual model for processing.
  - Both models use Gemini Pro by default. However, the `init` model can be optimized further by using a custom RAG (Retrieval-Augmented Generation) model for reduced resource consumption.

---

## **Client Functionality**

- [x] Models receive the user's prompt at approximately the same time.  
- [x] Models can extract relevant features from the prompt.  
- [x] Prompts are defined in the [`address.py`](../Ex_address.py) file, enabling easy replication of clients by copying and pasting code.  
- [x] Models consider historical data for decision-making.  
- [x] Models send feedback to the sequencer, including the model's name.  
- [x] Communication with the GPT breakout system is established.  

---

## **Output and Communication**

1. **JSON Output**:  
   Models return a JSON file containing the relevant extracted values.  

2. **Summary**:  
   - The models generate a summary of their operations and send it to the sequencer for database logging (history implementation).  
   - The JSON file and summary are also sent to the GPT breakout system for further processing and action-taking.

---

> [!NOTE]
> The main features of the models are detailed in the [Prompt File](../Ex_address.py).