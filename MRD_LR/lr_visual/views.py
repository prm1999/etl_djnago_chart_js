from django.db.models import Count
from django.shortcuts import render
from .models import completeData
from lr_visual import staticVar


# ─────────────────────────────────────────────
# Home — Raw data overview table
# ─────────────────────────────────────────────
def home(request):
    data = completeData.objects.all()[:900]
    context = {
        'MSG': 'Customer Data Overview',
        'dataTable': data,
    }
    return render(request, 'home.html', context)


# ─────────────────────────────────────────────
# Data Explorer — Zone & Month filtered chart
# ─────────────────────────────────────────────
def drop_down(request):
    context = {
        'MSG': 'Data Explorer',
        'monthList': staticVar.MONTH_LIST,
        'zoneList': staticVar.ZONE_LIST_NAME,
    }

    if request.method == 'POST':
        selected_months = request.POST.getlist('month_dropdown')
        selected_zone = request.POST.get('zone_dropdown')
        selected_chart = request.POST.get('chart_dropdown', 'column')

        sample_data = (
            completeData.objects
            .filter(MONTH__in=selected_months, ZONE_NAME__iexact=selected_zone)
            .order_by('CA_NO', 'MONTH')[:10]
        )

        count_by_zone = (
            completeData.objects
            .filter(MONTH__in=selected_months)
            .values('ZONE_NAME')
            .annotate(COUNT=Count('CA_NO'))
            .order_by('ZONE_NAME')
        )

        series_data = [{
            'name': 'Zone Count',
            'data': list(count_by_zone.values_list('COUNT', flat=True))
        }]
        cat_list = list(count_by_zone.values_list('ZONE_NAME', flat=True))

        context.update({
            'dataTable': sample_data,
            'seriesData': series_data,
            'catList': cat_list,
            'selectedmonth': ', '.join(selected_months),
            'userSelectedmonth': selected_months,
            'selectedchart': selected_chart,
        })

    return render(request, 'dropdown.html', context)


# ─────────────────────────────────────────────
# Distribution — Pie / Donut chart by zone
# ─────────────────────────────────────────────
def pie_chart(request):
    context = {
        'MSG': 'Customer Distribution',
        'monthList': staticVar.MONTH_LIST,
        'zoneList': staticVar.ZONE_LIST_NAME,
    }

    if request.method == 'POST':
        selected_months = request.POST.getlist('month_dropdown')
        selected_zone = request.POST.get('zone_dropdown')

        sample_data = (
            completeData.objects
            .filter(MONTH__in=selected_months, ZONE_NAME__iexact=selected_zone)
            .order_by('CA_NO', 'MONTH')[:10]
        )

        # Group customer count by zone for selected months
        count_by_zone = (
            completeData.objects
            .filter(MONTH__in=selected_months)
            .values('ZONE_NAME')
            .annotate(COUNT=Count('CA_NO'))
            .order_by('ZONE_NAME')
        )

        # Pure ORM — no pandas needed, safe against empty zones
        total_count = sum(r['COUNT'] for r in count_by_zone) or 1  # guard division by zero

        series_data = [
            {
                'name': row['ZONE_NAME'],
                'y': round((row['COUNT'] / total_count) * 100, 2),
            }
            for row in count_by_zone
        ]

        context.update({
            'dataTable': sample_data,
            'seriesData': series_data,
            'selectedmonth': ', '.join(selected_months),
            'userSelectedmonth': selected_months,
        })

    return render(request, 'piechart.html', context)


# ─────────────────────────────────────────────
# Drill Down — Zone pie with bucket breakdown
# ─────────────────────────────────────────────
def drill_down(request):
    context = {
        'MSG': 'Zone Drill Down',
        'monthList': staticVar.MONTH_LIST,
        'zoneList': staticVar.ZONE_LIST_NAME,
    }

    if request.method == 'POST':
        selected_months = request.POST.getlist('month_dropdown')
        selected_zone = request.POST.get('zone_dropdown')
        selected_chart = request.POST.get('chart_dropdown', 'column')
        btk_list = staticVar.BUCKET_DISPLAY_LIST

        sample_data = (
            completeData.objects
            .filter(MONTH__in=selected_months, ZONE_NAME__iexact=selected_zone)
            .order_by('CA_NO', 'MONTH')[:10]
        )

        count_by_zone = (
            completeData.objects
            .filter(MONTH__in=selected_months)
            .values('ZONE_NAME')
            .annotate(COUNT=Count('CA_NO'))
            .order_by('ZONE_NAME')
        )

        bucket_counts = (
            completeData.objects
            .filter(MONTH__in=selected_months)
            .values('ZONE_NAME', 'BUCKETING_DISPLAY')
            .annotate(COUNT=Count('CA_NO'))
            .order_by('ZONE_NAME')
        )

        total_count = sum(r['COUNT'] for r in count_by_zone) or 1  # guard div by zero

        # Build a dict {ZONE_NAME: PERCENTAGE} for O(1) lookup — no pandas needed
        zone_pct_map = {
            row['ZONE_NAME']: round((row['COUNT'] / total_count) * 100, 2)
            for row in count_by_zone
        }

        series_data, drill_list = [], []

        for zone in staticVar.ZONE_LIST_NAME:
            pct = zone_pct_map.get(zone, 0)

            bucket_data = []
            for btk in btk_list:
                btk_qs = bucket_counts.filter(
                    ZONE_NAME__iexact=selected_zone,
                    BUCKETING_DISPLAY__iexact=btk,
                )
                val = list(btk_qs.values_list('COUNT', flat=True))
                bucket_data.append([btk, val[0] if val else 0])

            series_data.append({'name': zone, 'y': pct, 'drilldown': zone})
            drill_list.append({
                'type': selected_chart,
                'name': zone,
                'id': zone,
                'data': bucket_data,
                'tooltip': {
                    'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                    'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>',
                },
            })

        context.update({
            'dataTable': sample_data,
            'seriesData': series_data,
            'dataList': drill_list,
            'selectedmonth': ', '.join(selected_months),
            'userSelectedmonth': selected_months,
            'selectedchart': selected_chart,
        })

    return render(request, 'drill_down.html', context)


# ─────────────────────────────────────────────
# Defaulter Analysis (Hue One)
# ─────────────────────────────────────────────
def hue_one(request):
    context = {
        'MSG': 'Defaulter Analysis',
        'monthList': staticVar.MONTH_LIST,
        'zoneList': staticVar.ZONE_LIST_NAME,
        'btkList': staticVar.BUCKET_DISPLAY_LIST,
    }

    if request.method == 'POST':
        selected_months = request.POST.getlist('month_dropdown')
        selected_count = request.POST.get('count_dropdown', 2)

        all_defaulters = (
            completeData.objects
            .filter(BUCKETING_DERIVED__iexact='Defaulter')
            .order_by('CA_NO', 'MONTH')
        )
        main_count = all_defaulters.count()

        repeat_defaulters = (
            all_defaulters
            .values('CA_NO')
            .annotate(COUNT=Count('BUCKETING_DERIVED'))
            .filter(COUNT__gte=selected_count)
        )
        ca_list = repeat_defaulters.values_list('CA_NO', flat=True)

        filtered_data = (
            completeData.objects
            .filter(CA_NO__in=ca_list)
            .order_by('CA_NO', 'MONTH')
        )
        defaulter_count = filtered_data.count()

        zone_count = (
            filtered_data
            .values('ZONE_NAME')
            .annotate(COUNT=Count('CA_NO'))
            .order_by('ZONE_NAME')
        )

        series_data = [{
            'name': 'Zone',
            'data': list(zone_count.values_list('COUNT', flat=True)),
            'colorByPoint': True,
        }]

        context.update({
            'main_count': main_count,
            'defauter_count': defaulter_count,
            'dataTable': filtered_data[:10],
            'seriesData': series_data,
            'catList': staticVar.ZONE_LIST_NAME,
            'selectedmonth': ', '.join(selected_months),
            'selectedcount': selected_count,
        })

    return render(request, 'hue_one.html', context)


# ─────────────────────────────────────────────
# Zone Analysis (Hue Two)
# ─────────────────────────────────────────────
def hue_two(request):
    context = {
        'MSG': 'Zone Analysis',
        'monthList': staticVar.MONTH_LIST,
        'zoneList': staticVar.ZONE_LIST_NAME,
        'btkList': staticVar.BUCKET_DISPLAY_LIST,
    }

    if request.method == 'POST':
        selected_months = request.POST.getlist('month_dropdown')
        selected_zone = request.POST.get('zone_dropdown')
        selected_chart = request.POST.get('chart_dropdown', 'column')

        sample_data = (
            completeData.objects
            .filter(MONTH__in=selected_months, ZONE_NAME__iexact=selected_zone)
            .order_by('CA_NO', 'MONTH')[:10]
        )

        context.update({
            'dataTable': sample_data,
            'selectedmonth': ', '.join(selected_months),
            'userSelectedmonth': selected_months,
            'selectedchart': selected_chart,
        })

    return render(request, 'hue_two.html', context)


# ─────────────────────────────────────────────
# Hue Three (mirrors Hue One logic — distinct view)
# ─────────────────────────────────────────────
def hue_three(request):
    context = {
        'MSG': 'Extended Defaulter View',
        'monthList': staticVar.MONTH_LIST,
        'zoneList': staticVar.ZONE_LIST_NAME,
        'btkList': staticVar.BUCKET_DISPLAY_LIST,
    }

    if request.method == 'POST':
        selected_months = request.POST.getlist('month_dropdown')
        selected_count = request.POST.get('count_dropdown', 2)

        all_defaulters = (
            completeData.objects
            .filter(BUCKETING_DERIVED__iexact='Defaulter')
            .order_by('CA_NO', 'MONTH')
        )
        main_count = all_defaulters.count()

        repeat_defaulters = (
            all_defaulters
            .values('CA_NO')
            .annotate(COUNT=Count('BUCKETING_DERIVED'))
            .filter(COUNT__gte=selected_count)
        )
        ca_list = repeat_defaulters.values_list('CA_NO', flat=True)

        filtered_data = (
            completeData.objects
            .filter(CA_NO__in=ca_list)
            .order_by('CA_NO', 'MONTH')
        )
        defaulter_count = filtered_data.count()

        zone_count = (
            filtered_data
            .values('ZONE_NAME')
            .annotate(COUNT=Count('CA_NO'))
            .order_by('ZONE_NAME')
        )

        series_data = [{
            'name': 'Zone',
            'data': list(zone_count.values_list('COUNT', flat=True)),
            'colorByPoint': True,
        }]

        context.update({
            'main_count': main_count,
            'defauter_count': defaulter_count,
            'dataTable': filtered_data[:10],
            'seriesData': series_data,
            'catList': staticVar.ZONE_LIST_NAME,
            'selectedmonth': ', '.join(selected_months),
            'selectedcount': selected_count,
        })

    return render(request, 'hue_three.html', context)
