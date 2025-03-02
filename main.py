# command = 'python install_packages.py'
# os.system(command)
from typing import List
from langchain_utilites import generate_response
from db_utilities import get_chat_history,insert_application_logs,get_all_documents
from pydantic import BaseModel
from chroma_utils import index_document_to_Chroma
import uuid
from fastapi import FastAPI, UploadFile, File,HTTPException
app=FastAPI()
import os




class query_input(BaseModel):
    question:str
    course_outcomes:str=None
    session_id: str = None
    model:str = "llama-3.3-70b-versatile"
class QueryResponse(BaseModel):
    response: str
    session_id: str
    model_name:str

@app.post("/chat", response_model=QueryResponse)
async def chat(query_input:query_input):
    if(not query_input.session_id):
        query_input.session_id = str(uuid.uuid4())
    chat_history =get_chat_history(query_input.session_id)
    response = generate_response(query_input.question, query_input.course_outcomes, chat_history)
    insert_application_logs(query_input.session_id, query_input.question, response, query_input.model)

    return QueryResponse(response=response, session_id=query_input.session_id, model_name=query_input.model)


@app.post("/uploadfile")
# def file_contents(files: UploadFile = File(...)):
#     return {"uploaded_files": files.filename}
async def create_upload_file( file: UploadFile = File(...)):
    # return {"filename": file.filename}
      try:
      #
              file_path = f"C://Users//Ruchitesh//Desktop//Rag_based_question_paper_generator//venv//papers//{file.filename}"
              with open(file_path, "wb") as f:
                    f.write(file.file.read())
              success = index_document_to_Chroma()

              if(success):

                     return {"message": "File saved successfully"}
              else:
                raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
     #
      except Exception as e:
         return {"message": e.args}



