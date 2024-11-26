import base64
from mistralai import Mistral

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

def get_result(image_path):
    with open('api_key.txt') as f:
        api_key = f.readline()

    # Path to your image
    # image_path = "data/images/certificate.png"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Specify model
    model = "pixtral-12b-2409"

    # Initialize the Mistral client
    client = Mistral(api_key=api_key)

    # Define the messages for the chat
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Напиши json где будет указан title (какой это анализ? анализ крови или флюрография - выбери одно из двух), class (В ответе дай только целочисленное значение, если это флюроография - 1, если это анализ крови - 2, если ни одно из перечисленных не подходит - 0), date (Напиши дату поступления анализов. В ответе дай только дату, дата должна быть в формате %Y.%M.%D) и recommendation (Напиши немного рекомендаций). В ответ дай только json"
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]

    # Get the chat response
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )

    # Print the content of the response
    return str(chat_response.choices[0].message.content)
