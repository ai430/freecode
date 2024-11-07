import openai
from seckey import my_sk

client = openai.OpenAI(api_key=my_sk)

max_tokens=500
temperature =0.1
top_p=0.5
#top_k=50
freq_pen=1
pres_pen=0.5

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role": "user",  
         "content": "what is the best fruit in diabetes? Give 7 fruits low in sugar"}
    ],
    max_tokens=max_tokens,
    temperature=temperature,
    n=1,
    top_p=top_p,
    #top_k=top_k,
    frequency_penalty=freq_pen,
    presence_penalty=pres_pen,
    stop=['.', 'End of list']
    
    
)
print(response.choices[0].message.content)
