# import spacy
# import spacy_dbpedia_spotlight
# import en_core_web_sm
# # load your model as usual
# nlp = spacy.blank('en')
# # add the pipeline stage
# nlp.add_pipe('dbpedia_spotlight')
# # nlp.get_pipe('dbpedia_spotlight')
# # print(nlp.get_pipe_config('dbpedia_spotlight'))
# # print(nlp.pipe_names)
# # get the document
# doc = nlp('The president of USA is calling Boris Johnson to decide what to do about coronavirus')
# # see the entities
# lst={}
# for ent in doc.ents:
#     # print('Entities', (ent.text, ent.kb_id_ ))
#     lst[ent.text] = ent.kb_id_
# print(lst)
# nlp = spacy.load('en_core_web_sm')
# doc = nlp('The president of USA is calling Boris Johnson to decide what to do about coronavirus')
# st={}
# for ent in doc.ents:
#     # print('Entities', (ent.text, ent.label_,ent.kb_id_ ))
#     st[ent.text] = ent.label_
#
# print(st)
#
#
# # inspect the raw data from DBpedia spotlight
# # print(doc.ents[0]._.dbpedia_raw_result)

import spacy
import en_core_web_sm
# load your model as usual
nlp = spacy.load('en_core_web_sm')
# add the pipeline stage
# nlp.add_pipe('dbpedia_spotlight')
# get the document
doc = nlp('The president of USA is calling Boris Johnson to decide what to do about coronavirus')
# see the entities
print('Entities', [(ent.text, ent.label_, ent.kb_id_) for ent in doc.ents])
# inspect the raw data from DBpedia spotlight
print(doc.ents[0]._.dbpedia_raw_result)