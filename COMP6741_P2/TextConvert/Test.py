import os
import pandas as pd
import spacy
import en_core_web_sm

def generate_topics(courseID,type, lectureID, filePath):
    if(count>=2):
        return
    file = open(filePath, 'r', encoding="UTF-8")
    text = file.read()
    try:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        for token in doc:
            if token.text!=None or token.text!=' ':
                # print("-----")
                # print(token.text)
                spacyDic[token.text]=(token.ent_type_, token.head.pos_)
                # print(spacyDic)
                # print('********')
            # spacyDic[token.ent_type] = token.ent_type
            # spacyDic[token.ent_type]=token.head.pos_


        # print(spacyDic)


        nlp = spacy.blank('en')
        nlp.add_pipe('dbpedia_spotlight')
        doc=nlp(text)
        # print('Entities', [(ent.text, ent.label_, ent.kb_id_) for ent in doc.ents])
        for ent in doc.ents:
            if ent.kb_id_ not in dbDic.values():
                dbDic[ent.text] = ent.kb_id_
                # print(ent.text, ent.label_)

        # print(dbDic)
        # print(len(dbDic))
        # print(len(spacyDic))

        if(len(dbDic)<=len(spacyDic)):
            for str in dbDic:
                # print(str)
                if str in spacyDic:
                    # get topic name, entity type and dbpedia link
                    # print(str,maxDic[str],minDic[str])
                    dup['CourseId'].append(courseID)
                    dup['Type'].append(type)
                    dup['Identifier'].append(lectureID)
                    dup['Topic Name'].append(str)
                    dup['Topic Link'].append(dbDic.get(str))
                    dup['Entity Type'].append(spacyDic.get(str)[0])
                    dup['POS'].append(spacyDic.get(str)[1])

        else:
            for str in spacyDic:
                # print(str)
                if str in dbDic:
                    # get topic name, entity type and dbpedia link
                    # print(str,maxDic[str],minDic[str])
                    dup['CourseId'].append(courseID)
                    dup['Type'].append(type)
                    dup['Identifier'].append(lectureID)
                    dup['Topic Name'].append(str)
                    dup['Topic Link'].append(dbDic.get(str))
                    dup['Entity Type'].append(spacyDic.get(str)[0])
                    dup['POS'].append(spacyDic.get(str)[1])

        # print(len(minDic))



            # if ent.label_ in pattern:
            # print(ent.label_)
            # if ent.kb_id_ not in dup['Topic Link']:
            #     dup['Course ID'].append(courseID)
            #     dup['Type'].append(type)
            #     dup['Lecture ID'].append(lectureID)
            #     dup['Topic Name'].append(ent.text)
            #     dup['Topic Link'].append(ent.kb_id_)

        # print(len(doc.ents))
    except IOError:
        print("Could not read file:", file)
    file.close()

if __name__ == "__main__":
    path = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\datasets\\"
    IS_worksheet_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6741\worksheet"
    IS_lecture_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6741\lecture"
    IS_lab_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6741\Labs"
    AI_worksheet_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6721\worksheet"
    AI_lecture_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6721\lecture"
    AI_lab_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6721\Labs"
    dup = {
        'CourseId': [],
        'Type': [],
        'Identifier': [],
        'Topic Name': [],
        'Topic Link': [],
        'Entity Type': [],
        'POS':[]
    }
    spacyDic = {}
    dbDic={}

    pattern=["ORG","MONEY","PERSON","WORK OF ART","LANGUAGE","EVENT","TYPE"]

    count = 1
    for txtfile in os.listdir(IS_lecture_directory):
        print(str(txtfile))
        generate_topics('40355', 'Slide', count, IS_lecture_directory + '\\' + txtfile)
        count = count + 1

    print(dup)
    # count = 1
    # for txtfile in os.listdir(IS_worksheet_directory):
    #     print(str(txtfile))
    #     generate_topics('40355', 'WorkSheet', count, IS_worksheet_directory + '\\' + txtfile)
    #     count = count + 1
    #
    # count = 1
    # for txtfile in os.listdir(IS_lab_directory):
    #     print(str(txtfile))
    #     generate_topics('40355', 'Lab', count, IS_lab_directory + '\\' + txtfile)
    #     count = count + 1
    #
    # count = 1
    # for txtfile in os.listdir(AI_lecture_directory):
    #     print(str(txtfile))
    #     generate_topics('40353', 'Slide', count, AI_lecture_directory + '\\' + txtfile)
    #     count = count + 1
    #
    # count = 1
    # for txtfile in os.listdir(AI_worksheet_directory):
    #     print(str(txtfile))
    #     generate_topics('40353', 'Worksheet', count, AI_worksheet_directory + '\\' + txtfile)
    #     count = count + 1
    #
    # count = 1
    # for txtfile in os.listdir(AI_lab_directory):
    #     print(str(txtfile))
    #     generate_topics('40353', 'Lab', count, AI_lab_directory + '\\' + txtfile)
    #     count = count + 1

    # df = pd.DataFrame(dup)
    # df.to_csv(path+'Topics1.csv', index=False)
    # dd=pd.DataFrame.from_dict(dbDic,orient="index")
    # dd.to_csv(path+'temp.csv')
