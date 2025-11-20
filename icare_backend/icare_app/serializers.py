from rest_framework import serializers
from .models import Registration, Showcase, LoginHistory, Demonstration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ['id', 'username', 'login_time', 'ip_address', 'user_agent', 'status']

from rest_framework import serializers
from .models import Showcase

class ShowcaseSerializer(serializers.ModelSerializer):
    media_file = serializers.FileField(required=False)  # <-- IMPORTANT
    media_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Showcase
        fields = [
            'id', 'title', 'description', 'media_type',
            'media_file', 'media_file_url', 'website_url', 'created_at'
        ]

    # --- Return correct URL for frontend ---
    def get_media_file_url(self, obj):
        request = self.context.get('request')

        if obj.media_type == 'image' and obj.media_file:
            if request:
                return request.build_absolute_uri(obj.media_file.url)
            return obj.media_file.url

        if obj.media_type == 'video':
            return obj.website_url

        return None

    # --- Validation ---
    def validate(self, data):
        media_type = data.get('media_type', 'image')
        media_file = data.get('media_file')
        website_url = data.get('website_url')

        # CREATE
        if self.instance is None:
            if media_type == 'image' and not media_file:
                raise serializers.ValidationError({
                    "media_file": "Image file is required for image type"
                })

            if media_type == 'video' and not website_url:
                raise serializers.ValidationError({
                    "website_url": "Video URL is required for video type"
                })

        return data

# NEW SERIALIZER FOR DEMONSTRATION
class DemonstrationSerializer(serializers.ModelSerializer):
    media_file = serializers.SerializerMethodField()

    class Meta:
        model = Demonstration
        fields = ['id', 'title', 'description', 'media_type', 'media_file', 'website_url', 'created_at']

    def get_media_file(self, obj):
        request = self.context.get('request')
        
        if obj.media_type == 'image' and obj.media_file:
            if request:
                return request.build_absolute_uri(obj.media_file.url)
            else:
                return obj.media_file.url
        elif obj.media_type == 'video':
            return obj.website_url
        
        return None

    def validate(self, data):
        media_type = data.get('media_type', 'image')
        media_file = data.get('media_file')
        website_url = data.get('website_url')

        if self.instance is None:
            if media_type == 'image' and not media_file:
                raise serializers.ValidationError({
                    "media_file": "Image file is required for image type"
                })

            if media_type == 'video' and not website_url:
                raise serializers.ValidationError({
                    "website_url": "Video URL is required for video type"
                })

        return data