import google.generativeai as genai
from ..config import settings
import asyncio
from functools import partial
from fastapi import UploadFile
import tempfile
import os

class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY not configured")
        # Configure the Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use gemini-2.5-flash - newer stable model that's confirmed available
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    async def summarize_document(self, text: str) -> str:
        prompt = f"""
You are a helpful assistant for parents. Summarize the following financial document focusing on:
- Tuition, hostel, transport charges
- Scholarships or waivers
- Important due dates and action items

Document:
{text}
"""
        # Use sync API with asyncio to avoid v1beta issues
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            partial(self.model.generate_content, prompt)
        )
        return response.text

    async def summarize_file(self, file: UploadFile) -> str:
        """Summarize a financial document from an uploaded file (PDF, image, etc.)"""
        # Read file content
        content = await file.read()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            # Upload file to Gemini
            loop = asyncio.get_event_loop()
            uploaded_file = await loop.run_in_executor(
                None,
                partial(genai.upload_file, tmp_path, display_name=file.filename)
            )
            
            prompt = """
You are a helpful assistant for parents. Analyze this financial document and provide a clear summary focusing on:
- Tuition, hostel, transport charges
- Scholarships or waivers
- Important due dates and action items
- Total amounts due

Please be specific with numbers and dates.
"""
            
            # Generate content with the uploaded file
            response = await loop.run_in_executor(
                None,
                partial(self.model.generate_content, [prompt, uploaded_file])
            )
            
            # Clean up uploaded file from Gemini
            await loop.run_in_executor(None, uploaded_file.delete)
            
            return response.text
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    async def financial_advice(self, student_name: str, breakdown: dict, history: list[dict]) -> str:
        prompt = f"""
Given a student's fee breakdown and past payment history, provide concise, personalized planning advice for a parent.
Be practical and mention opportunities to optimize, including the impact of scholarships.

Student: {student_name}
Fee Breakdown: {breakdown}
Payment History (latest first): {history}
"""
        # Use sync API with asyncio to avoid v1beta issues
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            partial(self.model.generate_content, prompt)
        )
        return response.text

    async def generate_receipt_summary(self, receipts_data: str, user_prompt: str) -> str:
        """Generate AI-powered summary of receipts based on user prompt"""
        prompt = f"""
You are a financial assistant AI specialized in analyzing payment receipts and providing insights based on user queries.

You have access to a collection of payment receipts with the following information for each receipt:
- receipt_id: Unique receipt identifier
- payment_id: Payment transaction ID
- student_name: Name of the student
- student_class: Class/grade of the student
- amount: Payment amount in rupees
- category: Payment category (tuition, hostel, transport, etc.)
- paid_at: Date and time of payment

Your task is to analyze these receipts and provide meaningful summaries, insights, and answers based on the user's specific prompt.

Always provide:
1. A clear, concise answer to the user's query
2. Relevant statistics and calculations when applicable
3. Organized, easy-to-read formatting
4. Actionable insights when relevant

If the user asks for specific calculations (totals, averages, trends), perform them accurately.
If the user asks for trends or patterns, identify them clearly.

Payment Receipts Data:
{receipts_data}

User Query: {user_prompt}

Please analyze the receipts and provide a comprehensive response to the user's query.
"""
        # Use sync API with asyncio to avoid v1beta issues
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            partial(self.model.generate_content, prompt)
        )
        return response.text
