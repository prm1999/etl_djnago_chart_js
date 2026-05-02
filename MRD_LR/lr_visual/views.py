from django.db.models import Count
from django.shortcuts import render
from .models import completeData
from lr_visual import staticVar


def home(request):
    msg = "Hii"
    dataTable = completeData.objects.all()[:900]
    # print(dataTable.to_dataframe())

    context = {
        'MSG': msg,
        'dataTable': dataTable,
    }
    return render(request, 'home.html', context=context)


def drop_down(request):
    mesg = "Hello drop drown"

    monthList = staticVar.MONTH_LIST  # getting month list
    zoneList = staticVar.ZONE_LIST_NAME
    # zoneList = list(completeData.objects.all().values_list('ZONE_NAME', flat=True).distinct())#getting Zone name list
    # print(zoneList) finding all zones in the dataframe
    context = {
        'MSG': mesg,
        'monthList': monthList,
        'zoneList': zoneList,
    }
    if request.method == 'POST':
        selectedmonth = request.POST.getlist(
            "month_dropdown")  # getlist is ued when  we want multiple month at the time
        print(selectedmonth)
        selectedzone = request.POST.get("zone_dropdown")
        print(selectedzone)
        selectedchart = request.POST.getlist("chart_dropdown")
        print(selectedchart)

        QS_data = completeData.objects.filter(
            MONTH__in=selectedmonth,
            ZONE_NAME__iexact=selectedzone).order_by("CA_NO", "MONTH")[
                  :10]  # filter the customer by month and zone name

        count_Customer = completeData.objects.filter(
            MONTH__in=selectedmonth,
        ).values('ZONE_NAME').annotate(COUNT=Count('CA_NO')).order_by('ZONE_NAME')
        print(count_Customer.to_dataframe)

        seriesData = [{
            "name": "Zone  Name",
            "data": list(count_Customer.values_list("COUNT", flat=True))
        }]
        print(seriesData)
        catList = list((count_Customer.values_list("ZONE_NAME", flat=True)))
        print(catList)
        context.update({
            'userSelectedmonth': selectedmonth,
            'dataTable': QS_data,
            'seriesData': seriesData,
            'catList': catList,
            # 'selectedmonth':selectedmonth,
            'selectedmonth': ",".join(selectedmonth),
            'selectedchart': selectedchart,
        })

    return render(request, 'dropdown.html', context=context)


def pie_chart(request):
    msg = "welcome to pie chart"
    monthList = staticVar.MONTH_LIST  # getting month list
    zoneList = staticVar.ZONE_LIST_NAME  # print(dataTable.to_dataframe())
    context = {
        'MSG': msg,
        'monthList': monthList,
        'zoneList': zoneList,

    }

    if request.method == 'POST':
        selectedmonth = request.POST.getlist("month_dropdown")
        # print(selectedmonth)
        selectedzone = request.POST.get("zone_dropdown")
        # print(selectedzone)
        selectedchart = request.POST.getlist("chart_dropdown")
        # print(selectedchart)

        QS_data = completeData.objects.filter(
            MONTH__in=selectedmonth,
            ZONE_NAME__iexact=selectedzone).order_by("CA_NO", "MONTH")[
                  :10]  # filter the customer by month and zone name

        count_Customer = completeData.objects.filter(
            MONTH__in=selectedmonth,
        ).values('ZONE_NAME').annotate(COUNT=Count('CA_NO')).order_by('ZONE_NAME')

        # (customer count per zone /sum  of all customer)*100

        # totalCount = (list(count_Customer.values_list("COUNT", flat=True)))
        # print(totalCount)
        totalCount = sum(list(count_Customer.values_list("COUNT", flat=True)))
        print(totalCount)

        count_Customer_DF = count_Customer.to_dataframe()
        count_Customer_DF["PERCENTAGE"] = round((count_Customer_DF["COUNT"] / totalCount) * 100, 2)

        print(count_Customer_DF)

        seriesData = []
        for zone in zoneList:
            tempQS = count_Customer_DF.query(f"ZONE_NAME=='{zone}'")
            seriesData.append({
                "name": zone,
                "y": tempQS["PERCENTAGE"].tolist()[0],
            })
        print(seriesData)
        context.update({
            'userSelectedmonth': selectedmonth,
            'dataTable': QS_data,
            'seriesData': seriesData,
            # 'catList': catList,
            'selectedmonth': ",".join(selectedmonth),
            'selectedchart': selectedchart,
        })

    return render(request, 'piechart.html', context=context)


def drill_down(request):
    msg = "welcome to drill_down"
    monthList = staticVar.MONTH_LIST  # getting month list
    zoneList = staticVar.ZONE_LIST_NAME  # print(dataTable.to_dataframe())
    btkList = staticVar.BUCKET_DISPLAY_LIST
    context = {
        'MSG': msg,
        'monthList': monthList,
        'zoneList': zoneList,

    }

    if request.method == 'POST':
        selectedmonth = request.POST.getlist("month_dropdown")
        # print(selectedmonth)
        selectedzone = request.POST.get("zone_dropdown")
        # print(selectedzone)
        selectedchart = request.POST.getlist("chart_dropdown")
        # print(selectedchart)

        QS_data = completeData.objects.filter(
            MONTH__in=selectedmonth,
            ZONE_NAME__iexact=selectedzone).order_by("CA_NO", "MONTH")[
                  :10]  # filter the customer by month and zone name

        count_Customer = completeData.objects.filter(
            MONTH__in=selectedmonth,
        ).values('ZONE_NAME').annotate(COUNT=Count('CA_NO')).order_by('ZONE_NAME')

        btkcount = completeData.objects.filter(
            MONTH__in=selectedmonth,
        ).values('ZONE_NAME', 'BUCKETING_DISPLAY').annotate(COUNT=Count('CA_NO')).order_by('ZONE_NAME')
        # print(btkcount.to_dataframe)

        # print(list(completeData.objects.filter(MONTH__in=selectedmonth,).order_by('BUCKETING_DISPLAY').values_list('BUCKETING_DISPLAY',flat=True).distinct()))
        # print all the bucket present in zone
        # (customer count per zone /sum  of all customer)*100

        # totalCount = (list(count_Customer.values_list("COUNT", flat=True)))
        # print(totalCount)
        totalCount = sum(list(count_Customer.values_list("COUNT", flat=True)))
        # print(totalCount)

        count_Customer_DF = count_Customer.to_dataframe()
        count_Customer_DF["PERCENTAGE"] = round((count_Customer_DF["COUNT"] / totalCount) * 100, 2)

        # print(count_Customer_DF)

        seriesData, dataList = [], []
        for zone in zoneList:

            tempQS = count_Customer_DF.query(f"ZONE_NAME=='{zone}'")

            tempList = []

            for btk in btkList:
                btkQS = btkcount.filter(
                    ZONE_NAME__iexact=selectedzone,
                    BUCKETING_DISPLAY__iexact=btk,
                )
                btkVal = list(btkQS.values_list("COUNT", flat=True))[0]
                tempList.append([btk, btkVal])

            seriesData.append({
                "name": zone,
                "y": tempQS["PERCENTAGE"].tolist()[0],
                "drilldown": zone,

            })
            dataList.append({
                "type": selectedchart,
                "name": zone,
                "id": zone,
                "data": tempList,
                ' tooltip':
                    {
                        'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                        'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
                    },

            })

            print(dataList)

        print(seriesData)
        context.update({
            'userSelectedmonth': selectedmonth,
            'dataTable': QS_data,
            'seriesData': seriesData,
            'dataList': dataList,
            # 'catList': catList,
            'selectedmonth': ",".join(selectedmonth),
            'selectedchart': selectedchart,
        })

    return render(request, 'drill_down.html', context=context)


def hue_one(request):
    msg = 'hello hue one'
    monthList = staticVar.MONTH_LIST  # getting month list
    zoneList = staticVar.ZONE_LIST_NAME  # print(dataTable.to_dataframe())
    btkList = staticVar.BUCKET_DISPLAY_LIST
    context = {
        'MSG': msg,
        'monthList': monthList,
        'zoneList': zoneList,
        'btkList': btkList,

    }

    if request.method == 'POST':
        selectedmonth = request.POST.getlist("month_dropdown")
        # print(selectedmonth)
        selectedzone = request.POST.get("zone_dropdown")
        # print(selectedzone)
        selectedchart = request.POST.getlist("chart_dropdown")
        # print(selectedchart)
        selectedbucket = request.POST.get("bucket_dropdown")
        # print(selectedcount)
        selectedcount = request.POST.get("count_dropdown")
        # print(selectedcount)

        QS_data = completeData.objects.filter(
            # MONTH__in=selectedmonth,
            BUCKETING_DERIVED__iexact='Defaulter',
            # ZONE_NAME__iexact=selectedzone
        ).order_by("CA_NO", "MONTH")

        main_count = len(QS_data)

        count_customer = QS_data.values("CA_NO").annotate(COUNT=Count('BUCKETING_DERIVED')).order_by('CA_NO')
        count_customer = count_customer.filter(COUNT__gte=selectedcount)
        print(count_customer.to_dataframe())
        customer_list = count_customer.values_list('CA_NO', flat=True)
        QS_data = completeData.objects.filter(
            CA_NO__in=customer_list
        ).order_by("CA_NO", "MONTH")
        defauter_count = len(QS_data)

        zone_count = QS_data.values('ZONE_NAME').annotate(COUNT=Count("CA_NO")).order_by('ZONE_NAME')
        print(zone_count.to_dataframe())
        for zone in zoneList:
            seriesData = [{
                'name': 'ZONE',
                'data': list(zone_count.values_list('COUNT', flat=True)),
                'colorByPoint': 'true'
            }]
            print(seriesData)

        context.update({
            # 'userSelectedmonth': selectedmonth,
            'main_count': main_count,
            'defauter_count': defauter_count,
            'dataTable': QS_data[:2],
            'seriesData': seriesData,
            # 'dataList': dataList,
            'catList': zoneList,
            'selectedmonth': ",".join(selectedmonth),
            'selectedcount': selectedcount,
        })

    return render(request, 'hue_one.html', context=context)


def hue_two(request):
    mess = "hello from hue_two"
    monthList = staticVar.MONTH_LIST  # getting month list
    zoneList = staticVar.ZONE_LIST_NAME  # print(dataTable.to_dataframe())
    btkList = staticVar.BUCKET_DISPLAY_LIST
    context = {
        'MSG': mess,
        'monthList': monthList,
        'zoneList': zoneList,
        'btkList': btkList,
    }

    if request.method == 'POST':
        selectedmonth = request.POST.getlist("month_dropdown")
        # print(selectedmonth)
        selectedzone = request.POST.get("zone_dropdown")
        # print(selectedzone)
        selectedchart = request.POST.getlist("chart_dropdown")
        # print(selectedchart)

        QS_data = completeData.objects.filter(
            MONTH__in=selectedmonth,
            ZONE_NAME__iexact=selectedzone).order_by("CA_NO", "MONTH")[:10]  # filter the customer by month and zone name

        count_Customer = completeData.objects.filter(
            MONTH__in=selectedmonth,
        ).values('ZONE_NAME').annotate(COUNT=Count('CA_NO')).order_by('ZONE_NAME')

        context.update({
            'userSelectedmonth': selectedmonth,
            'dataTable': QS_data,
            #'seriesData': seriesData,
            #'dataList': dataList,
            # 'catList': catList,
            'selectedmonth': ",".join(selectedmonth),
            'selectedchart': selectedchart,
        })

    return render(request, 'hue_two.html', context=context)

def hue_three(request):
    msg = 'hello hue three'
    monthList = staticVar.MONTH_LIST  # getting month list
    zoneList = staticVar.ZONE_LIST_NAME  # print(dataTable.to_dataframe())
    btkList = staticVar.BUCKET_DISPLAY_LIST
    context = {
        'MSG': msg,
        'monthList': monthList,
        'zoneList': zoneList,
        'btkList': btkList,

    }

    if request.method == 'POST':
        selectedmonth = request.POST.getlist("month_dropdown")
        # print(selectedmonth)
        selectedzone = request.POST.get("zone_dropdown")
        # print(selectedzone)
        selectedchart = request.POST.getlist("chart_dropdown")
        # print(selectedchart)
        selectedbucket = request.POST.get("bucket_dropdown")
        # print(selectedcount)
        selectedcount = request.POST.get("count_dropdown")
        # print(selectedcount)

        QS_data = completeData.objects.filter(
            # MONTH__in=selectedmonth,
            BUCKETING_DERIVED__iexact='Defaulter',
            # ZONE_NAME__iexact=selectedzone
        ).order_by("CA_NO", "MONTH")

        main_count = len(QS_data)

        count_customer = QS_data.values("CA_NO").annotate(COUNT=Count('BUCKETING_DERIVED')).order_by('CA_NO')
        count_customer = count_customer.filter(COUNT__gte=selectedcount)
        print(count_customer.to_dataframe())
        customer_list = count_customer.values_list('CA_NO', flat=True)
        QS_data = completeData.objects.filter(
            CA_NO__in=customer_list
        ).order_by("CA_NO", "MONTH")
        defauter_count = len(QS_data)

        zone_count = QS_data.values('ZONE_NAME').annotate(COUNT=Count("CA_NO")).order_by('ZONE_NAME')
        print(zone_count.to_dataframe())
        for zone in zoneList:
            seriesData = [{
                'name': 'ZONE',
                'data': list(zone_count.values_list('COUNT', flat=True)),
                'colorByPoint': 'true'
            }]
            print(seriesData)

        context.update({
            # 'userSelectedmonth': selectedmonth,
            'main_count': main_count,
            'defauter_count': defauter_count,
            'dataTable': QS_data[:2],
            'seriesData': seriesData,
            # 'dataList': dataList,
            'catList': zoneList,
            'selectedmonth': ",".join(selectedmonth),
            'selectedcount': selectedcount,
        })

    return render(request, 'hue_one.html', context=context)

