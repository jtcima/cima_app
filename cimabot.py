from chatterbot import ChatBot

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
