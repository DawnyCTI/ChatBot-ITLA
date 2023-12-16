
import preguntas_respuesta
import random
import re

def responder_pregunta(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_messages(split_message, preguntas_respuesta.ITLA_PREGUNTAS_RESPUESTAS)
    return response

def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message, qa_dict):
    highest_prob = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob
        highest_prob[bot_response] = message_probability(message, list_of_words, single_response, required_words)


    response('¡Hola! ¿En qué puedo ayudarte hoy?', ['hola', 'klk', 'saludos', 'buenas'], single_response=True)
    response('Todo bien, gracias. ¿Y tú qué tal?', ['como', 'estas', 'va', 'vas', 'sientes'], required_words=['como'])
    response('Nos encontramos en un lugar genial: Autopista Las Américas, Km. 27, PCSD, La Caleta, Boca Chica 11606', ['ubicados', 'donde', 'ubicacion'], single_response=True)
    response('Siempre a tu disposición. ¿Algún tema específico que te interese?', ['gracias', 'te lo agredezco', 'thanks'], single_response=True)


    for pregunta, respuesta in qa_dict.items():
        response(respuesta, pregunta.lower().split(), single_response=True)

    best_match = max(highest_prob, key=highest_prob.get)
    return unknown() if highest_prob[best_match] < 1 else best_match

def unknown():
    response = ['¿Puedes repetir eso?', 'No estoy seguro de entender. Intenta reformularlo, por favor.', '¡Google es tu amigo para eso!'][random.randrange(3)]
    return response

while True:
    user_input = input('Tú: ')
    bot_response = responder_pregunta(user_input)
    print("Bot:", bot_response)
