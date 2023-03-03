from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.models import KPIProject, AggregateRating, Sprint, KPIRating, Workforce
from .serializers import KPIProjectSerializer, RatingSerializer, PostKPIRatingSerializer, NewRatingSerializer
import utils.utils as util


class SelfRating(APIView):
    def getProjectKPI(self, project_id):
        try:
            kpiData = KPIProject.objects.filter(project_id_id=project_id)
            return kpiData
        except:
            raise Http404

    def getSelfRatingFlag(self, project_id, sprint_id, emp_id):
        try:
            data = KPIRating.objects.filter(project_id_id=project_id, sprint_id_id=sprint_id, emp_id_id=emp_id)
            return data
        except:
            return None

    def get(self, request, project_id, sprint_id, emp_id):
        kpiData = self.getProjectKPI(project_id)
        serializerKPIProject = KPIProjectSerializer(kpiData, many=True)
        if serializerKPIProject.data:
            data = util.serialize(serializerKPIProject.data, True, 'Returning projects KPIs', status.HTTP_200_OK)
            return Response(data)
        else:
            data = util.serialize(None, False, 'No Project KPIs are there or Project is not define', status.HTTP_400_BAD_REQUEST)
            return Response(data)

    def post(self, request, project_id, sprint_id, emp_id):
        ratingActiveData = self.getSelfRatingFlag(project_id, sprint_id,emp_id)
        if ratingActiveData:
            data = util.serialize(None, False, 'Can not  rate, assessment already done', status.HTTP_401_UNAUTHORIZED)
            return Response(data)
        else:
            data = request.data
            data['review_type'] = 'self'
            serializer = PostKPIRatingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data = util.serialize(None, True, 'Self Rating has created', status.HTTP_201_CREATED)
                return Response(data)
            data = util.serialize(None, False, 'Fields Value are not correct', status.HTTP_201_CREATED)
            return Response(data)


class EmployeeRating(APIView):
    def getSelfRatingFlag(self, project_id, sprint_id, emp_id, review_type='self'):
        try:
            data = KPIRating.objects.filter(project_id_id=project_id, sprint_id_id=sprint_id, emp_id_id=emp_id, review_type=review_type)
            return data
        except:
            return None

    def checkAllEmployeeRated(self, project_id, sprint_id):
        returnData = True
        try:
            emp_list = Workforce.objects.filter(project_id_id=project_id, is_deleted=False)
            for i in emp_list:
                dataManager = KPIRating.objects.filter(project_id_id=project_id, sprint_id_id=sprint_id, emp_id_id=i.emp_id_id,
                                               review_type='review')
                if dataManager:
                    continue
                else:
                    returnData = False
                    break
        except:
            raise Http404
        return returnData

    def get(self, request, emp_id, project_id, sprint_id):
        ratingActiveData = self.getSelfRatingFlag(project_id, sprint_id, emp_id)
        if ratingActiveData:
            ratingReviewerData = self.getSelfRatingFlag(project_id, sprint_id, emp_id, 'review')
            if ratingReviewerData:
                data = util.serialize(None, False, 'Can not  rate, already assessed',
                                      status.HTTP_401_UNAUTHORIZED)
                return Response(data)
            else:
                serializerRating = RatingSerializer(ratingActiveData, many=True)
                data = util.serialize(serializerRating.data, True, 'Returning Employee notes, Rating of every KPI', status.HTTP_200_OK)
                return Response(data)
        else:
            data = util.serialize(None, False, 'Employee Have not assessed himself', status.HTTP_400_BAD_REQUEST)
            return Response(data)


    def post(self, request, project_id, sprint_id, emp_id):
        ratingActiveData = self.getSelfRatingFlag(project_id, sprint_id,emp_id)
        if not ratingActiveData:
            data = util.serialize(None, False, 'Can not  rate, assessment already done', status.HTTP_401_UNAUTHORIZED)
            return Response(data)
        else:
            data = request.data
            data['review_type'] = 'review'
            serializer = PostKPIRatingSerializer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = util.serialize(None, True,'Rating have saved successfully', status.HTTP_201_CREATED)
                    if self.checkAllEmployeeRated(project_id, sprint_id):
                        data = Sprint.objects.get(project_id_id=project_id, sprint_id=sprint_id)
                        data.is_completed = True
                        data.save()
                    return Response(data)
                except:
                    raise Http404
            data = util.serialize(None, False, 'Fields value are incorrect', status.HTTP_401_UNAUTHORIZED)
            return Response(data)


class RateMultiple(APIView):
    def getSelfRatingFlag(self,sprint_id, project_id):
        returnData=[]
        try:
            emp_list = Workforce.objects.filter(project_id_id=project_id, is_deleted=False)
            for i in emp_list:
                dataSelf = KPIRating.objects.filter(project_id_id=project_id, sprint_id_id=sprint_id, emp_id_id=i.emp_id_id, review_type='self')
                dataManager = KPIRating.objects.filter(project_id_id=project_id, sprint_id_id=sprint_id, emp_id_id=i.emp_id, review_type='review')
                if dataSelf and dataManager:
                    continue
                elif dataManager:
                    continue
                elif dataSelf:
                    returnData.append(dataSelf)
            return returnData
        except:
            raise Http404

    def checkAllEmployeeRated(self, project_id, sprint_id):
        returnData = True
        try:
            emp_list = Workforce.objects.filter(project_id_id=project_id, is_deleted=False)
            for i in emp_list:
                dataManager = KPIRating.objects.filter(project_id_id=project_id, sprint_id_id=sprint_id, emp_id_id=i.emp_id_id,
                                               review_type='review')
                if dataManager:
                    continue
                else:
                    returnData = False
                    break
        except:
            raise Http404
        return returnData

    def get(self, request, sprint_id, project_id):
        selfAssesData = self.getSelfRatingFlag(sprint_id, project_id)
        if selfAssesData:
            returnData = []
            for i in selfAssesData:
                serializerRating = NewRatingSerializer(i[0])
                returnData.append(serializerRating.data)
            data = util.serialize(returnData, True, 'Returning left Employee notes, Rating of every KPI',
                                  status.HTTP_200_OK)
            return Response(data)
        else:
            data = util.serialize(None, False, 'Can not  rate, either all employee are rated or no one have fill self asses',
                                  status.HTTP_401_UNAUTHORIZED)
            return Response(data)

    def post(self, request, project_id, sprint_id):
        ratingActiveData = self.getSelfRatingFlag(project_id=project_id, sprint_id=sprint_id)
        if not ratingActiveData:
            data = util.serialize(None, False, 'Can not  rate, assessment already done', status.HTTP_401_UNAUTHORIZED)
            return Response(data)
        else:
            data = request.data
            for item in data:
                item['review_type'] = 'review'
            serializer = PostKPIRatingSerializer(data=data, many=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                    data = util.serialize(None, True, 'Rating has saved', status.HTTP_201_CREATED)
                    if self.checkAllEmployeeRated(project_id, sprint_id):
                        dataSprint = Sprint.objects.get(project_id_id=project_id, sprint_id=sprint_id)
                        dataSprint.is_completed = True
                        dataSprint.save()
                    return Response(data)
                except:
                    raise Http404
            data = util.serialize(None, False, 'Fields value are incorrect', status.HTTP_401_UNAUTHORIZED)
            return Response(data)

