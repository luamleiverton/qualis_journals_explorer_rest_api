import tabula as tb
import csv
import os
from django.conf import settings
from django.shortcuts import render
from qualis.models import Journals 

def import_file(request):
    url = 'http://www.cin.ufpe.br/~imprensa/NovoQualisPeriodico.pdf'
    file = os.path.join(settings.MEDIA_ROOT_JOURNALS, "qualis.csv")
    try:
        tb.convert_into(url, file, output_format="csv", pages="all")
    except:
        raise ConnectionError('Recurso indisponível')
    journals_list = open_file(file)

    formatted_list = format_journals_list(journals_list)
    data = persist_data(formatted_list)
    included_registers = len(data[0])
    non_included_registers = len(data[1])
    context = {
        'included_list':data[0],
        'non_included_list':data[1],
        'count_included_register':included_registers,
        'count_non_included_register':non_included_registers,
    }

    return render(request, 'importa_arquivo.html', context)


def open_file(file):
    with open(file) as f:
        lista=[]
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            lista.append(line[0])
    return lista


def split_issn_name(item):
    item = item.replace('"','')
    sep_issn_name=item[9]
    if sep_issn_name == ' ':
        item = item[:9]+','+item[9:]
        return item
    return item


def split_qualis(item):
    classificacao1 = ('A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2','C3', 'C4', 'NP')
    classificacao2 = ('C')
    if item.endswith(classificacao1):
        value = item[-3:]
        blank_char = value.find(' ')
        if blank_char == 0:
            item = item.replace(value[blank_char], ',')
    if item.endswith(classificacao2):
        value = item[-2:]
        blank_char = value.find(' ')
        if blank_char == 0:
            item = item.replace(value[blank_char], ',')
    return item

def remove_name_sep(item):
    position = [pos for pos, char in enumerate(item) if char ==',']
    if len(position)>2:
        del position[0]
        name = item[10:position[-1]]
        item = item.replace(name, name.replace(',', ' '))
    return item

def complete_string(item):
    count = item.count(',')
    if count != 2:
        item = item[:-1]+', '
    return item

def format_journals_list(journals_list):
    formatted_list=[]
    for item in journals_list:
        item = split_issn_name(item)
        item = split_qualis(item)
        item = remove_name_sep(item)
        item = complete_string(item)
        item = item.split(',')
        formatted_list.append(item)
    return formatted_list

def persist_data(formatted_list):
    included_items = []
    non_included_items=[]
    for register in formatted_list:
        if register[0] is not None and register[0] != 0:
            issn = str(register[0])
            if issn[4]=='-':
                issn = issn.replace('-','')
        
        if register[1] is not None and register[1] != '':
            journal = str(register[1])

        if register[2] is not None and register[2] != '':
            qualis = register[2]
            if len(qualis)>2:
                journal = journal+qualis
                qualis=''
        
        try:
            obj_issn = Journals.objects.get(issn=issn, journal=journal).issn
        except:
            obj_issn = None

        try:
            obj_journal = Journals.objects.get(issn=issn, journal=journal).journal
        except:
            obj_journal = None


        try:
            obj_qualis = Journals.objects.get(issn=issn, journal=journal).qualis
        except:
            obj_qualis = None

        if (obj_issn==issn and obj_journal==journal and obj_qualis==qualis):
            if (qualis != obj_qualis):
                Journals.objects.filter(issn=issn, journal=journal).update(qualis=qualis)
            else:
                continue
        else:
            try:
                register = Journals.objects.create(
                    issn = issn,
                    journal = journal,
                    qualis = qualis
                )
                register.save()
                included_items.append([issn, journal, qualis])
            except:
                non_included_items.append([issn, journal, qualis])
                continue
    return [included_items, non_included_items]


