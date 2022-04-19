import requests
import json

response = requests.post('http://localhost:3030/uni/query',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>

PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

 # 13)Which topics are covered in Lab 2 of COMP6741?


    ASK{
        ?course dcterms:title "%s"@en.
        ?student uni:hasRecord ?rec.
        ?rec dcterms:title ?course.
        ?student foaf:givenName "%s".
        ?rec uni:hasGot ?grade.
        FILTER (?grade != "F")
    }"""% (('INTELLIGENT SYSTEMS', 'Joe'))})
# out=json.loads(response.text)
hi=response.json()
print(hi)
# print(hi['results']['bindings'][0]['desc']['value'])
print(hi['boolean'])
if hi['boolean']== True:
    print("hello")
else:
    print("false")
# for result,value in hi['results']['bindings'].items(): #hi["bindings"]:
#     # print(result,":",value)
#     print(result)
#     break
topics= []
links = []
for val in hi['results']['bindings']:
    links.append(val['topic']['value'])
    topics.append(val['tname']['value'])
print(topics)
print(links)
    # break
print("heelo")
