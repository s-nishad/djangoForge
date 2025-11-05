from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Document, ParsingStatus
from .serializers import DocumentSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .utils import parse_document
from .vector_db import save_to_vector_db, query_vector_db

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-created_at')
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        # Don't pass user here; serializer already sets it
        document = serializer.save()

        try:
            # If file uploaded → parse content
            if document.file:
                document.parse_content_status = ParsingStatus.IN_PROGRESS
                document.save(update_fields=['parse_content_status'])

                content = parse_document(document.file.path)
                
                if not content.strip():
                    raise ValueError("Parsed content is empty from the uploaded file.")

                document.parse_content = content
                document.parse_content_status = ParsingStatus.COMPLETED
                document.save()

                save_to_vector_db(
                    content,
                    metadata={"document_id": document.id, "title": document.title}
                )

            # If content was provided manually
            elif document.parse_content:
                document.parse_content_status = ParsingStatus.MANUAL
                document.save()
                save_to_vector_db(
                    document.parse_content,
                    metadata={"document_id": document.id, "title": document.title}
                )

            else:
                # This should never happen due to serializer validation
                raise ValueError("No content provided or parsed.")

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


            return Response({"context": combined_context}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)