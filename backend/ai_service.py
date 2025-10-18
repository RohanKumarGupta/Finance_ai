from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from models import DocumentAnalysis
from config import settings
import logging
import json

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.llm = None
        if settings.gemini_api_key:
            try:
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-pro-2.5",
                    google_api_key=settings.gemini_api_key,
                    temperature=0.3
                )
                logger.info("Gemini AI service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini AI: {e}")
        else:
            logger.warning("Gemini API key not provided")

    async def analyze_financial_document(self, content: str, document_type: str) -> DocumentAnalysis:
        """Analyze financial document using Gemini AI"""
        if not self.llm:
            return self._get_default_analysis(document_type)
        
        try:
            system_prompt = """You are a financial advisor AI assistant specialized in analyzing educational financial documents. 
            Your task is to analyze the provided document and extract key financial information.
            
            Please provide a JSON response with the following structure:
            {
                "document_type": "identified document type",
                "summary": "brief summary of the document",
                "key_findings": ["finding1", "finding2", "finding3"],
                "recommendations": ["recommendation1", "recommendation2"],
                "confidence_score": 0.85
            }
            
            Focus on:
            - Tuition fees, hostel fees, transport fees
            - Payment due dates
            - Scholarship information
            - Payment methods and policies
            - Any penalties or late fees
            """
            
            human_prompt = f"""
            Document Type: {document_type}
            Document Content: {content}
            
            Please analyze this financial document and provide insights.
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            # Try to parse JSON response
            try:
                analysis_data = json.loads(response.content)
                return DocumentAnalysis(**analysis_data)
            except json.JSONDecodeError:
                # If JSON parsing fails, create analysis from text response
                return self._parse_text_response(response.content, document_type)
                
        except Exception as e:
            logger.error(f"Error analyzing document: {e}")
            return self._get_default_analysis(document_type)

    def _parse_text_response(self, response_text: str, document_type: str) -> DocumentAnalysis:
        """Parse text response when JSON parsing fails"""
        return DocumentAnalysis(
            document_type=document_type,
            summary=response_text[:200] + "..." if len(response_text) > 200 else response_text,
            key_findings=["Document analyzed successfully", "Financial information extracted"],
            recommendations=["Review payment due dates", "Consider payment plan options"],
            confidence_score=0.7
        )

    def _get_default_analysis(self, document_type: str) -> DocumentAnalysis:
        """Return default analysis when AI service is not available"""
        return DocumentAnalysis(
            document_type=document_type,
            summary="Document received and processed. AI analysis not available due to missing API key.",
            key_findings=["Document uploaded successfully", "Manual review recommended"],
            recommendations=["Please review the document manually", "Contact support for assistance"],
            confidence_score=0.5
        )

    async def generate_financial_advice(self, parent_data: dict, student_data: dict, payment_history: list) -> str:
        """Generate personalized financial advice"""
        if not self.llm:
            return "Financial advice generation requires AI service configuration."
        
        try:
            system_prompt = """You are a financial advisor AI assistant helping parents manage their children's educational expenses. 
            Provide personalized, practical financial advice based on the parent's financial situation and payment history."""
            
            human_prompt = f"""
            Parent Information:
            - Name: {parent_data.get('name', 'N/A')}
            - Email: {parent_data.get('email', 'N/A')}
            
            Student Information:
            - Name: {student_data.get('name', 'N/A')}
            - Class: {student_data.get('class_name', 'N/A')}
            
            Recent Payment History:
            {json.dumps(payment_history, indent=2)}
            
            Please provide personalized financial advice for managing educational expenses.
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating financial advice: {e}")
            return "Unable to generate financial advice at this time. Please try again later."

    async def generate_receipt_summary(self, receipts_data: str, user_prompt: str) -> str:
        """Generate AI-powered summary of receipts based on user prompt"""
        if not self.llm:
            return "Receipt summarization requires AI service configuration."

        try:
            system_prompt = """You are a financial assistant AI specialized in analyzing payment receipts and providing insights based on user queries.

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
            """

            human_prompt = f"""
            Payment Receipts Data:
            {receipts_data}

            User Query: {user_prompt}

            Please analyze the receipts and provide a comprehensive response to the user's query.
            """

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]

            response = await self.llm.ainvoke(messages)
            return response.content

        except Exception as e:
            logger.error(f"Error generating receipt summary: {e}")
            return "Unable to generate receipt summary at this time. Please try again later."

