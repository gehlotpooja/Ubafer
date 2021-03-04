from .controllers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def conference_details(request):
    ret_dict = {
        'status': 'Error',
        'msg': 'Error in getting the Talk details. Please try again.',
        'data': {}
    }
    try:
        output_file = open("E:/virtualenvs/ubafer/ubafer_app/output.txt", "w")
        lines = request.data.get("test_input")
        res_list = get_track_wise_talk_details(lines, output_file)
        output_file.close()
        if res_list:
            ret_dict = {
                'status': 'Success',
                'msg': "Data sorted successfully,check output.txt file",
                'data': res_list
            }
        return Response(data=ret_dict, status=status.HTTP_200_OK)
    except Exception as e:
        print(e.args)
        return Response(data=ret_dict, status=status.HTTP_404_NOT_FOUND)







