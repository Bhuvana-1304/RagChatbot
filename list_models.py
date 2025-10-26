import google.generativeai as genai
genai.configure(api_key="AIzaSyC4-idS_JcR4OZScXFzoZpSAK758Z_Edv8")
print([m.name for m in genai.list_models()])
