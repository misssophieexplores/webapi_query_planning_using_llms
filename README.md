# WebAPI Query Planning Using LLMs

Goal of this project is to test out different LLM's capabilities of query planning by successively increasing the complexity of tasks.  

![Schema of Web API Query Planning Using LLMs](images/web_api_query_planning.png)  

Complexity can be:
* Length: Number of steps that need to be executed
* Chaining: Output to be used as input in later steps
* Vagueness in prompts
* Reasoning: Comparing different outputs, also assessing contradictory or illogical results (e.g. interpretation of wrong results or unexpected API behaviour)
* Multi-lingual: Results can be in German or English, inputs need to be in English (translation needed when using previous outputs)


For this project, 45 prompts have been selected and run with GPT 3.5-Turbo and GPT 4. For the final analysis, 31 distinct prompts have been analysed. Results can be found here: https://wandb.ai/misssophie/LLM_multi_step_query/reports/WebAPI-Query-Planning-Using-LLMs--Vmlldzo3NTQyMDcx?accessToken=isvo4woevdpg3enta77w4n1videztgvxppm76so066joi2ewyd65rumol6ncctbt