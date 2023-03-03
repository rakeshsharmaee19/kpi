from utils.models import KPIProject, KPIRating, KPI, Project, Sprint, AggregateRating, Workforce, Roles
from rest_framework import serializers


class KPIProjectSerializer(serializers.ModelSerializer):
    kpi_name = serializers.CharField(source='kpi_id.kpi_name')
    project_name = serializers.CharField(source='project_id.project_name')
    description = serializers.CharField(source='kpi_id.description')
    project_manager_id = serializers.IntegerField(source='project_id.project_manager_id_id')
    class Meta:
        model = KPIProject
        fields = ['project_id', 'weightage','kpi_id', 'kpi_name', 'project_name', 'description', 'project_manager_id']


class RatingSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project_id.project_name')
    kpi_name = serializers.CharField(source='kpi_id.kpi_name')
    description = serializers.CharField(source='kpi_id.description')
    project_manager_id = serializers.IntegerField(source='project_id.project_manager_id_id')
    weightage = serializers.SerializerMethodField()

    class Meta:
        model = KPIRating
        fields = ['emp_id', 'kpi_id', 'rating', 'project_id', 'reviewer_id', 'review_type', 'sprint_id','weightage',
                  'notes', 'project_name', 'kpi_name', 'description', 'project_manager_id']

    def get_weightage(self, obj):
        return obj.kpi_id.KPI_PROJECT_KPI_ID.get(project_id=obj.project_id).weightage


class PostRatingSerializer(serializers.ModelSerializer):
    weightage = serializers.FloatField()

    class Meta:
        model = KPIRating
        fields = ('kpi_id', 'rating', 'weightage', 'notes' )


class GetRatingSerializer(serializers.ModelSerializer):
    weightage = serializers.SerializerMethodField()
    kpi_name = serializers.CharField(source='kpi_id.kpi_name')

    class Meta:
        model = KPIRating
        fields = ['kpi_id', 'rating', 'weightage', 'notes', 'kpi_name' ]

    def get_weightage(self, obj):
        return obj.kpi_id.KPI_PROJECT_KPI_ID.get(project_id=obj.project_id).weightage


class NewRatingSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField()
    project_name = serializers.CharField(source='project_id.project_name')
    description = serializers.CharField(source='kpi_id.description')
    first_name = serializers.CharField(source='emp_id.emp_id.first_name')
    last_name = serializers.CharField(source='emp_id.emp_id.last_name')
    roleName = serializers.SerializerMethodField()

    class Meta:
        model = KPIRating
        fields = ['emp_id', 'project_id', 'reviewer_id', 'sprint_id', 'review_type', 'project_name',
                  'description', 'first_name', 'last_name','roleName', 'ratings']

    def get_ratings(self, obj: KPIRating):
        employee_ratings = KPIRating.objects.filter(emp_id=obj.emp_id, project_id=obj.project_id, reviewer_id=obj.reviewer_id, sprint_id=obj.sprint_id, review_type='self')
        serializer = GetRatingSerializer(employee_ratings, many=True)
        return serializer.data

    def get_roleName(self, obj: KPIRating):
        d = Workforce.objects.get(emp_id=obj.emp_id, project_id=obj.project_id).role_id
        roleData = Roles.objects.get(role_id=d).role
        return roleData


class PostKPIRatingSerializer(serializers.ModelSerializer):
    ratings = PostRatingSerializer(many=True)

    class Meta:
        model = KPIRating
        fields = ('emp_id', 'project_id', 'reviewer_id', 'sprint_id', 'ratings', 'review_type')

    def create(self, validated_data):
        ratings = validated_data.pop('ratings')

        rating_data = []
        aggregate_rating = 0
        for rating in ratings:
            aggregate_rating += round((rating['rating'] * rating['weightage']) / 100, 3)
            rating_data.append(
                KPIRating(
                    emp_id=validated_data['emp_id'],
                    project_id=validated_data['project_id'],
                    reviewer_id=validated_data['reviewer_id'],
                    sprint_id=validated_data['sprint_id'],
                    review_type=validated_data['review_type'],
                    kpi_id=rating['kpi_id'],
                    rating=rating['rating'],
                    notes=rating['notes']
                )
            )

        kpi_ratings = KPIRating.objects.bulk_create(rating_data)

        # Add data into aggregate rating table
        AggregateRating.objects.create(
            emp_id=validated_data['emp_id'],
            project_id=validated_data['project_id'],
            sprint_id=validated_data['sprint_id'],
            review_type=validated_data['review_type'],
            rating=round(aggregate_rating, 3)
        )
        return kpi_ratings

