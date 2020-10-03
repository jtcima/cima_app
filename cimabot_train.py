from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

cimabot=ChatBot('cima',
                #storage_adapter='chatterbot.storage.SQLStorageAdapter',
                logic_adapters=[
                    'chatterbot.logic.MathematicalEvaluation',
                    #'chatterbot.logic.TimeLogicAdapter',
                    'chatterbot.logic.BestMatch',
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'default_response': 'I am sorry, but I do not understand. I am still learning.',
                        'maximum_similarity_threshold': 0.90
                    }
                 ],
                #database_uri='sqlite:///db.sqlite3'
)

training_data = open('training_data/training_data.txt').read().splitlines() + open('training_data/conversation.txt').read().splitlines()

trainer = ListTrainer(cimabot)
trainer.train(training_data)

trainer_corpus = ChatterBotCorpusTrainer(cimabot)
trainer_corpus.train('chatterbot.corpus.english.greetings')
trainer_corpus.train('chatterbot.corpus.english.computers')
trainer_corpus.train('chatterbot.corpus.english.ai')
trainer_corpus.train('chatterbot.corpus.english.conversations')
trainer_corpus.train('chatterbot.corpus.english.botprofile')
trainer_corpus.train('chatterbot.corpus.english.humor')



