from technical_assistant_agent.llm.base import LLM
from technical_assistant_agent.tools.registry import ToolRegistry
from technical_assistant_agent.tools.tool_executor import ToolExecutor

#from technical_assistant_agent.models.agent_response import AgentResponse
from technical_assistant_agent.models.agent_state import AgentState
from technical_assistant_agent.models.agent_context import AgentContext
from technical_assistant_agent.agent.agent_policy import AgentPolicy
from technical_assistant_agent.models.chat_message import ChatMessage
from technical_assistant_agent.models.agent_stop_reason import AgentStopReason
from technical_assistant_agent.models.agent_response import AgentResponse

import asyncio

class Agent:
    def __init__(
        self,
        llm: LLM,
        tools: ToolRegistry,
        tool_executor: ToolExecutor,
        agent_policy: AgentPolicy      
    ) -> None:
        
        self.llm = llm
        self.tools = tools
        self.tools_executor = tool_executor
        self.agent_policy = agent_policy

    async def run(
        self,
        #prompt: str,
        agent_state: AgentState,
        agent_context: AgentContext   # w przyszlosci do przekazania informacji o maszynie
    ) -> AgentState: #AgentResponse:

        # dodajemy ostatnia wiadomosc do historii konwersacji
        agent_state.chat_history.add(
            ChatMessage(
                role = 'user',
                content = agent_state.user_message
            )
        )

        return await self._agent_loop(
            agent_state = agent_state,
            agent_context = agent_context
        )

    async def _agent_loop(
        self,
        agent_state: AgentState,
        agent_context: AgentContext
    ) -> AgentResponse: #AgentState: 

        #################################################
        ################## PETLA AGENTA #################
        #################################################

        while not agent_state.finished:
            
            ##############################################
            ############## SRPRAWDZAMY LIMITY#############
            ##############################################

            stop_reason = self.agent_policy.run_check(
                agent_state = agent_state
            )

            if stop_reason is not None:
                agent_state.finished = True
                agent_state.stop_reason = stop_reason
                break

            agent_state.iteration += 1

            ##############################################
            ########## POBIERAMY LISTE NARZEDZI ##########
            ##############################################

            available_tools = self.tools.list_tools()

            ##############################################
            ############# WYWOLANIE MODELU ###############
            ##############################################

            response = await self.llm.chat(
                chat_history = agent_state.chat_history,
                tools = available_tools
            )

            # print("\n==============================")
            # print(f"ITERATION: {agent_state.iteration}")
            # print("LLM CONTENT:")
            # print(repr(response.message.content))
            # print("LLM TOOL CALLS:")
            # print(response.message.tool_calls)
            # print("==============================\n")

            assistant_response = response.message

            #############################################
            ###### DODANIE ODPOWIEDZI DO HISTORII #######
            #############################################

            agent_state.chat_history.add(
                assistant_response
            )

            #############################################
            ### NIE WYWOLANO NARZEDZI = MAMY ODPOWIEDZ ##
            #############################################

            if not assistant_response.tool_calls:
                agent_state.finished = True
                agent_state.final_answer = (
                    assistant_response.content or ''
                )
                agent_state.stop_reason = AgentStopReason.COMPLETED
                break

            #############################################
            ### SPRAWDZAMY LICZBE WYWOLANYCH NARZEDZI ###
            #############################################

            if (agent_state.tool_calls + len(assistant_response.tool_calls) > self.agent_policy.max_tool_calls):
                agent_state.finished = True
                agent_state.stop_reason = AgentStopReason.MAX_TOOL_CALLS

                # czy tutaj nie powinnismy wywolac LLMa jeszcze raz, ale tym razem bez tooli
                # zeby miec pewnosc ze dostaniemy pisana odpowiedz?
                # bo co w przypadku kiedy agent bedzie chcial raz po raz wywolywac narzedzia?
                
                break

            ############################################
            ############## ODPALENIE TOOLI #############
            ############################################

            #if response.message.tool_calls:
            tool_results = await asyncio.gather(            # bo model moze chciec rownolegle wykonac kilka tooli
                *[
                    self.tools_executor.execute(tool_call, agent_context)
                    for tool_call in assistant_response.tool_calls
                ]
            )

            # print("\n============ ODPOWIEDZ AGENTA ===========")
            # print(assistant_response)

            # print("\n========== TOOL RESULTS ==========")

            # for result in tool_results:
            #     print("name:", result.name)
            #     print("content:", repr(result.content))
            #     print("structured:", result.structured_content)
            #     print("error:", result.is_error)

            # print("==================================\n")

            ############################################
            ########## ZAPISANIE WYNIKOW TOOLI #########
            ############################################

            for tool_call, tool_result in zip(
                assistant_response.tool_calls,
                tool_results
            ):
                tool_call.result = tool_result

            agent_state.tool_calls += len(tool_results)

            ###########################################
            ############## KONIEC PETLI ###############
            ###########################################
            #print("\n\nkoniec przebiegu petli. historia czatu:")
            #print(agent_state.chat_history)

            # print("\n========== HISTORY ==========")
            # print(agent_state.chat_history.model_dump())
            # print("=============================\n")

        # return AgentResponse(
        #     answer = agent_state.final_answer or "",
        #     iterations = agent_state.iteration,
        #     stop_reason = agent_state.stop_reason
        # )

        agent_response = self._format_response(
            agent_state = agent_state
        )
        return agent_response

    def _format_response(
        self,
        agent_state: AgentState
    ) -> AgentResponse:

        agent_response = AgentResponse(
            chat_history = agent_state.chat_history.public(),
            iteration = agent_state.iteration,
            tool_calls = agent_state.tool_calls,
            finished = agent_state.finished,
            final_answer = agent_state.final_answer,
            stop_reason = agent_state.stop_reason,
        )

        return agent_response