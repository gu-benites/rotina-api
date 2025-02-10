import os
import asyncio
import time
import json
import httpx
import pinecone
from openai import OpenAI
from pinecone import Pinecone
from config import OPENAI_API_KEY, OPENAI_ORG_ID, PINECONE_API_KEY, PINECONE_REGION, PINECONE_INDEX_NAME

# Initialize OpenAI client
client = OpenAI(
    organization=OPENAI_ORG_ID,
    api_key=OPENAI_API_KEY
)

# Pinecone-related functions
def initialize_pinecone():
    return Pinecone(api_key=PINECONE_API_KEY)

def connect_to_pinecone_index(pinecone_client):
    return pinecone_client.Index(PINECONE_INDEX_NAME)

async def aromachat(input_query):
    print("Getting embeddings from OpenAI...")
    model_embed = os.environ.get("OPENAI_MODEL_EMBED")
    embed_query = await asyncio.to_thread(
        client.embeddings.create, input=input_query, model=model_embed
    )
    embeddings = embed_query.data[0].embedding
    print("Embeddings obtained.")
    # Retry logic for Pinecone connection
    max_retries = 3
    for retry_count in range(max_retries):
        try:
            print("Initializing Pinecone...")
            pinecone_client = initialize_pinecone()
            print(pinecone_client)
            print("Connecting to Pinecone index...")
            index = connect_to_pinecone_index(pinecone_client)
            print(index)
            print(f"Searching Pinecone query: {input_query}.")
            query_response = index.query(
                vector=embeddings,
                top_k=5,
                include_values=True,
                include_metadata=True,
            )
            pinecone_results = {
                'description': f'context to help answer query: {input_query}. Only use context if relevant information can be found regarding user input_query.',
                'context': []
            }
            for match in query_response.matches:
                if match.score > 0.70:  # Threshold can be adjusted as needed
                    context_text = match.metadata.get('text')
                    pinecone_results['context'].append(context_text)
            print("Results from Pinecone successfully extracted.")
            return pinecone_results
        except Exception as e:
            print(f"Error connecting to Pinecone: {str(e)}")
            if retry_count < max_retries - 1:
                print("Retrying...")
                time.sleep(2)
            else:
                print("Max retries reached. Unable to connect to Pinecone.")
                raise

def brasil_living_kit(health_problem):
    try:
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-1106:rotina-natural::8RqjEBby",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um expert em óleos essenciais e aromaterapia. Sua tarefa é montar uma única receita e protocolo para o problema de saúde listado usando somente usando os produtos mais apropriados da lista abaixo:\n\nProdutos doterra disponíveis:\n1. Lavender (Lavanda), Lavandula angustifolia\n2. Lemon (Limão-Siciliano), Citrus limon\n3. Peppermint (Hortelã-Pimenta), Mentha piperita\n4. Melaleuca (Tea Tree), Melaleuca alternifolia\n5. Tangerine (Tangerina), Citrus reticulata\n6. Frankincense (Olíbano)\n   - Ingredientes principais: Óleo de Boswellia carterii, Óleo de resina de Boswellia sacra, Óleo de resina de Boswellia papyrifera, Óleo de resina de Boswellia frereana.\n7. Copaíba\n    - Ingredientes principais: Óleo de resina de Copaifera coriacea/langsdorffii/officinalis/reticulata.\n8. doTERRA Balance®\n    - Ingredientes principais: Óleo de coco, Óleo de ramo/folha de abeto negro (Picea mariana), Óleo da folha de canela-canforeira (Camphor), Óleo de Boswellia carterii (Frankincense), Óleo da flor/folha/tronco de Tanacetum annuum (Blue Tansy), Óleo de camomila, Extrato da flor de Osmanthus fragrans.\n9. doTERRA ZenGest®\n    - Ingredientes principais: Óleo de Mentha piperita (Peppermint), Óleo da semente de coentro (Coriandrum sativum), Óleo da raiz de gengibre (Zingiber officinale), Óleo da semente de Carum carvi (Caraway), Óleo da semente de cardamomo (Elettaria cardamomum), Óleo de funcho (Foeniculum vulgare), Óleo de fruto/semente de anis estrelado (Illicium verum).\n10. doTERRA Deep Blue®\n   - Ingredientes principais: Óleo da folha de Gaultheria procumbens (Wintergreen), Óleo de canela-canforeira (Camphor), Óleo de Mentha piperita (Peppermint), Óleo da flor de Cananga odorata (Ylang Ylang), Óleo da flor/folha/tronco de Tanacetum annuum (Blue Tansy), Óleo de camomila, Extrato da flor de Osmanthus fragrans.\n11. doTERRA On Guard®\n   - Ingredientes principais: Óleo da casca de laranja doce (Citrus sinensis), Óleo do botão de cravo (Eugenia caryophyllata), Óleo da folha de canela (Cinnamomum zeylanicum), Óleo da casca de canela, Óleo de eucalipto (Eucalyptus radiata), Óleo da folha de alecrim (Rosmarinus officinalis).\n12. doTERRA Breathe®\n   - Ingredientes principais: Óleo da folha de Laurus nobilis (Lourel), Óleo da folha de Eucalyptus globulus, Óleo de Mentha piperita (Peppermint), Óleo de melaleuca (Tea Tree), Óleo da casca de Citrus limon (Limão), Óleo da semente de Elettaria cardamomum (Cardamomo), Óleo da folha de Cinnamomum camphora (Ravintsara), Óleo da folha de Ravensara aromatica.",
                },
                {
                    "role": "user",
                    "content": f"###Problema de saúde###: {health_problem}\nSua tarefa: monte uma única receita e protocolo para atender uma pessoa com o problema de saúde acima."
                }
            ],
            temperature=0,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            return "Não foi possível gerar uma resposta."
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Ocorreu um erro ao gerar a resposta."
