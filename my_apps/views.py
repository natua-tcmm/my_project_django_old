from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q

from .models import SongData

# β版のメッセージを出すかを決めるやつ
is_beta = True

# トップ画面
def top(request):
    return render(request, 'top.html',{ "is_beta":is_beta, "is_app":False })

# 定数検索ページ
def const_search(request):

    song_data = SongData.objects.all()
    context = { "is_beta":is_beta, "is_app":True, "song_data":song_data }

    if request.POST:

        # POSTから検索queryを取得
        query = request.POST.get("query")

        # 文字が入力されてないなら全部返す
        # 入力されているなら検索して返す
        if query=="":
            song_search = [ e for e in SongData.objects.all() ]
        else:
            song_search = [ e for e in SongData.objects.filter(Q(song_name__icontains=query) | Q(song_auther__icontains=query) ) ]

        # 整える
        search_hit_count = len(song_search)
        song_response = [ render_to_string("const_search/song_info.html",context={"song":song}) for song in song_search[:30] ]

        # 多すぎたらこうすうる
        if search_hit_count  > 30:
            song_response.append(render_to_string("const_search/too_many_result_info.html"))

        # Jsonとして返す
        d = {
                "query":query,
                "search_response":song_response[::-1],
                "search_hit_count":search_hit_count,
            }
        return JsonResponse(d)

    # renderする
    return render(request, 'const_search.html',context=context)

# app2
def app2(request):
    return render(request, 'app2.html',{ "is_beta":is_beta, "is_app":True })