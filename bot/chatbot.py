import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path: str, user_data: dict):
    with open(file_path, 'w') as file:
        json.dump(user_data, file, indent=2)

def find_best_match(user_question: str, questions: list) -> str:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    else:
        return None

def get_answer_for_match(question: str, knowledge_base: dict) -> str:
    for ques in knowledge_base['questions']:
        if ques['question'] == question:
            return ques['answer']
    return None

def chatbot():
    file_name = "knowledge_base.json"
    knowledge_base = load_knowledge_base(file_name)
    while True:
        user_question = input("You: ")
        if user_question.lower() == 'quit':
            break
        ques_list = [q['question'] for q in knowledge_base['questions']]
        best_match = find_best_match(user_question, ques_list)
        if best_match:
            answer = get_answer_for_match(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: I don't know the answer, please teach me!")
            user_answer = input("Type the answer or enter 'skip' to skip: ")
            if user_answer.lower() != 'skip':
                knowledge_base['questions'].append({'question': user_question, 'answer': user_answer})
                save_knowledge_base(file_name, knowledge_base)
                print("Bot: Thank you for teaching me. I have learned a new response.")

if __name__ == "__main__":
    chatbot()
