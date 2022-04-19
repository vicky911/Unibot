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
    graph.add((contenId, RDF.type, DCTERMS.BibliographicResource))
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
contentDataCSV = pandas.read_csv('datasets/contentData.csv')
studentEnrolledDataCSV = pandas.read_csv('datasets/StudentEnrolled.csv')
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
        graph.add((courseId, UNISCHEMA.hasContent, contentId))

    # Student and Course Mapping

    if studentEnrolledDataCSV[studentEnrolledDataCSV['CourseId'] == courseLine['CourseId']].shape[0] != 0:
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
        graph.add((lectureId, UNISCHEMA.Topic, DBR[str(lectureLine['Topic'])]))
        graph.add((lectureId, RDFS.seeAlso, URIRef(lectureLine['seeAlso'])))
        graph.add((lectureId, DCTERMS.isPartOf, courseId))
        # Content Mapping with lecture
        lectureContentRecord = contentDataCSV[
            (contentDataCSV['CourseId'] == courseLine['CourseId']) & (contentDataCSV['Id'] == lectureLine['Id'])]
        for contentIndex in range(len(lectureContentRecord)):
            studentEnrolledLine = lectureContentRecord.iloc[contentIndex]
            contentId = addData(studentEnrolledLine["Content"], studentEnrolledLine["ContentType"])
            graph.add((lectureId, UNISCHEMA.hasContent, contentId))

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

    studentEnrolledRecord = studentEnrolledDataCSV[(studentEnrolledDataCSV['IDNumber'] == studentLine['IDNumber'])]

    for studentEnrolledIndex in range(len(studentEnrolledRecord)):
        studentEnrolledLine = studentEnrolledRecord.iloc[studentEnrolledIndex]
        # studentEnrolledId = addData(studentEnrolledLine["Content"], studentEnrolledLine["ContentType"])
        # graph.add((studentId, UNISCHEMA.hasContent, contentId))

        graph.add((studentId, UNISCHEMA.enrolledIn,courdID_dict.get(studentEnrolledLine['CourseId'])))
        graph.add((studentId, DCTERMS.title, Literal(str( studentEnrolledLine['CourseId']))))
        graph.add((studentId, UNISCHEMA.hasGot, Literal(str(studentEnrolledLine['Grades']))))
        if studentEnrolledLine['Grades'] != 'F':
            graph.add((studentId, DCTERMS.description, Literal(str(studentEnrolledLine['Competencies']))))

# print(courdID_dict)
# To save graph in turtle Format
graph.serialize('Knowdlegde_base123.ttl', format='turtle')
# To Save data in N-Triple format
graph.serialize('Knowdlegde_base123.nt',format='nt')
