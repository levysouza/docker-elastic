from PyPDF2 import PdfReader

def extract_pdf(file):
    reader = PdfReader(file.file)
    raw_text_pdf = ''
    for page in reader.pages:
      
      raw_text_pdf += '\n'
      
      raw_text_pdf += page.extract_text()

    return raw_text_pdf


def index_payload(data):

    for i, row in data.iterrows():
        
        process_id = str(row['processo'])
        process_file = str(row['arquivo'])
        cod_subject = str(row['codigos_assunto'])
        cod_classs = (row['classe_processual'])
        decision_file = str(row['decisao'])
        text_petition = str(row['raw_peticao'])
        clean_text_petition = str(row['peticao_clean_text'])
        cod_judge = row['magistrado']

        yield {
            "_index": "index-tj-matching",
            "_source": {
                "process_id": process_id,
                "process_file": process_file,
                "cod_subject": cod_subject,
                "cod_classs": cod_classs,
                "decision_file": decision_file,
                "text_petition": text_petition,
                "clean_text_petition":clean_text_petition,
                "cod_judge": cod_judge
            }
        }     
