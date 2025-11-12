# Engineering Knowledge AI Agent Test

## 1. Describe differences between REST API, MCP in the context of AI.
Both are a protocol that allows two systems to communicate each other.
MCP is built on top of FastAPI, a library web framwork whih designed to build high perfromance API.
In REST API, there are a lot of methods (GET, POST, DELETE, etc) and input types (query params, body, form, etc), while in MCP use JSON RPC to transfer both input or output data.
MCP server acts as a bridge between MCP client with the original API resource.
This enables LLM applications to communicate with external tools (APIs, Prompts, Resources) with standardize protocol.
There are additional capability from MCP to sample LLM on the client without hosting in server-side.

The MCP client can connect to multiple MCP server and maintains their connectivity.
If there are some updates on the Server such as tool changes, MCP server can notify the client so they can adapt with new schema.

## 2. How REST API, MCP, can improve the AI use case.
AI knowledge, especially for LLM, is limited by thier own training dataset even though the model is trained on huge amount of data but still for a domain specific (knowledge like internal document owned by company) their knowledge is limited. This limitation make the LLM not so really helpful for variety of use cases.

To exceed their limitation, we can give the knowledge to LLM so they can understand the context.
This technique is called RAG (Retrieval Augmented Generation). Given a user query, LLM will find out relevant documents and give an answer from it. This is similar to human use google search just to answer the question.

Accessing to knowledge is not limited to text or file based format.
Modern LLM have capability to call some function/tools like API, Python Function or even web search by reading the schema definition, providing structured input and understanding the output as well.
This idea makes LLM so powerfull in solving complex problem.

## 3. How do you ensure that your AI agent answers correctly?
AI Agent is an advanced LLM implementation where we do not need to create a static or predefined workflow to solve the problem, meanwhile we let the LLM to interact with the enivornment more dynamic. 
This let LLM to do multiple attempts of reasoning and tool use just to answer the question.

Because this is not a predefined process, we should ensure that:
- AI Agent select correct tools by tracing each step of the reasoning process. An efficient agent will requires a small number of steps to solve the problem.
- For RAG application, the correctnes of response can also be determined by the performance of retriever system due to low quality of chunking strategy and the embedding model accuracy. 
- Retrieval Relevancy: measure how retrieved documents/knowledge is relevat with user question
- Answer Relevancy: measure how relevant the LLM response with user question in terms of topic.
- Groundedness: measure how accuract the response of LLM based on given data. Small Language Model sometimes failed to mention correct numbers.
- Guardrails: ensure that LLM should not answer question that is off-topic.

Some evaluation can be done by using LLM as a judge by leveraging higher model.
We can also use human response by providing a feedback button for each LLM response.

## 4. Describe what can you do with Docker / Containerize environment in the context of AI
Container helps us to package software program with their own dependencies so the program can run smoothly without worying about other library updates over the time by capturing the state of the code when we build the code.
This feature enable us to versionize the code for sepecific modification and can be 
Another benefit from container concept is to isolate the dependency with the original host machine and other application even though we use the same libary but with different version. It won't effect each other since each container run on their own environment.
Besides, the host and the application can run on different operating system but still utilizing CPU and RAM from the host.
One sample of container managers we can use is Docker. 
Unlike other software installer (.exe, .apk, etc) that requires an installation setup and some times take a few moment to be ready, by using docker image we do not need to manually setup the program because the instruction is executed when image is being created. A docker image can be started so fast because they have their own environment without the need of installation. This is useful for large scale AI application that requires scalability. 

## 5. How do you finetune the LLM model from raw ?
Finetuning LLM model usualy use existing pretrained model and teach it with new or domain specific knowledge so the model can perform better on that task. Finetuning model is needed because there is a possibility of LLM that is not understand so well in a specific terminology 