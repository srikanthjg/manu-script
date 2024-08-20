# from langchain_community.tools import ShellTool
# from langchain.agents import AgentType, initialize_agent
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnableLambda, RunnablePassthrough
# from bedrock import *
# import re    


# def get_contextual_answer(query):
#     template = """Answer the question based only on the following context:
#     {context}

#     Question: {question}
#     """
#     prompt = ChatPromptTemplate.from_template(template)

#     model = get_llm(bedrock_client,LLM_ANTHROPIC_MODEL)
#     retriever = get_from_knowledge_base_retriever()
#     chain = (
#         {"context": retriever, "question": RunnablePassthrough()}
#         | prompt
#         | model
#         | StrOutputParser()
#     )

#     return chain.invoke()