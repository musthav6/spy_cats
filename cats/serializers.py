# serializers.py

from rest_framework import serializers
from .models import SpyCat, Mission, Target, validate_cat_breed


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['name', 'country', 'notes', 'is_completed']

class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['spy_cat', 'targets', 'is_completed']

    def create(self, validated_data):
        print(validated_data)
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            target_data['mission'] = mission
            Target.objects.create(**target_data)
        return mission

    def update(self, instance, validated_data):
        targets_data = validated_data.pop('targets', None)
        instance.complete = validated_data.get('complete', instance.complete)
        instance.save()

        if targets_data:
            for target_data in targets_data:
                target, created = Target.objects.update_or_create(
                    name=target_data['name'],
                    defaults={**target_data, 'mission': instance}
                )
        return instance


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'experience_years', 'breed', 'salary']
