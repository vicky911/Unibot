# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="my first action!")

        return []


class q1(Action):
    def name(self) -> Text:
        return "q1_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT ?name ?credit
WHERE {
  	?course dcmitype:subject "%s" .
    ?course dcmitype:identifier "%s" .
	?course dcterms:title ?name .
	?course uni:hasCredit ?credit.
}
    """ % (tracker.slots['course'], tracker.slots['course_number'])})
        hi = response.json()
        str = ""
        if hi == []:
            str = "I don't know"
        # print(response.status_code)
        # print(hi)
        else:
            for val in hi['results']['bindings']:
                name = val['name']['value']
                credit = val['credit']['value']
                str = "Name of the course is " + name + " and the credit is " + credit
                # print(credit)
        dispatcher.utter_message(str)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q2(Action):
    def name(self) -> Text:
        return "q2_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT ?cname
WHERE{
  	?student foaf:givenName "%s".
  	?student uni:hasRecord ?rec.
  	?rec dcterms:title ?cid.
  	?cid dcterms:title ?cname.
  	?rec uni:hasGot ?grade.
	FILTER (?grade != "F").
 }
    """ % (tracker.slots['person'])})
        hi = response.json()
        # print(response.status_code)
        # print(hi)
        hi = response.json()
        str = ''
        if hi['results']['bindings'] == []:
            str = "I don't know"
        else:
            courses = []
            for val in hi['results']['bindings']:
                courses.append(val['cname']['value'])
            # print(courses)
            str = tracker.slots['person'] + " is competent in {}".format(', '.join(courses))
        # print(str)
        # print(credit)
        dispatcher.utter_message(str)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q3(Action):
    def name(self) -> Text:
        return "q3_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT ?topic ?tname
WHERE {
  	?course dcmitype:subject "%s" .
   	?course dcmitype:identifier "%s" .
	?lecture dcterms:isPartOf ?course .
  	?lecture dcmitype:identifier "%s" .
	?lecture uni:hasResource ?res.
  	?res uni:hasTopic ?topic.
  	?topic rdfs:label ?tname

 } 
    """ % (tracker.slots['course'], tracker.slots['course_number'], tracker.slots['lecture_number'])})
        # hi = response.json()
        # print(response.status_code)
        topics = []
        links = []
        opt = ''
        hi = response.json()
        if hi['results']['bindings'] == []:
            str = "I don't know"

        # print(hi)
        else:
            for val in hi['results']['bindings']:
                links.append(val['topic']['value'])
                topics.append(val['tname']['value'])

            str = "Topics covered in lecture number " + tracker.slots['lecture_number'] + " of " + tracker.slots[
                'course'] + " " + tracker.slots['course_number'] + " are " + "\n"
            # opt = ''
            for x, y in zip(topics, links):
                opt += x + ", " + y + "\n"

        output = str + opt
        # print(opt)
        # print(str)
        # print(credit)
        dispatcher.utter_message(output)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q4(Action):
    def name(self) -> Text:
        return "q4_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT  ?outline
WHERE {
  	?course dcmitype:subject "%s" .
  	?course dcmitype:identifier "%s" .
  	?course uni:hasOutline ?content .
	?content dcterms:type "OUTLINE" .
    ?content dcterms:source ?outline .
}   
    """ % (tracker.slots['course'], tracker.slots['course_number'])})
        hi = response.json()
        str = ""
        if hi['results']['bindings'] == []:
            str = "I don't know"
        # print(response.status_code)
        else:
            for val in hi['results']['bindings']:
                str = "Outline for " + tracker.slots['course'] + " " + tracker.slots['course_number'] + " is " + \
                      val['outline']['value']

            # print(credit)
        dispatcher.utter_message(str)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q5(Action):
    def name(self) -> Text:
        return "q5_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT  ?Reading
WHERE {
  	?courseid dcterms:title "%s"@en.
  	?courseid rdf:type uni:Course .	
  	?lectureid dcterms:isPartOf ?courseid.  	
  	?lectureid uni:hasResource ?content.
  	?content dcterms:type "READING".
    ?content dcterms:source ?Reading.
}   
    """ % (tracker.slots['course_name'])})
        hi = response.json()
        # print(response.status_code)
        readings = []
        hi = response.json()
        if hi['results']['bindings'] == []:
            str = "I don't know"
        else:
            for val in hi['results']['bindings']:
                readings.append(val['Reading']['value'])
            str = "Recommended readings for " + tracker.slots['course'] + " " + tracker.slots[
                'course_number'] + " are {}".format(', '.join(readings))

            # print(credit)
        dispatcher.utter_message(str)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q6(Action):
    def name(self) -> Text:
        return "q6_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT ?firstname ?lastName ?title ?grade
WHERE{

  	?course dcmitype:subject "%s" .
 	?course dcmitype:identifier "%s".
  	?course dcterms:title ?title.
  	?student uni:studyAt uni:Concordia_University.
  	?student uni:hasRecord ?rec.
  	?rec dcterms:title ?course.
  	?rec uni:hasGot ?grade.
  	?student foaf:givenName ?firstname.
  	?student foaf:familyName ?lastName.
}   
    """ % (tracker.slots['course'], tracker.slots['course_number'])})
        hi = response.json()

        # print(response.status_code)
        name = []
        grade = []
        opt = ''
        hi = response.json()
        if hi['results']['bindings'] == []:
            str = "I don't know"
        else:
            for val in hi['results']['bindings']:
                name.append(val['firstname']['value'] + val['lastName']['value'])
                grade.append(val['grade']['value'])
            str = "Grades for students of  " + tracker.slots['course'] + " " + tracker.slots[
                'course_number'] + " are as follows: " + "\n"
            # opt = ''
            for x, y in zip(name, grade):
                opt += x + ", " + y + "; "
        output = str + opt
        # print(credit)
        dispatcher.utter_message(output)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q7(Action):
    def name(self) -> Text:
        return "q7_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT (count(?course) as ?courseCount)
WHERE{

  	?course dcmitype:subject "%s" .
  	?course rdf:type uni:Course.

}   
    """ % (tracker.slots['course'])})
        hi = response.json()
        hi = response.json()
        if hi['results']['bindings'] == []:
            str = "I don't know"
        else:
            for val in hi['results']['bindings']:
                str = "Total courses offered in " + tracker.slots['course'] + " are " + val['courseCount']['value']
            # print(credit)
        dispatcher.utter_message(str)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q8(Action):
    def name(self) -> Text:
        return "q8_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

    ASK{
        ?course dcterms:title "%s"@en.
        ?student uni:hasRecord ?rec.
        ?rec dcterms:title ?course.
        ?student foaf:givenName "%s".
        ?rec uni:hasGot ?grade.
        FILTER (?grade != "F")
    }

    """ % (tracker.slots['course_name'], tracker.slots['person'])})
        hi = response.json()
        # print(hi)
        # print(hi['boolean'])
        str = ''
        if hi['boolean'] == False:
            str = " No, " + tracker.slots['person'] + " is not competent in " + tracker.slots['course_name']
        elif hi['boolean'] == True:
            str = " Yes, " + tracker.slots['person'] + " is competent in " + tracker.slots['course_name']
        dispatcher.utter_message(str)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q9(Action):
    def name(self) -> Text:
        return "q9_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT (MAX(?credit) as ?courseCredit)
WHERE {
	?course rdf:type uni:Course.
  	?course dcterms:isPartOf unidata:Concordia_University.
	?course uni:hasCredit ?credit
}
    """})
        hi = response.json()
        if hi['results']['bindings'] == []:
            str = "I don't know"
        else:
            str = " Maximum credit for any course offered by Concordia University is " + \
                  hi['results']['bindings'][0]['courseCredit']['value']
        dispatcher.utter_message(str)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q10(Action):
    def name(self) -> Text:
        return "q10_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT ?grade

WHERE{
  	?sid foaf:givenName "%s".
  	?sid foaf:familyName "%s".
  	?cid dcmitype:subject "%s".
  	?cid dcmitype:identifier "%s".
  	?sid uni:hasRecord ?rec.
  	?rec dcterms:title ?cid.
  	?rec uni:hasGot ?grade.
}

    """ % (tracker.slots['givenName'], tracker.slots['familyName'], tracker.slots['course'],
           tracker.slots['course_number'])})
        hi = response.json()
        hi = response.json()
        str = ''
        if hi['results']['bindings'] == []:
            str = "I don't know"
        else:
            str = "Grade of " + tracker.slots['givenName'] + " " + tracker.slots['familyName'] + " in " + tracker.slots[
                'course'] + " " + tracker.slots['course_number'] + " is " + hi['results']['bindings'][0]['grade'][
                      'value']

        dispatcher.utter_message(str)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q12(Action):
    def name(self) -> Text:
        return "q12_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT ?cname ?desc
WHERE {
  	?course dcmitype:subject "%s" .
   	?course dcmitype:identifier "%s" .
  	?course dcterms:title ?cname.
  	?course dcterms:description ?desc.
}

    """ % (tracker.slots['course'], tracker.slots['course_number'])})
        hi = response.json()
        # print(hi)
        str = ''
        hi = response.json()
        if hi['results']['bindings'] == []:
            str = "I don't know"
        else:
            str = tracker.slots['course'] + " " + tracker.slots['course_number'] + " is about " + \
                  hi['results']['bindings'][0]['desc']['value']

        dispatcher.utter_message(str)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q13(Action):
    def name(self) -> Text:
        return "q13_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT ?topic ?tname
WHERE {
  	?course dcmitype:subject "%s" .
   	?course dcmitype:identifier "%s" .
	?lab dcterms:isPartOf ?course .
  	?lab dcmitype:identifier "%s" .
  	?lab rdf:type uni:Lab.
	?lab uni:hasResource ?res.
  	?res uni:hasTopic ?topic.
  	?topic rdfs:label ?tname.
}

    """ % (tracker.slots['course'], tracker.slots['course_number'], tracker.slots['lab_number'])})
        # hi = response.json()
        # print(hi)
        # print(response.status_code)

        hi = response.json()
        # print(hi)
        topics = []
        links = []
        str = ''
        opt = ''
        if hi['results']['bindings'] == []:
            str = "I don't know"
        else:
            for val in hi['results']['bindings']:
                links.append(val['topic']['value'])
                topics.append(val['tname']['value'])

            str = "Topics covered lab     number " + tracker.slots['lab_number'] + " of " + tracker.slots[
                'course'] + " " + tracker.slots['course_number'] + " are " "\n"

            for x, y in zip(topics, links):
                opt += x + ", " + y + "\n"

        output = str + opt
        dispatcher.utter_message(output)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []


class q14(Action):
    def name(self) -> Text:
        return "q14_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/uni/sparql',
                                 data={'query': """
PREFIX unidata: <http://uni.io/data#> 
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX uni: <http://uni.io/schema#> 
PREFIX dbo: <http://dbpedia.org/ontology/> 
PREFIX dbr: <http://dbpedia.org/resource/> 
PREFIX un: <http://www.w3.org/2007/ont/unit#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

SELECT ?cname (count (?cname) as ?count)
WHERE {
    ?course dcterms:isPartOf unidata:Concordia_University.
  	?course dcterms:title ?cname.
  	?event dcterms:isPartOf ?course.
  	?event uni:hasResource ?con.
  	?con uni:hasTopic ?topic.
  	?topic rdfs:label "%s".
}GROUP BY ?cname ORDER BY DESC(?count)


    """ % (tracker.slots['subject'])})
        hi = response.json()
        course = []
        count = []
        str = ''
        opt = ''
        hi = response.json()
        if hi['results']['bindings'] == []:
            str = "I don't know"
        else:
            for val in hi['results']['bindings']:
                course.append(val['cname']['value'])
                count.append(val['count']['value'])

            str = "Courses covering this topic are " + "\n"
            # opt = ''
            for x, y in zip(course, count):
                opt += x + ", " + y + "\n"

        output = str + opt
        dispatcher.utter_message(output)
        # for param in hi["results"]["bindings"]:
        #     dispatcher.utter_message(text=str(param['name']['credit']))
        # print("heelo")
        return []
