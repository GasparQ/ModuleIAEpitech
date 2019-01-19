from time import sleep

import os

import sys


def get_question(index):
    try:
        qf = open('./%d/questions.txt' % index, 'r')
        question = qf.read()
        qf.close()
        open('./%d/questions.txt' % index, 'w').close()
    except:
        return ''
    return question


def send_response(index, response):
    rf = open('./%d/reponses.txt' % index, 'w')
    rf.write(response)
    rf.close()


def runai(ai):
    try:
        os.mkdir('./%d' % ai.id)
    except:
        pass

    try:
        open('./%d/infos.txt' % ai.id, 'w').close()
        open('./%d/questions.txt' % ai.id, 'w').close()
        open('./%d/reponses.txt' % ai.id, 'w').close()
    except:
        pass

    while not ai.state.gameOver:
        question = ''
        while len(question) == 0 and not ai.state.gameOver:
            question = get_question(ai.id)
            ai.update_state('./%d/infos.txt' % ai.id)
            sleep(0.1)

        if ai.state.gameOver:
            break

        reponse = ai.__play__(question)

        if not ai.state.gameOver:
            send_response(ai.id, reponse)
    print('Game ended')
