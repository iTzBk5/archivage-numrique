import elasticsearch
from elasticsearch_dsl import Search,Q
from googletrans import Translator,LANGUAGES
from langdetect import detect

ELASTIC_HOST = 'http://localhost:9200'

client = elasticsearch.Elasticsearch(hosts=[ELASTIC_HOST],
                                     http_auth=('admin', 'adminadmin')
                                     )



def lookup(query, index='blog', fields = ['title','description']):

    detected_lang = detect(query)
    traslator_query =""
    if detected_lang != 'fr':
        traslator = Translator()
        traslator_query= traslator.translate(query, src=detected_lang,dest='fr').text

    if not traslator_query:
        return
    

    #search_query = Q('bool', should=[
      #  Q("multi_match", fields=fields, query=traslator_query, fuzziness='AUTO'),
     #   Q("more_like_this", fields=fields, like=traslator_query, min_term_freq=1, min_doc_freq=1)
    #])

    #results = Search(index=index).using(client).query(search_query)
    
    results = Search(index = index).using(client).query("multi_match",fields=fields, fuzziness = 'AUTO',query=traslator_query)

    q_results = []


    for hit in results:
        print(hit.id)
        print(hit.title)
        print(hit.description)
        print(hit.url)
        summary = getattr(hit, 'summary', 'No summary available') 
        uploaded_file = getattr(hit, 'uploaded_file', 'No pdf')
        image_url = getattr(hit, 'image', 'default_image_path_or_url')
        
        data = {
            "id": hit.id,
            "title": hit.title,
            "description": hit.description,
            "url": hit.url,
            "image": image_url,
            "summary": summary,
            "uploaded_file":uploaded_file,
        }
        q_results.append(data)
    return q_results