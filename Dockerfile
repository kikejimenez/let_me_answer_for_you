FROM ejimenezr/jupy-dark

COPY ./requirements.txt requirements.txt

#code formatter
RUN pip install -r requirements.txt
RUN python -c "from let_me_answer_for_you.settings import run_shell_installs,load_qa_models;\
    run_shell_installs();\
    load_qa_models();\
    "

