def render_tab2():
    import streamlit as st
    from dotenv import load_dotenv
    from os import environ as env
    from crewai import Crew, Agent, Task, Process, LLM
    from crewai_tools import ScrapeWebsiteTool, SerperDevTool
    from openai import OpenAI
    from langchain.chat_models import ChatOpenAI
    from config import llm

    # ===== Environment & API Setup =====
    load_dotenv()
    api_key = env["OPENAI_API_KEY"]
    serper_api_key = env["SERPER_API_KEY"]

    st.title("📊 Financial Market AI Crew")

    # ===== User Inputs First =====
    st.subheader("🧾 Trading Preferences")
    stock_selection = st.text_input("Stock Symbol (AAPL, NVDA, GOOGL, TSLA, MSFT, AMZN)", "")
    initial_capital = st.text_input("Initial Capital ($)", "100000")
    risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"], index=1)
    trading_strategy_preference = st.selectbox("Trading Strategy", ["Day Trading", "Swing Trading", "Scalping"])
    consider_news = st.checkbox("Consider News Impact", True)

    if stock_selection.strip() == "":
        st.warning("Please enter a stock symbol.")
        st.stop()

    # ===== OpenAI Setup =====
    client = OpenAI(api_key=api_key)

    # ===== CrewAI Tools =====
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()

    # ===== Agents =====
    data_analyst_agent = Agent(
        role="Data Analyst",
        goal="Analyze real-time market data to identify trends.",
        backstory="A market analyst using ML/statistical models.",
        tools=[search_tool, scrape_tool],
        allow_delegation=True,
        verbose=True,
    )

    trading_strategy_agent = Agent(
        role="Strategy Developer",
        goal="Develop trading strategies based on market insights.",
        backstory="Designs and tests strategies from market signals.",
        tools=[search_tool, scrape_tool],
        allow_delegation=True,
        verbose=True,
    )

    execution_agent = Agent(
        role="Trade Advisor",
        goal="Plan optimal trade execution.",
        backstory="Optimizes timing and logistics of trades.",
        tools=[search_tool, scrape_tool],
        allow_delegation=True,
        verbose=True,
    )

    risk_management_agent = Agent(
        role="Risk Advisor",
        goal="Assess risks of trading plans.",
        backstory="Evaluates risk exposure and mitigation.",
        tools=[search_tool, scrape_tool],
        allow_delegation=True,
        verbose=True,
    )

    # ===== Tasks =====
    data_analysis_task = Task(
        description=f"Analyze market data for {stock_selection}.",
        expected_output="Market insights and trends.",
        agent=data_analyst_agent,
    )
    strategy_development_task = Task(
        description=f"Create strategies for {stock_selection} considering {risk_tolerance} tolerance and {trading_strategy_preference}.",
        expected_output="List of trading strategies.",
        agent=trading_strategy_agent,
    )
    execution_planning_task = Task(
        description=f"Plan trade execution for {stock_selection} based on strategies and market conditions.",
        expected_output="Execution timing and pricing plan.",
        agent=execution_agent,
    )
    risk_assessment_task = Task(
        description=f"Assess risks for trading {stock_selection}.",
        expected_output="Risk analysis and mitigation strategies.",
        agent=risk_management_agent,
    )

    # ===== Create the Crew =====
    financial_trading_crew = Crew(
        agents=[
            data_analyst_agent,
            trading_strategy_agent,
            execution_agent,
            risk_management_agent,
        ],
        tasks=[
            data_analysis_task,
            strategy_development_task,
            execution_planning_task,
            risk_assessment_task,
        ],
        verbose=True,
        process=Process.hierarchical,
        manager_llm=llm,
    )

    # ===== Run the Crew =====
    with st.spinner("Thinking..."):
        financial_trading_inputs = {
            "stock_selection": stock_selection,
            "initial_capital": initial_capital,
            "risk_tolerance": risk_tolerance,
            "trading_strategy_preference": trading_strategy_preference,
            "news_impact_consideration": consider_news,
        }

        def generate_sample_questions(context, num_questions=5):
            prompt = f"""
            Based on the user's trading preferences, generate {num_questions} useful questions they might ask:

            ---
            {context}
            ---
            Format as a numbered list.
            """
            response = client.chat.completions.create(
                model="gpt-4o-mini", # gpt-4o-mini, gpt-4
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            reply = response.choices[0].message.content
            return [line.strip("0123456789. ") for line in reply.split("\n") if line.strip()]

        result_financial_trading = financial_trading_crew.kickoff(inputs=financial_trading_inputs)
        st.subheader("📈 Trading Result:")
        st.markdown(result_financial_trading)

    # ===== Chat UI =====
    st.divider()
    st.subheader("💬 Ask a question about real-time market data")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def display_chat_history():
        for role, message in st.session_state.chat_history:
            label = "**User:**" if role == "User" else "**AI:**"
            st.markdown(f"{label} {message}")

    # ===== Suggested Questions =====
    sample_input_summary = f"Stock: {stock_selection}, Strategy: {trading_strategy_preference}, Risk: {risk_tolerance}"
    suggested = generate_sample_questions(sample_input_summary)
    st.markdown("💡 Suggested Questions:")
    for q in suggested:
        st.markdown(f"- {q}")

    display_chat_history()
    user_query = st.text_input("Enter your question", key="financial_analysis")

    if st.button("Send") and user_query.strip():
        with st.spinner("Thinking..."):
            full_inputs = financial_trading_inputs.copy()
            full_inputs["question"] = user_query

            result = financial_trading_crew.kickoff(inputs=full_inputs)

            st.session_state.chat_history.append(("User", user_query))
            st.session_state.chat_history.append(("AI", result))

            st.success("Response received!")
            feedback = st.radio("Was the answer helpful?", ["Yes", "No"], horizontal=True)
            if feedback:
                st.write(f"Thanks for your feedback: {feedback}")
