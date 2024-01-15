from django.shortcuts import render
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .utils import handle_uploaded_file
from . import ensamble_pipeline, ranker


@api_view(['GET', 'POST'])
def song_list(request):
    if request.method == 'GET':
        data = Song.objects.all()
        serializer = SongSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print('post')
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def song_detail(request, pk):
    try:
        student = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = SongSerializer(student, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def prompt_prediction(request):
    data = request.POST
    upload_path = None
    if request.FILES:
        uploaded_file = request.FILES["image"]
        extension = uploaded_file.name.split(".")[-1]
        if extension not in ['jpag', 'jpg', 'png']:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "File should be an image."})

        upload_path = handle_uploaded_file(uploaded_file)

    act_preds, dress_code_preds = ensamble_pipeline(upload_path)
    print(act_preds)
    print(dress_code_preds)
    reco_df = ranker.rank(data["text"], act_preds, dress_code_preds)

    data = []
    for index, row in reco_df.iterrows():
        if not pd.isna(row['yt_id']):
            link = f"https://music.yandex.ru/track/{int(row['yt_id'])}"
        else:
            link = None
        data.append({
            "title": row["title"],
            "artist": row["artists"],
            "link": link
        })
    return Response(status=status.HTTP_201_CREATED, data=data)