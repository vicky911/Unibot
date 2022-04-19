import pandas
from uuid import uuid4

from rdflib import Graph, RDFS, URIRef, Literal
from rdflib.namespace import RDF, DC, DCTERMS, Namespace, NamespaceManager

DCMITYPE = Namespace("http://purl.org/dc/dcmitype/")
DBR = Namespace("http://dbpedia.org/resource/")
DBO = Namespace("http://dbpedia.org/ontology/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
LOCAL = Namespace("http://localhost:3030")
UNISCHEMA = Namespace("http://uni.io/schema#")
UNIDATA = Namespace("http://uni.io/data#")


# XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

def addData(location, type):
    contenId = UNIDATA["c" + str(uuid4())]
    graph.add((contenId, RDF.type, UNISCHEMA.Content))
    # graph.add((contenId, RDF.type, DCTERMS.BibliographicResource))
    graph.add((contenId, DCTERMS.type, Literal(type)))
    if 'http' in location:
        graph.add((contenId, DCTERMS.source, URIRef(location)))
    else:
        graph.add((contenId, DCTERMS.source, LOCAL[location]))

    return contenId


# graph1=Graph()
# to bind prefix with URI
namespace_manager = NamespaceManager(Graph())
namespace_manager.bind('UNIVERSITY', UNISCHEMA, override=False)

graph = Graph()
graph.bind('DC', DC)

# Add Univeristy Node to graph
graph.add((URIRef(UNIDATA.Concordia_University), RDF.type, UNISCHEMA.University))
graph.add((URIRef(UNIDATA.Concordia_University), RDFS.label, Literal(str("Concordia University"))))
graph.add((URIRef(UNIDATA.Concordia_University), RDFS.seeAlso, DBR.Concordia_University))


# To Read csv files
courseDataCSV = pandas.read_csv('datasets/courseData.csv')
studentDataCSV = pandas.read_csv('datasets/StudentData.csv')
lectureDataCSV = pandas.read_csv('datasets/lectureData.csv')
lectureContentCSV = pandas.read_csv('datasets/lectureContent.csv')
labDataCSV = pandas.read_csv('datasets/labData.csv')
labContentCSV = pandas.read_csv('datasets/labContent.csv')
TermCSV = pandas.read_csv('datasets/Term.csv')
TopicCSV = pandas.read_csv('datasets/Topics.csv')
courdID_dict={}
# To add triples in the graph
for courseIndex in range(len(courseDataCSV)):

    courseLine = courseDataCSV.iloc[courseIndex]
    courseId = UNIDATA[str(courseLine['CourseId'])]
    graph.add((courseId, RDF.type, UNISCHEMA.Course))
    graph.add((courseId, DCMITYPE.subject, Literal(str(courseLine['Subject']))))
    graph.add((courseId, DCMITYPE.identifier, Literal(str(courseLine['Number']))))
    graph.add((courseId, DCTERMS.title, Literal(str(courseLine['Title']), lang="en")))
    graph.add((courseId, UNISCHEMA.hasCredit, Literal(str(courseLine['Class Units']))))
    graph.add((courseId, DCTERMS.description, Literal(str(courseLine['Description']), lang="en")))
    if not pandas.isnull(courseLine['seeAlso']):
        graph.add((courseId, RDFS.seeAlso, Literal((courseLine['seeAlso']))))
    graph.add((courseId, DCTERMS.isPartOf, UNIDATA.Concordia_University))
    if not pandas.isnull(courseLine['Outline']):
        contentId = addData(courseLine["Outline"], "OUTLINE")
        graph.add((courseId, UNISCHEMA.hasOutline, contentId))

    # Student and Course Mapping
    if TermCSV[TermCSV['CourseId'] == courseLine['CourseId']].shape[0] != 0:
        courdID_dict[courseLine['CourseId']] = courseId
    # print(courseStudent)

    # Lecture and Course Mapping
    courseLecturesRecord = lectureDataCSV[lectureDataCSV['CourseId'] == courseLine['CourseId']]
    for lectureIndex in range(len(courseLecturesRecord)):
        lectureLine = courseLecturesRecord.iloc[lectureIndex]
        lectureId = UNIDATA["l" + str(uuid4())]
        graph.add((lectureId, RDF.type, UNISCHEMA.Lecture))
        graph.add((lectureId, DCMITYPE.identifier, Literal(str(lectureLine['Id']))))
        graph.add((lectureId, DCTERMS.title, Literal(str(lectureLine['Title']))))
        graph.add((lectureId, DCTERMS.isPartOf, courseId))

        # Content Mapping with lecture
        lectureContentRecord = lectureContentCSV[
            (lectureContentCSV['CourseId'] == courseLine['CourseId']) & (lectureContentCSV['Id'] == lectureLine['Id'])]
        for contentIndex in range(len(lectureContentRecord)):

            contentLine = lectureContentRecord.iloc[contentIndex]
            contentId = addData(contentLine["Content"], contentLine["ContentType"])
            graph.add((lectureId, UNISCHEMA.hasResource, contentId))

            #Content and Topic csv mapping
            contentTopicRecord = TopicCSV[(TopicCSV['CourseId'] == contentLine['CourseId']) & (TopicCSV['Identifier'] == contentLine['Id']) &
                                          ((TopicCSV['Type']==contentLine['ContentType']))]
            # print(len(contentTopicRecord))
            for topicIndex in range(len(contentTopicRecord)):
                # print("Hello")
                topicLine = contentTopicRecord.iloc[topicIndex]
                graph.add((contentId, UNISCHEMA.hasTopic, URIRef(topicLine['Topic Link']) ))
                # topicID=UNIDATA[str(topicLine['Topic Name'])]Literal(str(topicLine['Topic Name']))
                graph.add((URIRef(topicLine['Topic Link']), RDF.type, UNISCHEMA.Topic))
                # graph.add((Literal(str(topicLine['Topic Name'])), RDFS.seeAlso, ))
                graph.add((URIRef(topicLine['Topic Link']), RDFS.label,  Literal(str(topicLine['Topic Name']))))
                graph.add((URIRef(topicLine['Topic Link']), RDF.type,  Literal(str(topicLine['Entity Type']))))


    # Lab and Course Mapping
    courseLabRecord = labDataCSV[labDataCSV['CourseId'] == courseLine['CourseId']]
    for labIndex in range(len(courseLabRecord)):
        labLine = courseLabRecord.iloc[labIndex]
        labId = UNIDATA["lb" + str(uuid4())]
        graph.add((labId, RDF.type, UNISCHEMA.Lab))
        graph.add((labId, DCMITYPE.identifier, Literal(str(labLine['Id']))))
        graph.add((labId, UNISCHEMA.Topic, Literal(str(labLine['Title']))))
        # graph.add((labId, RDFS.seeAlso, URIRef(labLine['seeAlso'])))
        graph.add((labId, DCTERMS.isPartOf, courseId))
        # Content Mapping with lab
        labContentRecord = labContentCSV[
            (labContentCSV['CourseId'] == courseLine['CourseId']) & (labContentCSV['Id'] == labLine['Id'])]
        for contentIndex in range(len(labContentRecord)):
            contentLine = labContentRecord.iloc[contentIndex]

            contentId = addData(contentLine["Content"], contentLine["ContentType"])
            graph.add((labId, UNISCHEMA.hasResource, contentId))

            # Lab Content and Topic csv mapping
            contentTopicRecord = TopicCSV[
                (TopicCSV['CourseId'] == contentLine['CourseId']) & (TopicCSV['Identifier'] == contentLine['Id']) & (
                (TopicCSV['Type'] == contentLine['ContentType']))]

            # print(contentLine['CourseId'], "   " ,contentLine['Id'])
            for topicIndex in range(len(contentTopicRecord)):
                # print((len(contentTopicRecord)))
                topicLine = contentTopicRecord.iloc[topicIndex]
                # topicID = UNIDATA[str(topicLine['Topic Name'])]
                graph.add((contentId, UNISCHEMA.hasTopic, URIRef(topicLine['Topic Link'])))
                # topicID=UNIDATA[str(topicLine['Topic Name'])]Literal(str(topicLine['Topic Name']))
                graph.add((URIRef(topicLine['Topic Link']), RDF.type, UNISCHEMA.Topic))
                # graph.add((Literal(str(topicLine['Topic Name'])), RDFS.seeAlso, ))
                graph.add((URIRef(topicLine['Topic Link']), RDFS.label, Literal(str(topicLine['Topic Name']))))
                graph.add((URIRef(topicLine['Topic Link']), RDF.type, Literal(str(topicLine['Entity Type']))))

#Student Mapping
count=1
for studentIndex in range(len(studentDataCSV)):
    studentLine = studentDataCSV.iloc[studentIndex]
    # print(student)
    studentId = UNIDATA["s" + str(uuid4())]
    graph.add((studentId, RDF.type, UNISCHEMA.Student))
    graph.add((studentId, RDFS.subClassOf, FOAF.Person))
    graph.add((studentId, UNISCHEMA.studyAt, UNISCHEMA.Concordia_University))
    graph.add((studentId, FOAF.givenName, Literal(str(studentLine['firstName']))))
    graph.add((studentId, FOAF.familyName, Literal(str(studentLine['lastName']))))
    graph.add((studentId, DCMITYPE.identifier, Literal(str(studentLine['IDNumber']))))
    graph.add((studentId, FOAF.mbox, Literal(str(studentLine['Email']))))



    studentTermRecord = TermCSV[(TermCSV['IDNumber'] == studentLine['IDNumber'])]

    for TermIndex in range(len(studentTermRecord)):
        Record = UNIDATA["Record" + str(count)]
        graph.add((studentId, UNISCHEMA.hasRecord, Record))
        graph.add((Record, RDF.type, UNISCHEMA.Record))
        TermLine = studentTermRecord.iloc[TermIndex]
        # studentEnrolledId = addData(studentEnrolledLine["Content"], studentEnrolledLine["ContentType"])
        # graph.add((studentId, UNISCHEMA.hasContent, contentId))
        # print(courdID_dict.get(TermLine['CourseId']))
        # graph.add((studentId, UNISCHEMA.enrolledInCourse,courdID_dict.get(TermLine['CourseId'])))
        graph.add((Record, UNISCHEMA.enrolledInTerm, Literal(str(TermLine['Term']))))
        graph.add((Record, DCTERMS.title, courdID_dict.get(TermLine['CourseId'])))
        graph.add((Record, UNISCHEMA.hasGot, Literal(str(TermLine['Grades']))))
        if TermLine['Grades'] != 'F':
            graph.add((studentId, DCTERMS.description, Literal(str(TermLine['Competencies']))))
        count+=1


# print(courdID_dict)
# To save graph in turtle Format
graph.serialize('Knowdlegde_base.ttl', format='turtle')
# To Save data in N-Triple format
graph.serialize('Knowdlegde_base.nt',format='nt')
