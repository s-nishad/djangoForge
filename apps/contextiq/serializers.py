from rest_framework import serializers
from .models import Document, QueryLog

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'file',
            'parse_content',
            'parse_content_status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'parse_content_status', 'created_at', 'updated_at']

    def validate(self, data):
        """Require at least one of file or parse_content."""
        file = data.get('file')
        parse_content = data.get('parse_content')

        if not file and not parse_content:
            raise serializers.ValidationError(
                "Either a file must be uploaded or 'parse_content' must be provided."
            )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        document = Document(**validated_data)
        document.user = user
        document.save()
        return document
    

class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = ['id', 'query_text', 'response_text', 'metadata', 'created_at', 'updated_at']