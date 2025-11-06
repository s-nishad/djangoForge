from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Document, ParsingStatus, QueryLog, QueryLog
from .serializers import DocumentSerializer, QueryLogSerializer
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .utils import parse_document
from .vector_db import save_to_vector_db, query_vector_db

from .summarizer import summarize_document
from .rag_llm import generate_answer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-created_at')
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        document = serializer.save()

        try:
            # Parse file or manual content
            if document.file:
                document.parse_content_status = ParsingStatus.IN_PROGRESS
                document.save(update_fields=['parse_content_status'])

                content = parse_document(document.file.path)
                if not content.strip():
                    raise ValueError("Parsed content is empty.")

            elif document.parse_content:
                content = document.parse_content
                document.parse_content_status = ParsingStatus.MANUAL
                document.save(update_fields=['parse_content_status'])

            else:
                raise ValueError("No content provided or parsed.")

            # Summarize and detect language
            language, summary_text = summarize_document(content)

            # Save parsed content, language, and summary
            document.parse_content = content
            document.language = language
            document.document_summary = summary_text
            document.parse_content_status = ParsingStatus.COMPLETED
            document.save(update_fields=['parse_content', 'language', 'document_summary', 'parse_content_status'])

            # Save to vector DB with enriched metadata
            save_to_vector_db(
                content,
                metadata={
                    "document_id": document.id,
                    "title": document.title,
                    "language": language,
                    "summary": summary_text
                }
            )

        except Exception as e:
            document.parse_content_status = ParsingStatus.FAILED
            document.save(update_fields=['parse_content_status'])
            raise e


    @action(detail=False, methods=['get'])
    def query(self, request):
        """Search vector DB for semantic matches."""
        query = request.query_params.get("q")
        if not query:
            return Response({"error": "Missing 'q' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            results = query_vector_db(query, top_k=3)
            data = [{"text": r.page_content, "metadata": r.metadata} for r in results]
            return Response({"results": data})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DocumentQueryAPIView(APIView):
    """
    Given a document ID and a query string,
    search semantically within the document content.
    """

    def post(self, request, *args, **kwargs):
        document_id = request.data.get("document_id")
        query = request.data.get("query")

        if not document_id or not query:
            return Response(
                {"error": "Both 'document_id' and 'query' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch document object
        doc = get_object_or_404(Document, id=document_id)

        # Perform RAG-like semantic search
        try:
            results = query_vector_db(query, top_k=3)
            
            relevant_chunks = [
                r.page_content
                for r in results
                if str(r.metadata.get("document_id")) == str(document_id)
            ]

            # combine relevant chunks into a single context string
            combined_context = " ".join(relevant_chunks)

            # if no relevant chunks found include full document content
            if not combined_context:
                combined_context = (doc.parse_content[:5000] + "...") if doc.parse_content else "No relevant content found for your query."

            query_log = QueryLog.objects.create(
                user=request.user,
                document=doc,
                query_text=query,
                response_text=combined_context,
                metadata={
                    "source": "vector_db",
                    "num_chunks": len(relevant_chunks),
                }
            )

            # combined_context = generate_answer(combined_context, query)

            # Now you can call OpenAI with query + combined_context
            # For example:
            # answer = openai.Completion.create(
            #     model="gpt-4",
            #     prompt=f"Context: {combined_context}\n\nQuestion: {query}\nAnswer:",
            #     max_tokens=500
            # )

            return Response({"context": combined_context}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentQueryHistoryAPIView(generics.ListAPIView):
    """
    Returns chat history for a given document for the logged-in user.
    """
    serializer_class = QueryLogSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "document_id"

    def get_queryset(self):
        document_id = self.request.query_params.get("document_id")
        document = get_object_or_404(Document, id=document_id, user=self.request.user)
        if not document_id:
            return QueryLog.objects.none()
        return QueryLog.objects.filter(
            user=self.request.user,
            document=document
        ).order_by("created_at")  # chronological order