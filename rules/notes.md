

md file(s) -> doc_section -> doc_publish -> doc_stage

doc_publish will gather the markdown files and preprocess them as necessary for jekkyl or pdf. The user can run doc_publish to get a visualisation of the docs for these specific sections at localhost

doc_stage takes all the doc_publish and compiles the repo docs for jekkyl or pdf. If you run doc_stage, all doc_publish targets are built. Their outputs are copied into some other overarching repo doc structure and they are copied to the docs folder (which is publish on GitHub pages). To update GitHub pages, you need to run the doc_stage target. 