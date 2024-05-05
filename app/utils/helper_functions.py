PROMPT_LIMIT = 3750

def chunk_text(text, chunk_size=200):
    # Split the text by sentences to avoid breaking in the middle of a sentence
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        # Check if adding the next sentence exceeds the chunk size
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + '. '
        else:
            # If the chunk reaches the desired size, add it to the chunks list
            chunks.append(current_chunk)
            current_chunk = sentence + '. '
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

#prompt engineering
def build_prompt(query, context):

    prompt_start = (
        "Answer the query. If the query asks for book recommendations/availability, use the inventory of books we have that is attached. If instead it asks about store policies or asks to add books to cart, DO NOT use the context. Instead, look at the history of the conversation and provide an appropriate answer. Return just the answer to the question, don't add anything else. Don't start your response with the word 'Answer:'. Make sure your response is in markdown format. "+
        "Inventory:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )

    # append context chunks until we hit the 
    # limit of tokens we want to send to the prompt.   
    prompt = prompt_start + context + prompt_end
    
    return prompt

def construct_messages_list(chat_history, prompt):
    messages = [{"role": "system", "content": "You are a helpful online bookstore assistant (you can provide book recommendations, add selected items to a user's shopping cart, and answer General inquiries about store policies, shipping, and returns.)"}]
    
    # Populate the messages array with the current chat history
    print(chat_history)
    for message in chat_history:
        print(message)
        if message['isBot']:
            messages.append({"role": "system", "content": message["text"]})
        else:
            messages.append({"role": "user", "content": message["text"]})
    # Replace last message with the full prompt
    messages.append({"role": "user", "content": prompt})
    
    return messages