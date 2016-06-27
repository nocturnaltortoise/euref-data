# from bs4 import BeautifulSoup
import urllib.request, json, os.path
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap


def file_exists(filepath):
    return os.path.exists(filepath)


def write_file(filepath, contents):
    with open(filepath, 'w') as file:
        file.write(contents)


def get_signatures_by_constituency(json_file):
    with open(json_file) as file:
        json_data = json.load(file)
        constituencies = json_data['data']['attributes']['signatures_by_constituency']

    return constituencies


def get_petition():
    return urllib.request.urlopen('https://petition.parliament.uk/petitions/131215.json')


def sort_constituencies(list):
    return sorted(list, key = lambda k : k['signature_count'], reverse=True)


def print_graph(left_intervals, width, results, labels, color):
    plt.bar(left_intervals, results, width, color=color)
    plt.xticks(left_intervals + width/2, labels)
    plt.show()


def analyse(json_file):
    constituencies = get_signatures_by_constituency(json_file)
    sorted_constituencies = sort_constituencies(constituencies)

    signatures = [sorted_constituencies[i]['signature_count'] for i in range(len(sorted_constituencies))]
    constituency_names = [sorted_constituencies[i]['name'] for i in range(len(sorted_constituencies))]

    test = [signatures[i] for i in range(5)]
    test_labels = [constituency_names[i] for i in range(5)]
    test_labels = [ '\n'.join(wrap(label,10)) for label in test_labels ]

    width = 0.7
    left = np.arange(len(test))

    print_graph(left, width, test, test_labels, 'r')


if not file_exists('petitions.json'):
    response = get_petition()
    write_file('petitions.json', response.read().decode('utf-8'))

analyse('petitions.json')


# wiki_data = urllib.request.urlopen('https://en.wikipedia.org/w/api.php?action=query&titles=List_of_United_Kingdom_Parliament_constituencies&action=raw').read()
# html = BeautifulSoup(wiki_data, 'html.parser')
#
# print(html.title)
