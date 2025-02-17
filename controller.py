from discord import Message
from directCommands.directCommands import directCommand
from simpleResponse.simpleResponse import simpleResponse
from psychCommands.psychCommands import psychCommand

async def controller (message: Message, sessions, client, tokenizer, model) -> None:

    user_message: str = str(message.content)

    if not user_message:
        print("Intents were not enabled")
        return False
    
    if user_message[0] == ';':
        user_message = user_message[1:]
        query = "[q]" + user_message + "[a]"

        tokenized_inputs = tokenizer(
            query, 
            padding=True, 
            truncation=True,  # Explicitly enable truncation
            max_length=512,  # Ensure this matches your model's limit
            return_tensors="pt"  # Use 'tf' for TensorFlow
        )

        # **Generate Response**
        response = model.generate(
            tokenized_inputs["input_ids"], 
            max_new_tokens=100,  # Allow longer responses
            temperature=0.7, 
            top_p=0.9, 
            do_sample=True
        )

        # Decode and Print Output
        generated_text = tokenizer.batch_decode(response, skip_special_tokens=True)

        # Extract the response text after '[a]'
        response_text = generated_text[0]
        if '[a]' in response_text:
            response_text = response_text.split('[a]', 1)[1].strip()

        # Send the response back to the Discord channel
        await message.channel.send(response_text)


    #if the message starts with a question mark, it is a direct command
    #check directCommands folder
    # if user_message[0] == '?':
    #     user_message = user_message[1:]
    #     await directCommand(message, user_message)

    # if user_message[0] == '!':
    #     user_message = user_message[1:]
    #     await psychCommand(message, user_message, sessions, client)

    #if the message has no starting tag, it has a few fun responses
    #check simpleResponse folder
    # else:
    #     await simpleResponse(message)

    return True

