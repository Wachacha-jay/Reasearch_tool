from flask import Flask, render_template, request
import os
from langchain_core.messages import HumanMessage
from core.workflow import compile_research_team

app = Flask(__name__)

# Load Google API key from environment variable or .env
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    error = None
    topic = ''
    if request.method == 'POST':
        topic = request.form.get('topic', '').strip()
        if not topic:
            error = 'Please enter a research topic.'
        else:
            try:
                app_graph = compile_research_team()
                initial_state = {
                    'messages': [HumanMessage(content=f'Research the topic: {topic}')],
                    'research_topic': topic,
                    'next': 'researcher',
                    'current_agent': 'start',
                    'findings': {},
                    'final_report': ''
                }
                config = {'configurable': {'thread_id': 'web_session'}}
                final_state = None
                for step, state in enumerate(app_graph.stream(initial_state, config=config)):
                    current_state = list(state.values())[0]
                    final_state = current_state
                    if step > 10:
                        break
                if final_state and final_state['final_report']:
                    report = final_state['final_report']
                else:
                    error = 'No report generated.'
            except Exception as e:
                error = f'Error: {str(e)}'
    return render_template('index.html', report=report, error=error, topic=topic)

if __name__ == '__main__':
    app.run(debug=True) 