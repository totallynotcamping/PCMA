import os
from openai import AzureOpenAI
from unstructured.partition.auto import partition
from core.config import settings
from sqlalchemy.orm import Session
from app.crud import crud_consultant
from app.schemas.consultant import SkillCreate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeAgent:
    def __init__(self, db: Session):
        self.db = db
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_ACCESS_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_API_BASE,
        )

    def extract_skills_from_resume(self, file_path: str, consultant_id: int):
        try:
            # 1. Parse resume using unstructured.io
            elements = partition(filename=file_path, unstructured_api_key=settings.UNSTRUCTURED_API_KEY, unstructured_api_url=settings.UNSTRUCTURED_BASE_URL)
            resume_text = "\n".join([str(el) for el in elements])
            
            # 2. Extract skills using Azure OpenAI
            prompt = f"""
            From the following resume text, extract the top 5-7 most relevant technical and soft skills.
            Return the skills as a comma-separated list.
            
            Resume:
            {resume_text}
            
            Skills:
            """
            
            response = self.client.completions.create(
                model=settings.AZURE_OPENAI_MODEL_ID,
                prompt=prompt,
                max_tokens=50,
                temperature=0.2,
            )
            
            extracted_skills_str = response.choices[0].text.strip()
            skills_list = [skill.strip() for skill in extracted_skills_str.split(',') if skill.strip()]

            # 3. Add skills to consultant's profile in DB
            for skill_name in skills_list:
                skill = SkillCreate(name=skill_name)
                crud_consultant.add_skill_to_consultant(self.db, consultant_id=consultant_id, skill=skill)
            
            logger.info(f"Successfully extracted and updated skills for consultant {consultant_id}")
            return skills_list

        except Exception as e:
            logger.error(f"Error processing resume for consultant {consultant_id}: {e}")
            return None 