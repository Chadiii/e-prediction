from chatterbot import ChatBot

# Creating ChatBot Instance
chatbot = ChatBot(
    'CoronaBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3',
    read_only=True
) 




def trainBot():
    print("train bot")
    from chatterbot.trainers import ListTrainer
    from chatterbot.trainers import ChatterBotCorpusTrainer
    # Training with Personal Ques & Ans 
    training_data_quesans = open('training_data/ques_ans.txt').read().splitlines()
    training_data_personal = open('training_data/personal_ques.txt').read().splitlines()

    training_data = training_data_quesans + training_data_personal

    trainer = ListTrainer(chatbot)
    trainer.train(training_data)


    # Training with English Corpus Data 
    trainer_corpus = ChatterBotCorpusTrainer(chatbot)
    trainer_corpus.train(
        'chatterbot.corpus.english'
    ) 




try:
    resp = str(chatbot.get_response("bye"))
    print(resp)
    if (resp != "bye"):
        raise Exception()
    print("dont train bot")
except Exception as e:
    trainBot()